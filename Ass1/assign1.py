"""
Raw Data Cleaner for the Olympics Data Base
"""

__author__ = "Minjae Lee, 45363809"


from assign1_utilities import get_column, replace_column, truncate_string

def remove_athlete_id(row) :    # Removes athlete id
    
    """ Remove data in every column 0 (Athlete Identifier) from every row

    Parameters:
        row (str): String of data with comma separators (CSV format).

    Return:
        str: Updated row with blank("")/no data in column 1.
    """
    row = replace_column(row,"", 0)     # First column of data now contain blank ""
    # Column number '0' actually indicates column 1, as according to the property of array
    return row[1:]          # Remove first column of the string altogether

def max_char_30(row):  # Truncates sport, atheletes' first and family name to 30 characters
    
    """ Truncate data in indicated column to 30 characters. 

    Parameters:
        row (str): String of data with comma separators (CSV format).

    Return:
        str: Updated row with truncated data in columns 1 ~ 4.
    """
    for i in range(4):                      
        row_update = get_column(row, i)     # row_update now contain data from row and in the 'i' value of column
        row_updated = truncate_string(row_update, 30)   # Truncates string to 30 characters and stores in row_updated
        row = replace_column(row, row_updated, i)       # Updated data replaces the exisiting data at indicated column in the row  
    return row

def max_char_corrupt(row): # Check maximum character length and corrupts them if exceeded
    
    """ Return a boolean if data at the indicated column in the row is satisfied by a condition.. 

    Parameters:
        row (str): String of data with comma separators (CSV format).

    Return:
        bool: Corrupt is True for 'row' data in the indicated column.
        
    Preconditions:
        corrupt = False
    """
    corrupt = False     # Assign corrupt as a boolean variable
    for i in range (12):    
        if 4 <= i <= 5:                         # For column 5 to 6    
            row_update = get_column(row, i)     # Stores a string from the indicated 'i' value of column of row
            if len(row_update) > 3:             
                corrupt = True                  # Corrupt if the length of the characters in 'row_update' > 3
        elif i == 6 or i == 8:                  # For column 7 or 9
            row_update = get_column(row, i)
            if len(row_update) > 6:             
                corrupt = True                  # Corrupt if length > 6 character limit
        elif i == 7 or i == 9 or i == 10 or i == 11:    # Apply to column 8,10,11,12
            row_update = get_column(row, i)
            if len(row_update) > 8:                     
                corrupt = True                          # Corrupt if length exceeds max 8 char length
    return corrupt

def check_missing_entry(row):   # Corrupt if any missing entries in columns 1 to 5
    
    """ Return a boolean if data at the indicated column in the row is satisfied by a condition..  

    Parameters:
        row (str): String of data with comma separators (CSV format).

    Return:
        bool: Corrupt is True for 'row' data in the indicated column.
        
    Preconditions:
        corrupt = False
    """
    corrupt = False     # Assign corrupt as a boolean variable
    for i in range(5):
        if 0 <= i <= 4:     # Apply to column 1 to 5
            row_update = get_column(row, i) # String containing the data from indicated column
            if row_update == "":        # Corrupt if value is missing/blank
                corrupt = True
    return corrupt

def check_valid_medal(row):     # Check for non-legal values in the Medal column
    
    """ Return a boolean if data at the indicated column in the row is satisfied by a condition.. 

    Parameters:
        row (str): String of data with comma separators (CSV format).

    Return:
        bool: Corrupt is True for 'row' data in the indicated column.
        
    Preconditions:
        corrupt = False
    """
    corrupt = False                     # Assign corrupt as a boolean variable
    row_update = get_column(row, 8)     # Obtain a string from the Medal Column 
    row_updated = row_update.upper()    # Uppercases the string obtained
    # Upper casing all characters in the string is convenient for checking conditions below
    if row_updated == "GOLD" or row_updated == "SILVER" or row_updated == "BRONZE" or row_updated == "":
        pass            
    else:
        corrupt = True
    return corrupt

def fix_medal_letters(row):     # Fix medal name (upper/lower case)

    """ Fix letter casing of valid medal names. 

    Parameters:
        row (str): String of data with comma separators (CSV format).

    Return:
        str: Updated row with correct casing of medal names.
    """
    row_update = get_column(row, 8)             # A new variable store string from the Medal Column
    row_updated = row_update.upper()            # Uppercases the string contained in row_update and stores it in row_updated 
    if row_updated == "GOLD":                   
        row = replace_column(row, "Gold", 8)    # Fix GOLD as Gold in the indicated column in the row
    elif row_updated == "SILVER":       
        row = replace_column(row, "Silver", 8)  # Fix SILVER as Silver
    elif row_updated == "BRONZE":
        row = replace_column(row, "Bronze", 8)  # Fix Bronze as Bronze
    return row
    
def upper_case_country(row):    # Upper cases country code
    """ Upper case all values in the Country Code column. 

    Parameters:
        row (str): String of data with comma separators (CSV format).

    Return:
        str: Updated row with upper casing of country code.
    """
    row_update = get_column(row, 4)             # String from column 4 in the row
    row_updated = row_update.upper()            # Upper cases the string
    row = replace_column(row, row_updated, 4)   # Store updated string in the indicated column in row
    return row

def check_col_6_7_8(row):   # Corrupt if the value stored in column 6 is a whole number and occupied entries in BOTH column 7,8
                           # Also corrupt if no values stored in column 7,8 in row
    """ Return a boolean if data at the indicated column in the row is satisfied by a condition.  

    Parameters:
        row (str): String of data with comma separators (CSV format).

    Return:
        bool: Corrupt is True for 'row' data in the indicated column.
        
    Preconditions:
        corrupt = False
    """
    corrupt = False                     # Assign corrupt as a boolean variable
    row_update = get_column(row, 5)     # Obtain string from column 6 in row
    if row_update.isdigit():            # Determine if the string is a digit
        # Digit indicates a WHOLE number
        if len(get_column(row, 6)) > 0 and len(get_column(row, 7)) > 0: # Check if both column 7,8 store a value
            corrupt = True
        elif len(get_column(row, 6)) == 0 and len(get_column(row, 7)) == 0: # Check if both column 7,8 are empty entries
            corrupt = True
        else:
            pass
        return corrupt

def check_col_9_6(row):                  # Check if the value in column 6 is appropriate to the respective data in column 9
    """ Return a boolean if data at the indicated column in the row is satisfied by a condition.  

    Parameters:
        row (str): String of data with comma separators (CSV format).

    Return:
        bool: Corrupt is True for 'row' data in the indicated column.
        
    Preconditions:
        corrupt = False
    """
    corrupt = False                     # Assign corrupt as a boolean variable
    row_update = get_column(row, 8)     # String from the Medal column
    medal = row_update.upper()          # Variable 'medal' no store the upper cased string
    place = get_column(row, 5)          # Store a value from the Place column in 'place' variable
    if place == "1" and medal != "GOLD":
        corrupt = True                  # Corrupt if 1st place but no GOLD medal
    elif place == "2" and medal != "SILVER":
        corrupt = True                  # Corrupt if 2nd place but no SILVER medal
    elif place == "3"and medal != "BRONZE":
        corrupt = True                  # Corrupt if 3rd place but no BRONZE medal
    return corrupt

def check_world_olympic_record(row):    # Check if the world record corresponds to the olympic record
    """ Return a boolean if data at the indicated column in the row is satisfied by conditions.  

    Parameters:
        row (str): String of data with comma separators (CSV format).

    Return:
        bool: Corrupt is True for 'row' data in the indicated column.
        
    Preconditions:
        corrupt = False
    """
    corrupt = False                         # Assign corrupt as a boolean var
    world_record = get_column(row, 10)      
    olympic_record = get_column(row, 9)
    if len(world_record) > 0:               # If entry is occupied in the world record column
        if world_record != olympic_record:  # Compare world record and olympic record
            corrupt = True                  # Data is corrupt if two records do not match
        return corrupt

def rule_illegal_character(row):    # Check if there are any illegal characters according to format rules
    """ Return a boolean if data at the indicated column in the row is satisfied by conditions.  

    Parameters:
        row (str): String of data with comma separators (CSV format).

    Return:
        bool: Corrupt is True for 'row' data in the indicated column.
        
    Preconditions:
        corrupt = False
    """
    corrupt = False     # Assign Boolean variable
    legal_character = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-'"# Assign a list of legal characters
    row_update = get_column(row, 1)     # String in column 1 in row
    for c in row_update:                # For every character in the string
        if c not in legal_character:    # Check if any of these characters belong to 'legal_character' 
             corrupt = True             # If any character is found to be 'non-legal', data in row is corrupt
    row_update = get_column(row, 2)     # Same rules apply to corresponding columns as above
    for c in row_update:                
        if c not in legal_character:    
            corrupt = True
    row_update = get_column(row, 3)     # Same rules apply to corresponding columns as above
    for c in row_update:
        if c not in legal_character:
            corrupt = True
    row_update = get_column(row, 4)     # Same rules apply to corresponding columns as above
    for c in row_update:
        if c not in legal_character:
            corrupt = True
    return corrupt
    
def rule_place(row):    # Check for any illegal values in the 'Place' column
    """ Return a boolean if data at the indicated column in the row is satisfied by conditions.  

    Parameters:
        row (str): String of data with comma separators (CSV format).

    Return:
        bool: Corrupt is True for 'row' data in the indicated column.
        
    Preconditions:
        corrupt = False
    """
    corrupt = False                 # Assign boolean variable
    row_update = get_column(row, 5) # Store string from the 'Place' column in row_update
    if not row_update.isdigit():    # If the string in row_update is not a digit
            if row_update == "DNS" or row_update == "DNF" or row_update == "PEN" or row_update == "":
                pass                # Strings such as DNS, DNF, PEN are exceptions
            else:
                corrupt = True      # Everything else means corrupted data
            return corrupt
        
def rule_numbers(row):  # Check for any illegal values in the indicated columns
    """ Return a boolean if data at the indicated column in the row is satisfied by conditions.  

    Parameters:
        row (str): String of data with comma separators (CSV format).

    Return:
        bool: Corrupt is True for 'row' data in the indicated column.
        
    Preconditions:
        corrupt = False
    """
    corrupt = False                             # Assign a boolean variable
    legal_number_format = "1234567890.\n"       # List of legal numbers('.' accounts for float)
    # ' \n ' - 'new line' must be assigned to prevent the last column from satisfying the boolean
    
    if len(get_column(row, 6)) > 0:             # When column 7 contain a value
        row_update = get_column(row, 6)         
        for c in row_update:                    # For every character in the string of column 67in row
            if c not in legal_number_format:    # Check for characters that do not belong to legal_number_format
                corrupt = True                  # If illegal, data in row is corrupted
    elif len(get_column(row, 7)) > 0:           #-- Same rules apply as above for column 8
        row_update = get_column(row, 7)         
        for c in row_update:                            
            if c not in legal_number_format:    
                corrupt = True                  
    elif len(get_column(row, 9)) > 0:           #-- Same rules apply as above for column 10
        row_update = get_column(row, 9)         
        for c in row_update:                    
            if c not in legal_number_format:    
                corrupt = True                  
    elif len(get_column(row, 10)) > 0:          #-- Same rules apply as above for column 11
        row_update = get_column(row, 10)        
        for c in row_update:                    
            if c not in legal_number_format:    
                corrupt = True                  
    elif len(get_column(row, 11)) > 0:          #--Same rules apply as above for column 12
        row_update = get_column(row, 11)        
        for c in row_update :                  
            if c not in legal_number_format:
                corrupt = True                  
    return corrupt

def main() :
    """Main functionality of program."""
    with open("athlete_data.csv", "r") as raw_data_file, \
         open("athlete_data_clean.csv", "w") as clean_data_file :
        for row in raw_data_file :
            corrupt = False     # Assignation of the boolean variable, 'corrupt'
            
            # List of functions that check for corrupt data in row
            # 'or' operator used to prevent functions from overwriting each other's boolean outcome
            corrupt = (check_missing_entry(row) or max_char_corrupt(row)
                       or check_valid_medal(row) or check_col_6_7_8(row)
                       or check_col_9_6(row) or check_world_olympic_record(row)
                       or rule_place(row) or rule_illegal_character(row)
                       or rule_numbers(row))
            
            row = max_char_30(row)          # Data in 'row' updated accordingly to max_char_30(row) function
            row = upper_case_country(row)   # Data in 'row' updated accordingly to upper_case_country(row) function
            row = fix_medal_letters(row)    # Data in 'row' updated accordingly to fix_medal_letters(row) function
            row = remove_athlete_id(row)    # Remove Athlete ID from data in row
            
            row_to_process = row    # Saves row in original state, minus athlete id.

            # Save the row data to the cleaned data file.
            if not corrupt :
                clean_data_file.write(row_to_process)
            else :
                row = row[:-1]      # Remove new line character at end of row.
                clean_data_file.write(row + ",CORRUPT\n")    
        

# Call the main() function if this module is executed
if __name__ == "__main__" :
    main()
