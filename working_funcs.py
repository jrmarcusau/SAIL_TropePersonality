### SCRIPT FOR SMALL FUNCTIONALITIES: MERGING, VIEWING, COUNTING ###

import pandas as pd
import glob
import re
import bs4 as BeautifulSoup
import ast
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def merge_all_remdup():
    # Get a list of all csv files
    csv_files = glob.glob('deepscrape_v2_*.csv')

    # Initialize an empty list to store individual dataframes
    df_list = []

    # Loop through the csv files and append each one to the df_list
    for filename in csv_files:
        df = pd.read_csv(filename)
        df_list.append(df)

    # Concatenate all the dataframes in the list
    df = pd.concat(df_list, ignore_index=True)

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Save the final dataframe
    df.to_csv("deepscrape_v2_all.csv", index=False)

def merge_all_nodup():
    base = "tropes_personality_merge_"
    csv_files = ["1000", "2000", "3000", "4000", "5000", "6000"]
    csv_files = glob.glob('tropes_personality_merge_*.csv')
    
    df_list = []
    for f in csv_files:
        df = pd.read_csv(f)
        #df = pd.read_csv(base + f + ".csv")
        df_list.append(df)
    
    df = pd.concat(df_list, ignore_index=True)
    df.to_csv(base +  "all.csv")


def split_nodata():
    df = pd.read_csv("deepscrape_all.csv")

    #Create mask where 'mbti_vote' is null
    mask_missing = df['mbti_vote'].isnull()

    # Create mask where 'mbti_vote' is not null
    mask_not_missing = df['mbti_vote'].notnull()

    # Apply masks to create new dataframes
    df_missing = df[mask_missing]
    df_not_missing = df[mask_not_missing]

    # Save the new dataframes to csv
    df_missing.to_csv('deepscrape_all_nodata.csv', index=False)
    df_not_missing.to_csv('deepscrape_all_gooddata.csv', index=False)

def count_mbti(threshold):
    df = pd.read_csv("deepscrape_all_gooddata.csv")
    counter = 0
    for index, row in df.iterrows():
        votes = int(re.search('\d+', row['mbti_count']).group())
        if votes >= threshold:
            counter += 1
    return counter

def merge_last_set():
    df_remain = pd.read_csv("deepscrape_remaining.csv")
    df_good = pd.read_csv("deepscrape_all_gooddata.csv")
    df_list = [df_good, df_remain]
    df_all_updated = pd.concat(df_list, ignore_index=True)
    df_all_updated.to_csv('deepscrape_all.csv', index=False)

def countStuff():
    df = pd.read_csv("tropes_personality_merge_nodup.csv")
    print(len(df))
    

def checkExistence():
    df = pd.read_csv("tropes_deepscrape_all.csv", nrows=1)
    d = df['source'].iloc[0]
    print(d)
    st = str(d)
    print(st)
    print(type(st))
    print(df['text'])
    if "squatter" in d:
        print("good test")
    if "Aaron" in d:
        print("yes")

def tropes_advancedcount():
    overflows = 0
    noexamples = 0
    regular = 0

    df = pd.read_csv("tropes_examples_v2_all.csv")
    print("done loading")
    for index, row in df.iterrows():
        try:
            example = ast.literal_eval(row['examples'])
            if example == []:
                noexamples += 1
            elif example[0]['movie'] == "OVERFLOW":
                overflows += 1
            else:
                regular += 1
        except Exception as e:
            print(e)
            print(index)
    print("noexamples: " + str(noexamples))
    print("overflows: " + str(overflows))
    print("regular: " + str(regular))

def fixit():
    df = pd.read_csv("tropes_examples_all.csv")
    print("done loading")
    for index, row in df.iterrows():
        example = ast.literal_eval(row['examples'])
        if example == 0:
            df.at[index, 'examples'] = []
    df.to_csv("tropes_examples_all_v2.csv", index=False)

def dropcols():
    df = pd.read_csv("mbti_added_all.csv")

    print("done loading")
    df = df[['character','movie','mbti','href','year','notes','id','esfp','esfj','estp','estj','enfp','enfj','entp','entj','isfp','isfj','istp','istj','infp','infj','intp','intj','xxxx']]
    df.to_csv("personality_mbti_all.csv", index=False)

def to_json():
    df = pd.read_csv("tropes_examples_all.csv")
    df['examples'] = df['examples'].apply(ast.literal_eval)
    df.to_json('tropes_examples_all.json', orient='records', lines=True)

def expand_df():
    old_df = pd.read_csv("tropes_characters_v3_all.csv")
    print("done loading")
    fin_list = []
    for index, row in old_df.iterrows():
        print("row: " + str(index) + ", " + row['text'])
        examples = ast.literal_eval(row['examples'])
        for ex in examples:
            new_row = row[['text', 'href']].to_dict()
            new_row.update({'example': ex})
            fin_list.append(new_row)
    new_df = pd.DataFrame(fin_list)
    new_df.to_csv("tropes_characters_split.csv", index=False)



def split_2():
    old_df = pd.read_csv("tropes_characters_split.csv")
    print("done loading")
    fin_list = []
    for index, row in old_df.iterrows():
        print("row: " + str(index) + ", " + row['trope'])
        example = ast.literal_eval(row['example'])
        new_dict = {'trope' : row['trope'], 'link': row['link'], 'movie': example['movie'], 'href': example['href'], 'text': example['text']}
        fin_list.append(new_dict)
    new_df = pd.DataFrame(fin_list)
    #new_df.to_csv("tropes_characters_split_v2.csv", index=False)

#helper
def clean_character(character_str):
    # Replace problematic quotes within a character string
    return character_str.replace('""', "'").replace('"', "'")

#helper
def clean_characters(characters_list):
    # Clean each character string in the list
    return [clean_character(char) for char in characters_list]

def split_character():
    old_df = pd.read_csv("tropes_characters_split.csv")
    print("done loading")
    fin_list = []
    for index, row in old_df.iterrows():
        print("row: " + str(index) + ", " + row['trope'])
        example = ast.literal_eval(row['example'])
        characters = clean_characters(example['characters'])
        
        for character in characters:
            new_dict = {'trope': row['trope'], 'link': row['link'], 'movie': example['movie'], 'href': example['href'], 'text': example['text'], 'character': character}
            fin_list.append(new_dict)
    
    new_df = pd.DataFrame(fin_list)
    new_df.to_csv("tropes_characters_split_character.csv", index=False)
            
def filter_movies():
    old_df = pd.read_csv("tropes_characters_split_char.csv")
    movies = pd.read_csv("matchedmovie.csv")
    old_df['movie'] = old_df['movie'].str.lower()
    movies['movie'] = movies['movie'].str.lower()

    movies_list = movies['movie'].tolist()
    print("done loading")

    mask = old_df['movie'].isin(movies_list)

    filtered_df = old_df[mask]
    filtered_df.to_csv("tropes_characters_split_filter.csv", index=False)
        

def dropdup():
    old_df = pd.read_csv("tropes_personality_merge_all.csv")
    print("done loading")
    new_df = old_df.drop_duplicates(subset=['character'])
    new_df.to_csv("tropes_personality_merge_nodup.csv", index=False)

def merge_movie():
    # Example DataFrames
    personality_df = pd.read_csv("tropes_characters_split_nodup.csv")
    tropes_df = pd.read_csv("personality_mbti_nodup.csv")

    # Convert 'movie' column in both dataframes to lowercase (or uppercase)
    personality_df['movie'] = personality_df['movie'].str.lower()
    tropes_df['movie'] = tropes_df['movie'].str.lower()

    # File 1: Correctly Joined Ones
    matchmovie_df = pd.merge(personality_df[['movie']], tropes_df[['movie']], on='movie', how='inner')

    # Save the result to a CSV file
    matchmovie_df.to_csv('matchedmovie.csv', index=False)


def fuzzy_duplicate_removal(df, character_column_name, movie_column_name, threshold=70, proximity=5):
    indices_to_drop = set()

    # Iterate over each item in the DataFrame
    for i in range(len(df)):
        print(i)
        if i in indices_to_drop:
            continue

        # Get the current movie name and character string
        current_movie = df.iloc[i][movie_column_name].lower()
        current_character = df.iloc[i][character_column_name].lower()

        # Only compare with rows within the specified proximity
        for j in range(i+1, min(i+1+proximity, len(df))):
            comparison_movie = df.iloc[j][movie_column_name].lower()
            comparison_character = df.iloc[j][character_column_name].lower()

            # Continue only if movie names are the same
            if current_movie == comparison_movie:
                # Calculate the similarity ratio
                similarity_ratio = fuzz.partial_ratio(current_character, comparison_character)

                # Mark for dropping if the similarity is above the threshold
                if similarity_ratio >= threshold:
                    indices_to_drop.add(j)

    # Drop the duplicates based on the collected indices
    df = df.drop(index=indices_to_drop)

    return df

def remove_duplicates():
    df = pd.read_csv("tropes_characters_split_filter.csv")
    print("Original DataFrame size:", df.shape)
    df_no_duplicates = fuzzy_duplicate_removal(df, "character", "movie")

    df_no_duplicates.to_csv("tropes_characters_split_fuzzynodup", index=False)
    print("DataFrame size after fuzzy duplicate removal:", df_no_duplicates.shape)

def merge_personality_and_trope():
    start = 0
    end = 2000
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





#dropdup()

#expand_df()

#split_nodata()

#print(count_mbti(10))

#merge_last_set()

#split_2()

#split_character()

#merge_movie()

#filter_movies()
dropdup()

countStuff()

#merge_all_nodup()

#tropes_advancedcount()

#dropcols()

#to_json()

#fixit()

#checkExistence()

#remove_duplicates()

#merge_personality_and_trope()
