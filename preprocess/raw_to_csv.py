import os
import csv
from collections import defaultdict

from utils import parse

# Define the path to the input directory containing the txt files
input_directory = "raw_data"

# Define the path to the output directory where the csv files will be stored
output_directory = "source_data"

# Define a list of potential skill keywords
skill_keywords = ["data pipelines", "etl", "data warehouse", "data modeling", "GCP", "SQL", "MySQL", "PostgreSQL", "pandas"]

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Create a dictionary to store job data by date
jobs_by_date = defaultdict(list)

# Iterate through all txt files in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith(".tmp"):
        # print(f"Processing {filename}...")

        # todo parse file name
        job_title, company, date_str, time_str = parse.get_filename_data(filename)
        datetime_str = f"{date_str} {time_str}"

        # Read job description from file
        with open(os.path.join(input_directory, filename), 'r') as f:
            job_description = f.read().lower()

        # Extract up to 10 skill keywords from job description
        skills_found = []
        for skill in skill_keywords:
            skill = skill.lower()
            if skill in job_description and len(skills_found) < 10:
                skills_found.append(skill)

        if len(skills_found) == 0:
            # print(f"No relevant skills found in {filename}, skipping...")
            continue

        # Pad the skills list to 10 elements with empty strings if necessary
        skills_found += [''] * (10 - len(skills_found))
        # interest_score = round(len(skill_keywords) / len(skills_found))
        #
        # # Ensure the score is at least 1 if there is at least one skill matched
        # final_score = max(1, interest_score) if len(skills_found) > 0 else 0

        # Append the job data to the dictionary
        print(f"Job title: {job_title}, skills found: {', '.join(skills_found)}")
        jobs_by_date[date_str].append([datetime_str, job_title, company] + skills_found) #  + [str(final_score)])

# Write the data to CSV files, one per date
for date, jobs in jobs_by_date.items():
    output_filename = os.path.join(output_directory, f"{date}.csv")
    with open(output_filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['DateTime', 'JobTitle', 'Company', 'Skill1', 'Skill2', 'Skill3', 'Skill4', 'Skill5', 'Skill6', 'Skill7', 'Skill8', 'Skill9', 'Skill10']) # , 'InterestScore'])
        for job in jobs:
            csv_writer.writerow(job)

print(f"Job descriptions processed and CSV files created in {output_directory}.")
