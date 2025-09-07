Ubuntu Image Fetcher
Overview
The Ubuntu Image Fetcher is a Python script designed to download images from the web in the spirit of the Ubuntu philosophy: "I am because we are." This tool connects to the global internet community, respectfully fetches shared image resources, and organizes them for later use or sharing. The script fulfills an assignment to create a practical tool that fetches images, handles multiple URLs, prevents duplicates, ensures safe downloading, and incorporates proper error handling.
The project embodies the Ubuntu principles of:

Community: Connecting to web resources shared by others.
Respect: Handling errors gracefully and validating content before downloading.
Sharing: Saving images in an organized directory for easy access and sharing.
Practicality: Providing a reusable tool for image downloading.

Features

Prompts the user for one or more image URLs (comma-separated).
Creates a Fetched_Images directory to store downloaded images.
Validates image content using HTTP headers (Content-Type and Content-Length).
Prevents duplicate downloads by comparing file hashes (SHA-256).
Generates unique filenames to avoid overwriting existing files.
Handles errors for network issues, invalid URLs, or non-image content.
Supports multiple image formats (JPEG, PNG, GIF, BMP).
Limits file size to 10MB for safety.

Requirements
To run the script, you need:

Python 3.x
Required Libraries:
requests (for HTTP requests)
hashlib (for duplicate checking, included in Python standard library)
mimetypes (for file extension handling, included in Python standard library)
os and urllib.parse (included in Python standard library)



Install the requests library using pip:
pip install requests

File Structure

ubuntu_image_fetcher.py: The main Python script for fetching and saving images.
Fetched_Images/: Directory created automatically to store downloaded images.
README.md: This documentation file.

Setup Instructions

Clone or download the repository to your local machine:git clone https://github.com/your-username/Ubuntu_Requests.git


Navigate to the project directory:cd Ubuntu_Requests


Ensure the required libraries are installed (see Requirements).
Run the script:python ubuntu_image_fetcher.py



Usage

Run the script:python ubuntu_image_fetcher.py


You will see a welcome message:Welcome to the Ubuntu Image Fetcher
A tool for mindfully collecting images from the web


Enter one or more image URLs, separated by commas (e.g., https://example.com/image1.jpg, https://example.com/image2.png).
The script will:
Validate each URL and its content (checking Content-Type and file size).
Download valid images to the Fetched_Images directory.
Prevent duplicates by comparing file hashes.
Generate unique filenames if needed (e.g., appending a timestamp).
Display success or error messages for each URL.


Example output:Welcome to the Ubuntu Image Fetcher
A tool for mindfully collecting images from the web

Please enter image URL(s) (comma-separated for multiple): https://example.com/ubuntu-wallpaper.jpg
✓ Successfully fetched: ubuntu-wallpaper.jpg
✓ Image saved to Fetched_Images/ubuntu-wallpaper.jpg

Processed 1 URL(s). Successfully fetched 1 image(s).
Connection strengthened. Community enriched.



Implementation Details
The script is structured to meet the assignment requirements and challenge questions:
Core Functionality

URL Input: Accepts multiple URLs (comma-separated) from the user.
Directory Creation: Uses os.makedirs("Fetched_Images", exist_ok=True) to create the storage directory if it doesn't exist.
Image Fetching: Uses the requests library to fetch images, with a timeout of 10 seconds.
File Saving: Saves images in binary mode to the Fetched_Images directory.

Safety Precautions

Content Validation: Checks the Content-Type header to ensure the response is an image (JPEG, PNG, GIF, or BMP).
File Size Check: Limits downloads to 10MB using the Content-Length header to prevent large file downloads.
HEAD Request: Sends a preliminary HEAD request to check headers before downloading the full content, reducing unnecessary data transfer.

Duplicate Prevention

Hash Checking: Calculates the SHA-256 hash of downloaded images and compares them with existing files in the Fetched_Images directory to prevent duplicates.
Temporary Files: Saves images to a temporary file first, checking for duplicates before finalizing the save.

Unique Filenames

Filename Extraction: Extracts filenames from URLs using urllib.parse.urlparse and os.path.basename.
Extension Correction: Ensures the file extension matches the Content-Type using mimetypes.guess_extension.
Timestamp Appending: Generates unique filenames by appending a timestamp (e.g., image_20250907_121415.jpg) if a file already exists.

Error Handling

Handles requests.exceptions.RequestException for network issues (e.g., timeouts, invalid URLs).
Catches general exceptions for unexpected errors (e.g., file writing issues).
Provides clear error messages for each URL (e.g., invalid content type, file too large).

Ubuntu Principles

Community: Connects to the web to access shared resources.
Respect: Validates
