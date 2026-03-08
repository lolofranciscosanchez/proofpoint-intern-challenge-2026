import pandas as pd
import numpy as np
import re

def normalize_string(x):
    if pd.isna(x):
        return ""
    s = str(x).strip()
    # collapse multiple spaces into one
    s = re.sub(r'\s+', ' ', s)
    return s.lower()

def get_norm_num(x):
    if pd.isna(x):
        return 0
    s = str(x).strip()
    if not s:
        return 0
    try:
        val = float(s)
        if pd.isna(val):
            return 0
        if not val.is_integer() and val != 0:
            return 0
        val = int(val)
        return val if val >= 0 else 0
    except ValueError:
        return 0

def clean_data():
    raw_csv = 'episodes_raw.csv'
    df = pd.read_csv(raw_csv)
    initial_count = len(df)
    
    # Keep a copy of the raw dataframe to compare for corrections
    df_raw = df.copy()

    # 1. Data Cleaning & Defaults

    # Discard if 'Series Name' is missing or empty
    def is_empty_series(x):
        if pd.isna(x):
            return True
        return str(x).strip() == ""
    
    mask_keep_series = ~df['Series Name'].apply(is_empty_series)
    df = df[mask_keep_series].copy()
    
    def process_row(row):
        new_row = row.copy()
        
        # Season Number
        s_season = str(row['Season Number']).strip() if pd.notna(row['Season Number']) else ""
        if not s_season:
            new_row['Season Number'] = 0
        else:
            try:
                val = float(s_season)
                if not val.is_integer() and val != 0:
                    new_row['Season Number'] = 0
                else:
                    if int(val) < 0:
                        new_row['Season Number'] = 0
            except ValueError:
                new_row['Season Number'] = 0
                
        # Episode Number
        s_ep = str(row['Episode Number']).strip() if pd.notna(row['Episode Number']) else ""
        if not s_ep:
            new_row['Episode Number'] = 0
        else:
            try:
                val = float(s_ep)
                if not val.is_integer() and val != 0:
                    new_row['Episode Number'] = 0
                else:
                    if int(val) < 0:
                        new_row['Episode Number'] = 0
            except ValueError:
                new_row['Episode Number'] = 0
                
        # Episode Title
        s_title = str(row['Episode Title']).strip() if pd.notna(row['Episode Title']) else ""
        if not s_title:
            new_row['Episode Title'] = 'Untitled Episode'
            
        # Air Date
        s_date = str(row['Air Date']).strip() if pd.notna(row['Air Date']) else ""
        if not s_date:
            new_row['Air Date'] = 'Unknown'
        else:
            try:
                pd.to_datetime(s_date, format='mixed', errors='raise')
            except (ValueError, TypeError, OverflowError):
                new_row['Air Date'] = 'Unknown'
                
        return new_row

    # Apply defaults
    df_processed = df.apply(process_row, axis=1)
    
    # Discard if ALL are missing/default simultaneously
    def is_all_missing(row):
        # We check the processed row values, but also use get_norm_num to safely check 0.
        is_ep_0 = (get_norm_num(row['Episode Number']) == 0)
        is_title_missing = (row['Episode Title'] == 'Untitled Episode')
        is_date_missing = (row['Air Date'] == 'Unknown')
        return is_ep_0 and is_title_missing and is_date_missing

    mask_all_missing = df_processed.apply(is_all_missing, axis=1)
    df_processed = df_processed[~mask_all_missing].copy()
    
    discarded_entries = initial_count - len(df_processed)
    
    # Calculate corrected entries
    # A row is 'corrected' if it survived discarding AND any of its fields were changed
    num_corrected = 0
    check_cols = ['Series Name', 'Season Number', 'Episode Number', 'Episode Title', 'Air Date']
    
    for idx in df_processed.index:
        orig = df_raw.loc[idx]
        proc = df_processed.loc[idx]
        changed = False
        for col in check_cols:
            o = orig[col]
            p = proc[col]
            if pd.isna(o) and pd.isna(p):
                continue
            if pd.isna(o) != pd.isna(p):
                changed = True
                break
            if str(o) != str(p):
                changed = True
                break
        if changed:
            num_corrected += 1

    # 2. Normalization for Deduplication
    df_processed['SeriesName_norm'] = df_processed['Series Name'].apply(normalize_string)
    df_processed['EpisodeTitle_norm'] = df_processed['Episode Title'].apply(normalize_string)
    df_processed['Season_norm'] = df_processed['Season Number'].apply(get_norm_num)
    df_processed['Episode_norm'] = df_processed['Episode Number'].apply(get_norm_num)
    
    # Find connected components (duplicates) based on matching any of the three tuples
    indices = df_processed.index.tolist()
    adj = {i: [] for i in indices}
    
    n_rows = len(indices)
    for i in range(n_rows):
        for j in range(i + 1, n_rows):
            idx1 = indices[i]
            idx2 = indices[j]
            r1 = df_processed.loc[idx1]
            r2 = df_processed.loc[idx2]
            
            # Tuple A: (SeriesName_normalized, SeasonNumber, EpisodeNumber)
            t_a1 = (r1['SeriesName_norm'], r1['Season_norm'], r1['Episode_norm'])
            t_a2 = (r2['SeriesName_norm'], r2['Season_norm'], r2['Episode_norm'])
            
            # Tuple B: (SeriesName_normalized, 0, EpisodeNumber, EpisodeTitle_normalized)
            t_b1 = (r1['SeriesName_norm'], 0, r1['Episode_norm'], r1['EpisodeTitle_norm'])
            t_b2 = (r2['SeriesName_norm'], 0, r2['Episode_norm'], r2['EpisodeTitle_norm'])
            
            # Tuple C: (SeriesName_normalized, SeasonNumber, 0, EpisodeTitle_normalized)
            t_c1 = (r1['SeriesName_norm'], r1['Season_norm'], 0, r1['EpisodeTitle_norm'])
            t_c2 = (r2['SeriesName_norm'], r2['Season_norm'], 0, r2['EpisodeTitle_norm'])
            
            if (t_a1 == t_a2) or (t_b1 == t_b2) or (t_c1 == t_c2):
                adj[idx1].append(idx2)
                adj[idx2].append(idx1)
                
    # 3. Deduplication Priority (Tie-breakers)
    duplicates_detected = 0
    keep_indices = []
    
    def get_priority_key(idx):
        row = df_processed.loc[idx]
        is_valid_date = 1 if row['Air Date'] != 'Unknown' else 0
        is_known_title = 1 if row['Episode Title'] != 'Untitled Episode' else 0
        is_valid_numbers = 1 if (row['Season_norm'] != 0 and row['Episode_norm'] != 0) else 0
        # Priority order:
        # 1st: is_valid_date (desc)
        # 2nd: is_known_title (desc)
        # 3rd: is_valid_numbers (desc)
        # 4th: -idx (so smaller index is preferred)
        return (is_valid_date, is_known_title, is_valid_numbers, -idx)

    visited = set()
    for idx in indices:
        if idx not in visited:
            comp_list = []
            stack = [idx]
            visited.add(idx)
            while stack:
                curr = stack.pop()
                comp_list.append(curr)
                for neighbor in adj[curr]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        stack.append(neighbor)
                        
            if len(comp_list) > 1:
                duplicates_detected += (len(comp_list) - 1)
                
            best_idx = max(comp_list, key=get_priority_key)
            keep_indices.append(best_idx)
        
    df_final = df_processed.loc[keep_indices].sort_index()
    
    # 4. Output
    # Drop norm columns
    df_final = df_final[check_cols]
    
    # Export cleaned dataframe
    df_final.to_csv('episodes_clean.csv', index=False)
    
    total_output = len(df_final)
    
    report_content = f"""# Data Quality Report

- **Total input records**: {initial_count}
- **Total output records**: {total_output}
- **Number of discarded entries**: {discarded_entries}
- **Number of corrected entries**: {num_corrected}
- **Number of duplicates detected**: {duplicates_detected}

## Deduplication Strategy
Duplicates were identified by matching grouped rows that shared equivalence on ANY of the following three criteria tuples:
1. `(SeriesName_normalized, SeasonNumber, EpisodeNumber)`
2. `(SeriesName_normalized, 0, EpisodeNumber, EpisodeTitle_normalized)`
3. `(SeriesName_normalized, SeasonNumber, 0, EpisodeTitle_normalized)`

Strings were normalized (trimmed, lowercased, and multiple spaces collapsed) before comparison. The algorithm groups matching rows transitively.

When duplicates were found within these groups, the 'best' record was kept using the exact priority system instructed:
- **1st:** Has a valid Air Date (not 'Unknown')
- **2nd:** Has a known Episode Title (not 'Untitled Episode')
- **3rd:** Has valid Season and Episode Numbers (not 0)
- **4th:** If still tied, the first entry encountered in the file was kept.
"""
    with open('report.md', 'w') as f:
        f.write(report_content)
        
    print(f"Processing complete: Initial {initial_count} -> Output {total_output}. Report saved.")

if __name__ == "__main__":
    clean_data()
