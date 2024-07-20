import argparse
import os
import csv
import hashlib
import time
from llms import ProductLinkToMetadataExpert
from constants import GEMINI_API_KEY
from utils import download_webpage

if __name__ == "__main__":
  product_link_to_metadata_expert = ProductLinkToMetadataExpert(api_key=GEMINI_API_KEY)
  parser = argparse.ArgumentParser(description="Download webpages from a CSV file containing URLs of clothing items.")
  parser.add_argument("csv_file", help="Path to the CSV file containing clothing items URLs.")
  args = parser.parse_args()

  url_to_filepath = {}

  with open(args.csv_file, 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header row
    for row in reader:
      url = row[0]  # Assuming the first column is the URL
      print(f"Downloading content for {url} ...")
      content = download_webpage(url=url)

      if content:
        print(f"Downloaded content for {url} successfully!")
        os.makedirs("page_content", exist_ok=True)
        filename = hashlib.sha256(url.encode('utf-8')).hexdigest()
        filepath = os.path.join("page_content", filename)
        with open(filepath, "w") as f:
          f.write(content)
        url_to_filepath[url] = filepath
      else:
        print(f"Failed to download content for {url}.")

  print("URL to Filepath Mapping:")
  # Create a list to store all the headers
  all_headers = []
  # Open the CSV file for writing
  with open("product_metadata.csv", 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=all_headers)
    for url, filepath in url_to_filepath.items():
      print(f"{url} -> {filepath}")
      print("Running Gemini API to fetch product metadata...")
      json_data = ProductLinkToMetadataLLM.generate_product_metadata(filepath)
      print(json_data)

      # Update the headers list
      all_headers.extend(json_data.keys())
      all_headers = list(set(all_headers))  # Remove duplicate headers

      # Write the header row only once
      if not all_headers:
        writer.writeheader()

      # Write the data row
      writer.writerow(json_data)
      time.sleep(5)

    print(f"Product metadata saved to product_metadata.csv")
