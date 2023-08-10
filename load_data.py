# This file is for loading data into my db from Fantasypros.com
# I pulled some datasets, cleaned them up, manipulated them a bit; got it in the format I want
import pandas as pd
from app import get_db_connection
import sqlite3

def loadTeams(query):
    
    # Load our CSV into a pandas dataframe so that we can loop through it row by row
    df = pd.read_csv('datasets/teamData.csv')
    # Connect to the database
    conn = get_db_connection()
    # Loop through each row
    for idx, row in df.iterrows():
        # Capture team name and abbreviation - Pass in None as the first arg so that our PK can autoincrement
        data = (None, row["team_name"], row["team_abbreviation"])
        # Run Update Query
        try:
            conn.execute(query, data)
            conn.commit()
        except sqlite3.Error as e:
            print("Could not execute query\n", e)
        else:
            print(f"{row['team_name']} has been enterred into the database")
    
    conn.close()
    return print("loadTeams has finished running.")

# Load Teams
LOAD_TEAMS_QUERY = '''
        INSERT INTO Teams (team_id, team_name, team_abbreviation)
        VALUES (?, ?, ?)
        '''
# loadTeams(LOAD_TEAMS_QUERY)# - COMPLETE: Teams and their abbreviations are in the database

# Load Players
# Will be beneficial to add a field with abbreviation on each player, then I can use that to map team_abbreviations to capture team_id on my players


