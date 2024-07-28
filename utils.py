from typing import Any, List, Dict
from constants import USER_AGENT_HEADER
import requests
import json, re, os
import string
import random
from models import Item, ItemImage
from PIL import Image
import io
from constants import STATIC_FOLDER, IMAGES_UPLOAD_FOLDER
import pandas as pd

def item_repository_csv_to_json(csv_file: str) -> List[Dict[str, Any]]:
  """Reads a CSV file and converts it to JSON.

  Args:
    csv_file: The path to the CSV file.

  Returns:
    A list of dictionaries, where each dictionary represents a row in the CSV.
  """

  item_repository_df = pd.read_csv(csv_file)
  item_repository_data: List[Dict[str, Any]] = []
  for _, item_details in item_repository_df.iterrows():
    item_repository_data.append(item_details.to_dict())
  return item_repository_data


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

def generate_item_image_id() -> str:
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(10))
    return random_string

def get_item_image_static_filepath(user_id: int, filename: str) -> tuple[str,str]:
    """
    Returns two filepaths.
    1) Image Filepath: Path where the image will be saved under the static folder.
    2) Static Image Filepath: Static Folder + "/" + Image Filepath
    """
    _, extension = os.path.splitext(filename)
    item_image_filepath = os.path.join(IMAGES_UPLOAD_FOLDER, "user_" + str(user_id), "image_" + generate_item_image_id() + "_"+ extension)
    item_image_static_filepath = os.path.join(STATIC_FOLDER, item_image_filepath)
    os.makedirs(os.path.dirname(item_image_static_filepath), exist_ok=True)
    return item_image_filepath, item_image_static_filepath


def get_image_path_from_item_image_id(db, item_image_id: int) -> str:
    image_path = None
    if item_image_id:
        item_image = db.session.get(ItemImage, item_image_id)
        if item_image:
            image_path = item_image.path
    return image_path


#### Item Image Upload Functions ####
def upload_item_images(db, user_id:int, item_id:int, images):
  status_codes = {"success" : 0, "error": 0, "all": 0}
  user_item = db.session.get(Item, item_id)
  for image in images:
    status_codes["all"]+=1
    if image.filename == '':
        status_codes["error"]+=1
        continue  # Skip to the next file if no file is selected.
    if image:
        # Construct the image destination path.
        item_image_filepath, item_image_static_filepath = get_item_image_static_filepath(user_id=user_id,
                                        filename=image.filename)
        # Create ItemImage DB Object.
        item_image = ItemImage(
            item_id = item_id,
            path=item_image_filepath
        )
        db.session.add(item_image)
        user_item.images.append(item_image)

        # Resize the image & save the image.
        resized_image = resize_image_to_target(image.read())
        resized_image.save(item_image_static_filepath)
        status_codes["success"]+=1
  db.session.commit()
  return status_codes

#### Image Resize Functions ####
def resize_image_to_target(image_data: bytes, target_size: int = 512) -> Image:
    """Resizes an image to a target size while preserving aspect ratio.

    Args:
        image_data: The raw image data (bytes).
        target_size: The desired size of the shorter side of the image (in pixels).

    Returns:
        The resized image data as bytes.
    """
    image = Image.open(io.BytesIO(image_data))

    # Calculate new dimensions while preserving aspect ratio
    width, height = image.size
    if width < height:
        new_width = target_size
        new_height = int(height * (target_size / width))
    else:
        new_height = target_size
        new_width = int(width * (target_size / height))

    resized_image = image.resize((new_width, new_height))
    return resized_image
