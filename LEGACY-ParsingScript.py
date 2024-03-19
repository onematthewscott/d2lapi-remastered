#!/usr/bin/env python 
# Created by: Prof. Dirk Colbry, Matthew Scott Hernandez - EDLI URA.
# Enhanced Digital Learning Initiative, Michigan State University

import pandas as pd
import argparse

def parsedata(filename='ENTER FILENAME HERE', outfile="ENTER OUTFILE PATH HERE"):
    
    """Parse the D2L data and write a single entry per student to a new CSV.

    This function reads the input CSV file, processes the consent for each student,
    and writes the result to a new CSV file.

    Args:
        filename: The path to the CSV file to process.
        outfile: The path to the output CSV file where the results will be saved.
    """
    print(filename)
    df = pd.read_csv(filename)
    # Assume df.columns contains the correct column names.
    df.columns
    
    currentuser = {} # Dictionary to hold the current user's data.
    users = {} # Dictionary to hold the processed user data. 

    for index, row in df.iterrows():

        if type(row['Section #']) == str: # First row of section. Save previous student and start a new one.
            if len(currentuser) > 0:
                if currentuser['id'] in users:
                    if not currentuser['Consent'] == users[currentuser['id']]['Consent']:
                        print(f"REPEAT - WARNING: Student {row['Name']} Consents do not match")
                    else:
                        print(f"REPEAT - Caution: Consent Matches ID")
                    currentuser['Consent'] = currentuser['Consent'] and users[currentuser['id']]['Consent'] # Logical or will always be False if one is False
                else:
                    users[currentuser['id']] = currentuser
                currentuser = {}
            currentuser['Name'] = row['Section #']
            currentuser['Consent'] = False
            currentuser['id'] = ''

        else: # Use if statements to differentiate each row question. 
            if "protect your privacy" in row['Q Text']:
                currentuser['id'] = row['Answer Match']
            if type(row['Answer']) == str:
                if "Yes, I voluntarily" in row['Answer']:
                    if row['# Responses'] == 1.0:
                        # if 1 in both, then default to no - add conflict resolution script here...
                        currentuser['Consent'] = True
    
    
    # Write the results to the outfile.
    new_df = pd.DataFrame.from_dict(users, orient='index')   
    new_df.to_csv(outfile)

    print("Data successfully parsed. Output written to", outfile)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='ISB204_Summary.py',
        description='Converts D2L data to a single entry per student',
        epilog='Contact: herna757@msu.edu for assistance'

    )
    parser.add_argument('filename', help='The filename of the CSV to process') # positional argument - m
    parser.add_argument('-o', '--outfile', help="The filename of the output CSV", default="ENTER OUTFILE PATH HERE")  # option with default value
    parser.add_argument('-v', '--verbose', action='store_true', help="Increase output verbosity")  # on/off flag

    args = parser.parse_args()
    parsedata(args.filename, args.outfile)
    print("Data successfully parsed. Migration successful")

