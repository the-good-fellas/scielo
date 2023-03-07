from huggingface_hub import HfApi
import os

path = 'articles'

# filter the list to include only files (not directories)
files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

output_file = "scielo_train.txt"

api = HfApi()

# open the output file for writing
with open(output_file, "w") as f_out:
  # loop through each file and write its contents to the output file
  for i, file_name in enumerate(files):
    with open(os.path.join(path, file_name), "r") as f_in:
      content = f_in.read().strip()
      f_out.write(content)
      f_out.write("\n")
    if (i + 1) % 100 == 0:
      print(f"Processed {i + 1} files")

api.upload_file(
  path_or_fileobj=output_file,
  path_in_repo=output_file,
  repo_type='dataset',
  repo_id="thegoodfellas/scielo-health-ptbr",
)
