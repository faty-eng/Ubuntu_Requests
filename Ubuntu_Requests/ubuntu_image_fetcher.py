import requests
import os 
import hashlib
from urllib.parse import urlparse

def get_filename_from_url(url):
    """Extracts the filename from a URL or generates one."""
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    return filename if filename else "downloaded_image.jpg"

def hash_content(content):
    """Returns a short hash of file content to detect duplicates."""
    return hashlib.md5(content).hexdigest()

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    urls_input = input("Please enter image URLs (separate multiple with spaces): ").strip()
    urls = urls_input.split()
    
    # Create directory
    os.makedirs("Fetched_Images", exist_ok=True)

    # Keep track of downloaded hashes to avoid duplicates
    existing_hashes = set()
    success_count = 0

    for url in urls:
        try:
            print(f"\nFetching from: {url}")
            response = requests.get(url, timeout=10, stream=True)
            response.raise_for_status()

            # Check content type for safety
            content_type = response.headers.get('Content-Type', '')
            if not content_type.startswith('image/'):
                print(f"✗ Skipped (not an image): {url}")
                continue

            # Read content
            content = response.content
            file_hash = hash_content(content)

            # Prevent duplicates
            if file_hash in existing_hashes:
                print("⚠ Duplicate detected. Skipping this image.")
                continue
            existing_hashes.add(file_hash)

            # Determine filename and save path
            filename = get_filename_from_url(url)
            filepath = os.path.join("Fetched_Images", filename)

            # Handle name conflicts
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(filepath):
                filepath = os.path.join("Fetched_Images", f"{base}_{counter}{ext}")
                counter += 1

            # Save the image
            with open(filepath, 'wb') as f:
                f.write(content)

            print(f"✓ Successfully fetched: {filename}")
            print(f"✓ Image saved to {filepath}")
            success_count += 1

        except requests.exceptions.RequestException as e:
            print(f"✗ Connection error while fetching {url}: {e}")
        except Exception as e:
            print(f"✗ An unexpected error occurred: {e}")

    print(f"\nConnection strengthened. Community enriched. {success_count} image(s) successfully fetched.")

if __name__ == "__main__":
    main()
