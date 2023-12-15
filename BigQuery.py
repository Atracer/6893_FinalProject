import os
from google.cloud import bigquery

# Set the environment variable for authentication
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "e6893final-53e7e65dd00e.json"

# Instantiate a BigQuery client
client = bigquery.Client()