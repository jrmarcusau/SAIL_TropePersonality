
import pandas as pd
import glob
import re
import bs4 as BeautifulSoup
import ast
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def merge_personality_and_trope():
    start = 4000
    end = 6000
    # Load the personality and trope datasets
    personality_df = pd.read_csv("personality_mbti_all.csv")
    trope_df = pd.read_csv("tropes_chars_split_fuzzynodup.csv")

    # Initialize an empty list to store merged rows
    merged_rows = []

    # Iterate through character names in the personality database
    for index, row in personality_df[start:end].iterrows():
        print("row: " + str(index))
        character_name = row["character"]
        
        # Use fuzzywuzzy's process.extract to find all matches and scores
        matches = process.extract(character_name, trope_df["character"], scorer=fuzz.partial_ratio)
        
        # Filter matches with a score >= 70
        good_matches = [match for match in matches if match[1] >= 70]
        
        if good_matches:
            # Create a DataFrame for the personality row
            personality_row = pd.DataFrame([row] * len(good_matches))
            
            # Create a DataFrame for the matched trope rows
            trope_rows = trope_df[trope_df["character"].isin([match[0] for match in good_matches])]

            # Merge the personality and trope DataFrames
            merged_df = pd.concat([personality_row.reset_index(drop=True), trope_rows.reset_index(drop=True)], axis=1)

            # Append the merged rows to the list
            merged_rows.append(merged_df)

    # Concatenate all merged rows into the final DataFrame
    final_merged_df = pd.concat(merged_rows, ignore_index=True)

    # Save the final merged DataFrame to a CSV file
    filename = "tropes_personality_merge_" + str(end) + ".csv"
    final_merged_df.to_csv(filename, index=False)
    print("DataFrame size after fuzzy merge:", final_merged_df.shape)


merge_personality_and_trope()