import requests
import os
from urllib.parse import urlparse
import hashlib
import mimetypes
from datetime import datetime

def calculate_file_hash(filepath):
    """Calculate SHA-256 hash of a file to check for duplicates."""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def is_valid_image_content_type(content_type):
    """Check if the content type is a valid image type."""
    valid_image_types = ['image/jpeg', 'image/png', 'image/gif', 'image/bmp']
    return content_type in valid_image_types

def generate_unique_filename(filename, directory):
    """Generate a unique filename by appending a timestamp if needed."""
    base, ext = os.path.splitext(filename)
    filepath = os.path.join(directory, filename)
    if not os.path.exists(filepath):
        return filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base}_{timestamp}{ext}"

def fetch_image(url, directory="Fetched_Images"):
    """Fetch and save an image from a URL, with duplicate checking and safety measures."""
    try:
        # Send a HEAD request to check headers before downloading
        head_response = requests.head(url, timeout=10, allow_redirects=True)
        head_response.raise_for_status()

        # Check Content-Type header
        content_type = head_response.headers.get('Content-Type', '')
        if not is_valid_image_content_type(content_type):
            print(f"✗ Invalid content type for {url}: {content_type}. Must be an image.")
            return False

        # Check Content-Length header (if available) for file size
        content_length = head_response.headers.get('Content-Length')
        if content_length and int(content_length) > 10 * 1024 * 1024:  # Limit to 10MB
            print(f"✗ File too large for {url}: {content_length} bytes.")
            return False

        # Fetch the image
        response = requests.get(url, timeout=10, stream=True)
        response.raise_for_status()

        # Extract filename from URL or generate a default one
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename or not mimetypes.guess_extension(content_type):
            filename = f"downloaded_image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        else:
            # Ensure proper extension based on content type
            expected_ext = mimetypes.guess_extension(content_type) or '.jpg'
            if not filename.lower().endswith(expected_ext.lower()):
                filename = os.path.splitext(filename)[0] + expected_ext

        # Create directory if it doesn't exist
        os.makedirs(directory, exist_ok=True)

        # Generate unique filename to avoid overwriting
        filename = generate_unique_filename(filename, directory)
        filepath = os.path.join(directory, filename)

        # Save the image temporarily to check for duplicates
        temp_filepath = os.path.join(directory, f"temp_{filename}")
        with open(temp_filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        # Check for duplicates by comparing file hash
        new_file_hash = calculate_file_hash(temp_filepath)
        for existing_file in os.listdir(directory):
            existing_filepath = os.path.join(directory, existing_file)
            if existing_filepath != temp_filepath and os.path.isfile(existing_filepath):
                if calculate_file_hash(existing_filepath) == new_file_hash:
                    print(f"✗ Duplicate image detected for {url}. Image not saved.")
                    os.remove(temp_filepath)
                    return False

        # Move temp file to final location
        os.rename(temp_filepath, filepath)
        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error for {url}: {e}")
        return False
    except Exception as e:
        print(f"✗ An error occurred for {url}: {e}")
        return False

def main():
    """Main function to run the Ubuntu Image Fetcher."""
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    # Get URLs from user (comma-separated for multiple URLs)
    urls_input = input("Please enter image URL(s) (comma-separated for multiple): ")
    urls = [url.strip() for url in urls_input.split(',') if url.strip()]

    if not urls:
        print("✗ No valid URLs provided.")
        return

    success_count = 0
    for url in urls:
        if fetch_image(url):
            success_count += 1

    print(f"\nProcessed {len(urls)} URL(s). Successfully fetched {success_count} image(s).")
    print("Connection strengthened. Community enriched.")

if __name__ == "__main__":
    main()
