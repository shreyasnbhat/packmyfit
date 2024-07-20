import pandas as pd

def csv_to_dict(csv_file):
  """Reads a CSV file and converts it to JSON.

  Args:
    csv_file: The path to the CSV file.

  Returns:
    A JSON string representing the CSV data.
  """

  df = pd.read_csv(csv_file)
  item_repository = {}
  for category in df.groupby('Category'):
    item_repository[category[0]] = category[1][['Name', 'Brand', 'Colors', 'Quantity', 'Comments', 'Link']].to_dict('records')

  return item_repository
