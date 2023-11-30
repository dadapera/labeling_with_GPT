from openai import OpenAI
from dotenv import load_dotenv
from data_manager import load_data, save_df_as_csv, append_df_to_csv
from prompt import get_prompt
import pandas as pd
import json
import os

load_dotenv()
client = OpenAI()

system_prompt = get_prompt()

source_csv = "data/source_set.csv"
result_csv = "data/result_set12.csv"
chunk_size = 2

csv_reader = load_data(source_csv, chunk_size)

print("[*] JOB STARTED.")
for i, chunk in enumerate(csv_reader):
  print(f"Processing Chunk {i + 1}")

  chunk_clean = chunk.drop(columns=["source","packagePrice","basePrice","price","image","code"])
  chunk['query_text'] = chunk_clean.apply(lambda row: '/'.join(map(str, row)), axis=1)
  
  user_prompt = f"Products to be labeled:\n{chunk['query_text']}"

  response = client.chat.completions.create(
      seed=69,  
      temperature=0.2,
      model="gpt-4-1106-preview",
      response_format={ "type": "json_object" },
      messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
      ]
  )
  
  print("Generated.")
  labels_json = json.loads(response.choices[0].message.content)["products"]
  labels_df = pd.DataFrame(labels_json).set_index('product_id')
  chunk['labels'] = labels_df['labels']
  
  # Check if the .cvs file exists
  if os.path.isfile(result_csv):
    # If the file exists, append the new DataFrame to it
    append_df_to_csv(chunk, result_csv)
    print("Appended.")
  else:
    # If the file doesn't exist, save the new DataFrame to it
    save_df_as_csv(chunk, result_csv)
    print("Saved.")

print("[*] JOB ENDED.")
