from typing import Any, List, Dict
import requests
import json, re, os
import string
import random
from models import Item, ItemImage
from PIL import Image
import io
from constants import STATIC_FOLDER, IMAGES_UPLOAD_FOLDER
import pandas as pd

def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError as e:
        return False
    return True

def get_trip_prompt(trip_details):
    return f"""
Trip Parameters
Departure City: {trip_details['departure_city']}
Destination City: {trip_details['destination_city']}
Start Date: {trip_details['start_date']}
End Date: {trip_details['end_date']}
Laundry Service Available: {trip_details['laundry_service_available']}
Working Remotely: {trip_details['working_remotely']}
"""

def trip_itineary_to_textarea_string(trip_itinerary):
  """Converts a JSON itinerary to a hierarchical string for a textarea.

  Args:
    data: A JSON object representing the itinerary.

  Returns:
    A hierarchical string suitable for rendering in a textarea.
  """
  if type(trip_itinerary) is str:
     trip_itinerary = json.loads(trip_itinerary)

  output = ""
  for day, activities in trip_itinerary.items():
    output += f"## {day}\n"  # Day as a heading
    for i, activity in enumerate(activities):
      output += f"{i+1}. {activity.get('activity', '')}\n"
      for key in ['time', 'description', 'address', 'duration', 'transportation', 'cost']:
        value = activity.get(key)
        if value:
          output += f"    - {key[0].upper() + key[1:]}: {value}\n"
      output += "\n"
    output += "\n"
  return output

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

def get_json_from_generation(content: str) -> Any:
    json_data = None
    try:
        output_stripped = re.sub(r'```(?:json|JSON)\n|\n```', '', content)
        # Handle the extra double quote edge case
        output_stripped = output_stripped.strip()  # Remove leading/trailing whitespace
        if output_stripped.endswith('"'):
            output_stripped = output_stripped[:-1]
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
        # Resize the image & save the image.
        resized_image = resize_image_to_target(image.read())
        if resized_image:
          resized_image.save(item_image_static_filepath)
          item_image = ItemImage(
            item_id = item_id,
            path=item_image_filepath
          )
          db.session.add(item_image)
          user_item.images.append(item_image)
          status_codes["success"]+=1
        else:
           print(f"Error uploading: {image.filename}")
           status_codes["error"]+=1
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
    try:
      image = Image.open(io.BytesIO(image_data))
    except:
       print("Image could not be read.")
       return None

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
