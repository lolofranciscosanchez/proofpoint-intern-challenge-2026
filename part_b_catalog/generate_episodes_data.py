import pandas as pd
import random
import numpy as np

def generate_data():
    # Set a fixed seed for reproducibility
    random.seed(42)
    np.random.seed(42)

    columns = ['Series Name', 'Season Number', 'Episode Number', 'Episode Title', 'Air Date']
    data = []

    # 1. Missing fields
    data.append(["", "1", "1", "Pilot", "2023-01-01"]) # Empty Series Name
    data.append(["Missing Season Show", "", "2", "Episode 2", "2023-01-08"]) # Missing Season/Empty Season
    data.append(["Missing Episode Show", "1", "", "Episode 3", "2023-01-15"]) # Missing Episode Number
    data.append(["Empty Title Show", "1", "4", "", "2023-01-22"]) # Empty Episode Title
    data.append(["Missing Date Show", "1", "5", "Episode 5", ""]) # Missing Air Date
    data.append(["All Missing Show", "2", "", "", ""]) # Episode Num, Title, and Air Date all missing

    # 2. Invalid formats
    # Non-numeric in Season/Episode
    data.append(["Format Show", "one", "1", "Text Season", "2023-02-01"])
    data.append(["Format Show", "3.5", "2", "Float Season", "2023-02-08"])
    data.append(["Format Show", "--2", "3", "Negative Season", "2023-02-15"])
    data.append(["Format Show", "1", "one", "Text Episode", "2023-02-22"])
    data.append(["Format Show", "1", "3.5", "Float Episode", "2023-03-01"])
    data.append(["Format Show", "1", "--2", "Negative Episode", "2023-03-08"])

    # Impossible dates
    data.append(["Bad Dates Show", "1", "1", "Not a Date", "not a date"])
    data.append(["Bad Dates Show", "1", "2", "Impossible Date 1", "2022-40-99"])
    data.append(["Bad Dates Show", "1", "3", "Impossible Date 2", "0000-00-00"])

    # Whitespace and inconsistent capitalization
    data.append(["  Whitespace Show  ", " 1 ", " 1 ", "   Trim Me   ", " 2023-04-01 "]) # Extra whitespace
    data.append(["cApItAlIzAtIoN TeSt", "1", "2", "sOmE tItLe", "2023-04-08"]) # Inconsistent caps

    # 3. Duplicates
    # Pair 1: (SeriesName_normalized, SeasonNumber, EpisodeNumber)
    # High quality row
    data.append(["Duplicate Show A", "1", "10", "The Real Pilot", "2023-05-01"])
    # Low quality row (Unknown date, Untitled Episode)
    data.append(["duplicate show a", "1", "10", "Untitled Episode", "Unknown"])

    # Pair 2: (SeriesName_normalized, 0, EpisodeNumber, EpisodeTitle_normalized)
    # High quality row
    data.append(["Duplicate Show B", "0", "5", "The Special Episode", "2023-06-01"])
    # Low quality row (Missing date, lowercase title)
    data.append(["DUPLICATE SHOW B", "0", "5", "the special episode", ""])

    # Pair 3: (SeriesName_normalized, SeasonNumber, 0, EpisodeTitle_normalized)
    # High quality row
    data.append(["Duplicate Show C", "2", "0", "The Finale Crossover", "2023-07-01"])
    # Low quality row (Invalid date, extra whitespace)
    data.append(["  duplicate show c  ", "2", "0", "the finale crossover", "not a date"])

    # 4. Normal/Filler rows to reach exactly 30 rows
    base_series = ["The Great Show", "Mystery Chronicles", "Comedy Central"]
    base_dates = ["2023-01-15", "2023-02-20", "2023-03-10", "2023-04-25"]
    for i in range(7):
        series = random.choice(base_series)
        season = str(random.randint(1, 5))
        episode = str(random.randint(1, 20))
        title = f"Random Episode {episode}"
        date = random.choice(base_dates)
        data.append([series, season, episode, title, date])

    df = pd.DataFrame(data, columns=columns)
    
    # Save to CSV
    output_filename = "episodes_raw.csv"
    df.to_csv(output_filename, index=False)
    print(f"Successfully generated '{output_filename}' with {len(df)} rows.")

if __name__ == "__main__":
    generate_data()
