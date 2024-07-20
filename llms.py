import google.generativeai as genai
from utils import get_json_from_generation
from constants import TRIP_CHECKLIST_EXPERT, PRODUCT_IMAGE_TO_METADATA_EXPERT
from constants import TEST_PRODUCT_METADATA, TEST_TRIP_CHECKLIST
import json
import time

class BaseLLM:
    model_name = None

    @staticmethod
    def initialize_model(api_key=None):
        genai.configure(api_key=api_key)

    @staticmethod
    def upload_to_gemini(path, display_name, mime_type=None):
        """Uploads the given file to Gemini.

        See https://ai.google.dev/gemini-api/docs/prompting_with_media
        """
        file = genai.upload_file(path, mime_type=mime_type, display_name=display_name)
        print(f"Uploaded file '{file.display_name}' as: {file.uri}")
        return file

    @staticmethod
    def wait_for_files(files):
        """Waits for the given files to be active.

        Some files uploaded to the Gemini API need to be processed before they can be
        used as prompt inputs. The status can be seen by querying the file's "state"
        field.

        This implementation uses a simple blocking polling loop. Production code
        should probably employ a more sophisticated approach.
        """
        print("Waiting for file processing...")
        for name in (file.name for file in files):
            file = genai.get_file(name)
            while file.state.name == "PROCESSING":
                print(".", end="", flush=True)
                time.sleep(10)
                file = genai.get_file(name)
                if file.state.name != "ACTIVE":
                    raise Exception(f"File {file.name} failed to process")
        print("...all files ready")
        print()

class GeminiFlash(BaseLLM):
    model_name = "gemini-1.5-flash"

class GeminiPro(BaseLLM):
    model_name = "gemini-1.5-pro"
    
class TripChecklistExpert(GeminiFlash):
    generation_config = {
            "temperature": 0,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "application/json",
        }
    generation = None
    testing = False # Returns a default JSON Response.

    def __init__(self, api_key=None, testing=False) -> None:
        self.testing = testing
        if not testing:
            GeminiFlash.initialize_model(api_key)
            self.llm = genai.GenerativeModel(model_name=GeminiFlash.model_name,
                                    generation_config=self.generation_config,
                                    system_instruction=TRIP_CHECKLIST_EXPERT)
    
    def generate_trip_checklist(self, item_repository, user_preferences, trip_prompt):
        if not self.testing:
            llm_prompt = trip_prompt + "\nItem Repository\n" + "\n".join(item_repository) + "\n\nUser Preferences\n" + "\n".join(user_preferences)
            print(llm_prompt)
            self.generation = self.llm.generate_content([llm_prompt])
            print(self.generation.text)
            self.generation = get_json_from_generation(self.generation.text)
            return self.generation
        else:
            self.generation = json.loads(TEST_TRIP_CHECKLIST)
            return self.generation

class ProductImageToMetadataExpert(GeminiFlash):
    generation_config = {
            "temperature": 0,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "application/json",
        }
    generation = None
    testing = False # Returns a default JSON Response.
    
    def __init__(self, api_key=None, testing=False) -> None:
        self.testing = testing
        if not testing:
            GeminiFlash.initialize_model(api_key)
            self.llm = genai.GenerativeModel(model_name=GeminiFlash.model_name,
                                generation_config=self.generation_config,
                                system_instruction=PRODUCT_IMAGE_TO_METADATA_EXPERT)
    
    def generate_product_metadata(self, image_paths = []):
        if not self.testing:
            uploaded_images = []
            for image_path in image_paths:
                uploaded_images.append(
                    BaseLLM.upload_to_gemini(image_path,
                                            display_name=image_path))
            BaseLLM.wait_for_files(uploaded_images)

            uploaded_files_with_paths = []
            for image_path, uploaded_image in zip(image_paths, uploaded_images):
                uploaded_files_with_paths.append(image_path)
                uploaded_files_with_paths.append(genai.get_file(name=uploaded_image.name))
            
            self.generation = self.llm.generate_content(uploaded_files_with_paths)
            self.generation = get_json_from_generation(self.generation.text)
            print(self.generation)
            return self.generation
        else:
            self.generation = json.loads(TEST_PRODUCT_METADATA)
            return self.generation