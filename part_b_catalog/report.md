# Data Quality Report

- **Total input records**: 30
- **Total output records**: 23
- **Number of discarded entries**: 2
- **Number of corrected entries**: 15
- **Number of duplicates detected**: 5

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
