from llms import TripChecklistExpert, ProductImageToMetadataExpert, OutfitExpert
from constants import GEMINI_API_KEY
from flags import *

# Define the experts.
trip_checklist_expert = TripChecklistExpert(api_key=GEMINI_API_KEY, testing=LLM_TESTING)
product_image_to_metadata_expert = ProductImageToMetadataExpert(api_key=GEMINI_API_KEY, testing=LLM_TESTING)
outfit_expert = OutfitExpert(api_key=GEMINI_API_KEY, testing=LLM_TESTING)