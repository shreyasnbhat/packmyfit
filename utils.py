from typing import Any
from constants import USER_AGENT_HEADER
import requests
import json, re
import string
import random
from models import ItemImage

def download_webpage(url: str, max_retries: int = 3) -> str:
  """Downloads the contents of a webpage and returns the HTML Content.

  Args:
      url: The URL of the webpage to download.
      max_retries: The maximum number of retries if a request fails.

  Returns:
      The HTML Content of the webpage, or None if all retries fail.
  """

  for attempt in range(max_retries):
    try:
      response = requests.get(url, headers=USER_AGENT_HEADER)
      response.raise_for_status()  # Raise an exception for bad status codes
      return response.text
    except requests.exceptions.RequestException as e:
      print(f"Error downloading {url}: {e}. Retrying... (Attempt {attempt+1}/{max_retries})")
      if attempt == max_retries - 1:
        print(f"Failed to download {url} after {max_retries} attempts.")
        return None

def get_json_from_generation(content: str) -> Any:
    json_data = None
    try:
        output_stripped = re.sub(r'```(?:json|JSON)\n|\n```', '', content)
        print(output_stripped)
        json_data = json.loads(output_stripped)
    except json.JSONDecodeError:
        raise json.JSONDecodeError("Failed to parse JSON from generation.")
    return json_data

def generate_item_image_id():
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(10))
    return random_string

def get_image_path_from_item_image_id(db, item_image_id):
    image_path = None
    if item_image_id:
        item_image = db.session.get(ItemImage, item_image_id)
        if item_image:
            image_path = item_image.path
    return image_path