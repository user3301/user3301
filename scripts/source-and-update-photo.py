#!/usr/bin/env python3
"""
Fetch a random photo from Flickr and update README.md
"""

import os
import random
import requests
import re
from html.parser import HTMLParser


class HTMLStripper(HTMLParser):
    """Helper class to strip HTML tags"""

    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = []

    def handle_data(self, data):
        self.text.append(data)

    def get_data(self):
        return "".join(self.text)


def strip_html_tags(html):
    """Remove HTML tags from string"""
    if not html:
        return ""
    stripper = HTMLStripper()
    stripper.feed(html)
    return stripper.get_data().strip()


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

    # Extract description and clean HTML tags
    description_html = photo.get("description", "")
    description = strip_html_tags(description_html)

    # Remove "X posted a photo:" prefix that Flickr adds
    description = re.sub(r"^.+?\s+posted a photo:\s*", "", description)

    # If description is too long, truncate it
    if len(description) > 500:
        description = description[:497] + "..."

    return {
        "url": image_url,
        "title": photo.get("title", "Flickr Photo"),
        "link": photo.get("link", ""),
        "published": photo.get("published", ""),
        "description": description,
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
    description_section = ""
    if photo_info.get("description"):
        description_section = f"\n> {photo_info['description']}\n"

    photo_section = f"""# I am user3301

## 📸 ᴬ ᵈᵃⁱˡʸ ˢʰᵘᶠᶠˡᵉ ᶠʳᵒᵐ ᵐʸ ˡᵉⁿˢ ᵗᵒ ʸᵒᵘʳ ˢᶜʳᵉᵉⁿ

![Powered by GitHub Actions](https://img.shields.io/badge/Powered%20by-GitHub%20Actions-blue?logo=githubactions&logoColor=white)

[![{photo_info["title"]}]({photo_info["url"]})]({photo_info["link"]})

**[{photo_info["title"]}]({photo_info["link"]})**
{description_section}

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
    if photo_info.get("description"):
        print(f"   Description: {photo_info['description'][:100]}...")
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
