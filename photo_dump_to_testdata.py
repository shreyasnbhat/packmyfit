import os
import shutil
import csv

def create_directory_structure(item_repository_path):
    """
    Creates the directory structure based on the item repository CSV file.

    Args:
        item_repository_path (str): Path to the item repository CSV file.
    """

    with open(item_repository_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            item_id = row['Name']
            category = row['Category']
            brand = row['Brand']
            os.makedirs(os.path.join('data', category, brand, item_id), exist_ok=True)

def copy_images(source_directory, item_repository_path):
    """
    Copies images from the source directory to the appropriate directory based on item IDs.

    Args:
        source_directory (str): Path to the directory containing the images.
        item_repository_path (str): Path to the item repository CSV file.
    """

    with open(item_repository_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            item_id = row['Name']
            category = row['Category']
            brand = row['Brand']
            image_name = f"{item_id}.jpg"  # Assuming image names are in the format "item_id.jpg"
            source_image_path = os.path.join(source_directory, image_name)
            destination_image_path = os.path.join('data', category, brand, item_id, image_name)
            if os.path.exists(source_image_path):
                shutil.copy2(source_image_path, destination_image_path)
                print(f"Copied {image_name} to {destination_image_path}")
            else:
                print(f"Image {image_name} not found in {source_directory}")

if __name__ == "__main__":
    item_repository_path = '/Users/shreyasbhat/Code/llms/trip_checklist/testdata/item_repository.csv'
    source_directory = '/Users/shreyasbhat/Code/llms/trip_checklist/testdata'  # Replace with your actual source directory

    create_directory_structure(item_repository_path)
    copy_images(source_directory, item_repository_path)
