#!/usr/bin/env python3
"""
Fetch a random photo from Flickr and update README.md
"""

import os
import random
import requests


def fetch_flickr_photos(user_id):
    """Fetch photos from Flickr public feed"""
    url = f"https://www.flickr.com/services/feeds/photos_public.gne?id={user_id}&format=json&nojsoncallback=1"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("items", [])
    except Exception as e:
        print(f"Error fetching Flickr photos: {e}")
        return []


def get_random_photo(photos):
    """Select a random photo from the list"""
    if not photos:
        print("No photos available")
        return None

    photo = random.choice(photos)

    # Get the larger image URL (replace _m with _b for large size)
    image_url = photo.get("media", {}).get("m", "")
    if image_url:
        # Convert to large size
        image_url = image_url.replace("_m.jpg", "_b.jpg")

    return {
        "url": image_url,
        "title": photo.get("title", "Flickr Photo"),
        "link": photo.get("link", ""),
        "published": photo.get("published", ""),
    }


def update_readme(photo_info):
    """Update README.md with the photo information"""
    readme_path = "README.md"

    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"README.md not found")
        return False

    # Create the new photo section
    photo_section = f"""# I am user3301

![](https://github.com/user3301/user3301/blob/master/assets/header.png)

## 📸 My Photo of the Day

[![{photo_info["title"]}]({photo_info["url"]})]({photo_info["link"]})

*[{photo_info["title"]}]({photo_info["link"]}) - Click to view on Flickr*

---

<!-- <img
  src="https://github.com/user3301/user3301/blob/master/images/stat.svg"
  alt="My Activity Stats"
/>
 -->
"""

    # Write the updated content
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(photo_section)

    print(f"✅ README updated with: {photo_info['title']}")
    print(f"   Image URL: {photo_info['url']}")
    return True


def main():
    user_id = os.environ.get("FLICKR_USER_ID")
    if not user_id:
        print("Error: FLICKR_USER_ID environment variable not set")
        return

    print(f"Fetching photos for user: {user_id}")
    photos = fetch_flickr_photos(user_id)

    if not photos:
        print("No photos found or error occurred")
        return

    print(f"Found {len(photos)} photos")
    photo_info = get_random_photo(photos)

    if photo_info and photo_info["url"]:
        update_readme(photo_info)
    else:
        print("Could not select a random photo")


if __name__ == "__main__":
    main()
