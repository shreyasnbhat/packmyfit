from app import app, db, Item, ItemImage
from celery import shared_task
from llms import ProductImageToMetadataExpert
from constants import GEMINI_API_KEY
import json
import os
import re
from memory_profiler import profile


@profile
@shared_task(ignore_result=False)
def generate_product_metadata(item_id):
    """Celery task to generate metadata for an item."""
    print("Hurrah")
    item = db.session.get(Item, item_id)
    item_image_paths = [
        image.path
        for image in item.images
    ]

    # Initialize the expert with your API key
    product_image_to_metadata_expert = ProductImageToMetadataExpert(
        api_key=GEMINI_API_KEY
    )

    # Generate metadata using the expert
    expert_result = product_image_to_metadata_expert.generate_product_metadata(
        image_paths=item_image_paths
    )

    # Update the item with the generated metadata
    if "brand" in expert_result and expert_result["brand"] is not None:
        item.brand = expert_result["brand"]
    if "care_instruction" in expert_result:
        item.care_instruction = expert_result["care_instruction"]
    if "material" in expert_result:
        item.material = json.dumps(expert_result["material"])
    if "primary_image_path" in expert_result:
        primary_image_path = re.sub(
            r"^static/", "", expert_result["primary_image_path"]
        )
        primary_item_image = (
            db.session.query(ItemImage).filter_by(path=primary_image_path).first()
        )
        if primary_item_image:
            item.primary_image_id = primary_item_image.id
        else:
            print(
                f"Warning: Could not find ItemImage with path {primary_image_path}"
            )

    db.session.add(item)
    db.session.commit()

    return f"Metadata generated for item {item_id}"