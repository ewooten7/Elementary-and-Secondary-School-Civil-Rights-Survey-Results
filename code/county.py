# Install necessary libraries
# pip install pandas openpyxl

import pandas as pd
import re

def clean_value(text, suffix_to_remove):
    """Removes a specific suffix (like 'county' or 'city') and leading/trailing spaces."""
    if not isinstance(text, str):
        return ""
    pattern = r'\s+' + re.escape(suffix_to_remove) + r'$'
    cleaned_text = re.sub(pattern, '', text, flags=re.IGNORECASE).strip()
    return cleaned_text

def normalize_text(text):
    """Converts text to lowercase and removes all spaces for matching."""
    if not isinstance(text, str):
        return ""
    return text.lower().replace(' ', '')

def get_next_state(current_state, states_list):
    """Finds the next state in an alphabetically sorted list."""
    try:
        current_index = states_list.index(current_state)
        if current_index + 1 < len(states_list):
            return states_list[current_index + 1]
    except ValueError:
        return None
    return None

def perform_search(state_to_search, df_ref, norm_city, norm_county):
    """
    Performs a tiered search within a single, specified state.
    Returns (match_series, match_level_string) or (None, "None").
    """
    if not state_to_search:
        return None, "None"
        
    # Rule 3: Check for City + County
    if norm_city and norm_county:
        matches = df_ref[
            (df_ref['state_name'] == state_to_search) & 
            (df_ref['norm_city'] == norm_city) & 
            (df_ref['norm_county'] == norm_county)
        ]
        if not matches.empty:
            return matches.iloc[0], "City and County"
    
    # Rule 4: Check for City only
    if norm_city:
        matches = df_ref[
            (df_ref['state_name'] == state_to_search) & 
            (df_ref['norm_city'] == norm_city)
        ]
        if not matches.empty:
            return matches.sort_values(by='county_name').iloc[0], "City only"
    
    # Rule 5: Check for County only
    if norm_county:
        matches = df_ref[
            (df_ref['state_name'] == state_to_search) & 
            (df_ref['norm_county'] == norm_county)
        ]
        if not matches.empty:
            return matches.sort_values(by='city').iloc[0], "County only"
    
    return None, "None"

# --- 1. Load and Prepare Data ---
print("Loading and preparing data...")
try:
    df_systems = pd.read_csv("systems.csv")
    if 'key' not in df_systems.columns:
        print("Error: The required 'key' column was not found in 'systems.csv'.")
        exit()
except FileNotFoundError:
    print("Error: 'systems.csv' not found. Please place it in the same directory.")
    exit()

try:
    df_cities = pd.read_excel("uscities.xlsx")
except FileNotFoundError:
    print("Error: 'uscities.xlsx' not found. Please place it in the same directory.")
    exit()
    
print("Normalizing reference data for efficient matching...")
df_cities['norm_city'] = df_cities['city'].apply(normalize_text)
df_cities['norm_county'] = df_cities['county_name'].apply(normalize_text)

# Pre-calculate the sorted list of all states
ALL_STATES = sorted(df_cities['state_name'].unique())

# Exclude Hawaii and Puerto Rico
for skip_state in ["Hawaii", "Puerto Rico","District of Columbia"]:
    if skip_state in ALL_STATES:
        ALL_STATES.remove(skip_state)
        print(f"  -> '{skip_state}' will be skipped during processing.")

IMMEDIATE_ITERATOR_STATES = ["District of Columbia"]

# --- 2. Initialize Variables for Processing Loop ---
processed_rows = []
state_iterator = "Alabama"
previous_processed_row = {'key': None, 'System City': '', 'System County': '', 'System State': ''}
previous_raw_row = {'System City': None, 'System County': None, 'System State': None}
consecutive_next_state_count = 0
last_found_city_for_next_state = ""

total_rows = len(df_systems)
print(f"Starting processing of {total_rows} rows...")

# --- 3. Main Processing Loop ---
for index, row in df_systems.iterrows():
    next_state = get_next_state(state_iterator, ALL_STATES)
    print(f"Processing row {index + 1}/{total_rows} (Iterator: {state_iterator}, Checking Next: {next_state or 'N/A'})")
    
    current_raw_row = row.to_dict()
    
    # Rule 8 - Duplicate check
    if (str(current_raw_row.get('System City')) == str(previous_raw_row.get('System City')) and
        str(current_raw_row.get('System County')) == str(previous_raw_row.get('System County')) and
        str(current_raw_row.get('System State')) == str(previous_raw_row.get('System State'))):
        
        copied_row = row.to_dict()
        copied_row.update(previous_processed_row)  # merge matched data (System City/County/State)
        processed_rows.append(copied_row)
        print("  -> Row is a duplicate of previous. Copied result.")
        previous_raw_row = current_raw_row
        continue

    system_city_raw = row.get('System City', '')
    system_county_raw = row.get('System County', '')
    city_cleaned = clean_value(system_city_raw, 'city')
    county_cleaned = clean_value(system_county_raw, 'county')
    norm_city = normalize_text(city_cleaned)
    norm_county = normalize_text(county_cleaned)

    found_match, match_level = perform_search(state_iterator, df_cities, norm_city, norm_county)
    if found_match is None and next_state:
        found_match, match_level = perform_search(next_state, df_cities, norm_city, norm_county)

    final_row = row.to_dict()  # start with all original columns
    was_found = False

    if found_match is not None:
        was_found = True
        final_row.update({
            'System City': system_city_raw if match_level == "County only" else found_match['city'],
            'System County': found_match['county_name'],
            'System State': found_match['state_name']
        })
        print(f"  -> Match found ({match_level}) in '{final_row['System State']}': {final_row['System City']}, {final_row['System County']}")
    else:
        final_row.update({
            'System City': system_city_raw if pd.notna(system_city_raw) else previous_processed_row['System City'],
            'System County': previous_processed_row['System County'],
            'System State': previous_processed_row['System State']
        })
        print(f"  -> No match found. Copying from previous row: {final_row['System County']}, {final_row['System State']}")

    processed_rows.append(final_row)

    # State Iterator Update Logic
    if was_found:
        current_found_state = final_row['System State']
        current_found_city = final_row['System City']
        
        if current_found_state in IMMEDIATE_ITERATOR_STATES and state_iterator != current_found_state:
            print(f"  *** Special case: Match found in '{current_found_state}'. Moving iterator immediately. ***")
            state_iterator = current_found_state
            consecutive_next_state_count = 0
            last_found_city_for_next_state = ""
        else:
            if next_state and current_found_state == next_state:
                if current_found_city != last_found_city_for_next_state:
                    consecutive_next_state_count += 1
                    last_found_city_for_next_state = current_found_city
                
                if consecutive_next_state_count >= 3:
                    print(f"  *** 3 consecutive matches in '{next_state}'. Moving iterator. ***")
                    state_iterator = next_state
                    consecutive_next_state_count = 0
                    last_found_city_for_next_state = ""
            else:
                consecutive_next_state_count = 0
                last_found_city_for_next_state = ""
            
    previous_processed_row = final_row
    previous_raw_row = current_raw_row

# --- 4. Save the Result ---
print("\nProcessing complete. Saving results...")
df_processed = pd.DataFrame(processed_rows)

# ✅ NEW: Save all original columns + updated System City/County/State
df_processed.to_csv("systems1976.csv", index=False)

print("Successfully saved repaired data (all columns) to 'processed.csv'.")
