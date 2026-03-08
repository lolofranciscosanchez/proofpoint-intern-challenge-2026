# Proofpoint Technical Challenge - Intern Program 2026

This repository contains the source code and data files for the Technical Challenge as part of the Proofpoint Intern Program 2026 selection process. The repository includes solutions for the Data Cleaning (Streaming Catalog) and the Word Frequency Analysis exercises.

## 📂 Project Structure

- `process_episodes.py`: Main Python script for parsing, cleaning, and deduplicating the streaming catalog.
- `episodes_raw.csv`: Mock input dataset containing missing values, invalid formats, and duplicates.
- `episodes_clean.csv`: Final output dataset with all corrections and deduplication rules applied.
- `report.md`: Data quality report detailing metrics and the connected-components deduplication strategy.
- `word_frequency.py`: Python script for calculating word frequency in a text file, ignoring punctuation and case.
- `sample_text.txt`: Sample text file used to test the word frequency script.

## ⚙️ Installation & Setup

Before running the data processing script, you must install the required dependencies. The main challenge utilizes the `pandas` library for data manipulation. 

Please run the following command in your terminal to install it:
pip install pandas


## 🚀 How to Run

Part B: The Streaming Service's Lost Episodes
To execute the data cleaning and deduplication process:
cd part_b_catalog
python process_episodes.py

This will read episodes_raw.csv and generate both episodes_clean.csv and report.md in the root directory.

Part C: Word Frequency Analysis
To execute the word frequency analyzer, pass the target text file as an argument:
cd part_c_frequency
python word_frequency.py sample_text.txt

This will output the top 10 most frequent words directly to the console.

🧑‍💻 Author
Francisco Sánchez

- LinkedIn: https://www.linkedin.com/in/francisco-sanchez-5b64aa232/

- Email: 11francisco.sanchez@gmail.com
