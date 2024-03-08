import os
import json
import csv
import numpy as np
from bs4 import BeautifulSoup

story_json_path = "story/story.json"
output_csv_path = "story/story.csv"
new_line_char = "$"

def html_to_text(html):
    soup = BeautifulSoup(html, features="html.parser")
    return soup.get_text(new_line_char)

random = np.random.default_rng(31)

with open(story_json_path) as fp:
    story = json.loads(fp.read())

sequences = story["sequences"]
num_sequences = len(sequences)
shuffled_pages = 2 + random.permutation(num_sequences-1) # We start at 1 and exclude the first page from the shuffling
page_numbers = np.insert(shuffled_pages, 0, 1)

# Map sequence ids to their page number
sequence_id_to_page_number = {}
for idx, sequence in enumerate(sequences):
    sequence_id_to_page_number[sequence["id"]] = page_numbers[idx]

# Sort sequences by page
decorated = [(page_numbers[idx], sequence) for idx, sequence in enumerate(sequences)]
decorated.sort()
sorted_sequences = [sequence for (_, sequence) in decorated]

# Write 1 row in output csv file for each sequence
with open(output_csv_path, 'w', encoding="utf-8", newline='') as output_csv:
    csv_writer = csv.writer(output_csv, delimiter=';')
    csv_writer.writerow(["@image", "description", "next_sequence_text", "choices_text"])

    for idx, sequence in enumerate(sorted_sequences):
        # page_number = idx + 1
        image_path = f".\images\{sequence['id']}.jpg"
        if not os.path.exists(image_path):
            print(f"Error: {image_path} was not found!")
            image_path = ""
        description = html_to_text(sequence["content"])
        next_sequence_text = ""
        choices_text = ""

        if "next" in sequence and sequence["next"] is not None and sequence["next"] != "null":
            next_sequence_page_number = sequence_id_to_page_number[sequence["next"]]
            next_sequence_text = f"Aller à la page {next_sequence_page_number}"

        elif sequence["choices"] != []:
            for choice in sequence["choices"]:
                choice_page_number = sequence_id_to_page_number[choice["next"]]
                choices_text += html_to_text(choice["content"]) + " : "\
                    + f"Aller à la page {choice_page_number}"\
                    + new_line_char
        elif "isHappyEnd" in sequence:
            # Action on finding en ending?
            print(f"{sequence['id']} was correctly tagged as ending")
        else:
            print(f"Error: neither 'next' or 'choices' non-empty fields were found for current sequence {sequence['id']}")

        csv_writer.writerow([image_path, description, next_sequence_text, choices_text])




