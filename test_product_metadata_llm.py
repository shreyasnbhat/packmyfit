from llms import ProductImageToMetadataExpert
from constants import GEMINI_API_KEY

def generate_product_metadata():
  product_metadata_expert = ProductImageToMetadataExpert(api_key=GEMINI_API_KEY, testing = True)
  image_paths = ["Item Repository/PXL_20240702_180748313.MP.jpg", "Item Repository/PXL_20240702_180829353.MP.jpg"]
  product_metadata = product_metadata_expert.generate_product_metadata(image_paths = image_paths)
  print(product_metadata)

if __name__ == "__main__":
  generate_product_metadata()