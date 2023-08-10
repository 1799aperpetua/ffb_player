# This file is for loading data into my db from Fantasypros.com
# I pulled some datasets, cleaned them up, manipulated them a bit; got it in the format I want
import pandas as pd
from app import get_db_connection
import sqlite3

# = - Load Teams Data - ==============================================================================================
LOAD_TEAMS_QUERY = '''
        INSERT INTO Teams (team_id, team_name, team_abbreviation)
        VALUES (?, ?, ?)
        '''
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

# loadTeams(LOAD_TEAMS_QUERY)# - COMPLETE: Teams and their abbreviations are in the database
# = - END - ==========================================================================================================

# = - UPDATE Players: Add Column - ===================================================================================
# Add a column to Players so that we can map team abbreviations to eachother and update team_id on each player
UPDATE_PLAYER_SCHEMA_Q = "ALTER TABLE Players ADD COLUMN team_abbrev VARCHAR(255);"
def updatePlayerSchema(query):
    conn = get_db_connection()
    try:
        conn.execute(query)
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        return print("Could not execute query\n", e)
    else:
        return print("Successfully altered your Players table to add a team_abbreviation column")
    
# updatePlayerSchema(UPDATE_PLAYER_SCHEMA_Q)# - COMPLETE: team_abbrev Column has been added to Players
# = - END - ==========================================================================================================

# = - Load Players Data - ============================================================================================
LOAD_PLAYER_DATA_Q = '''
                INSERT INTO Players (player_id, player_name, position, position_tier, position_rank, overall_rank, adp, bye_week, team_abbrev)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                '''
def loadPlayerData(query):
    # Load our dataframe
    df = pd.read_csv('datasets/playerData.csv', index_col=False)
    # Connect to our database
    conn = get_db_connection()
    # Loop through each row in our dataset
    for idx, row in df.iterrows():
        data = (
            None,
            row['player_name'],
            row['position'],
            row['position_tier'],
            row['position_rank'],
            row['overall_rank'],
            row['adp'],
            row['bye_week'],
            row['team_abbreviation'],
        )
        try:
            conn.execute(query, data)
            conn.commit()
        except sqlite3.Error as e:
            print("Could not accept query\n", e)
        else:
            print("Query submitted successfully")
    
    conn.close()
        
#loadPlayerData(LOAD_PLAYER_DATA_Q)# - COMPLETE: Player data has been loaded into the DB
# = - END - ==========================================================================================================

# = - Load Players Data - ============================================================================================
UPDATE_PLAYERS_TEAMID_Q = '''
                UPDATE Players SET team_id = (
                SELECT team_id FROM Teams WHERE Players.team_abbrev = Teams.team_abbreviation);
                '''
def updatePlayersTeamId(query):
    conn = get_db_connection()
    try:
        conn.execute(query)
        conn.commit()
    except sqlite3.Error as e:
        return print("Could not execute query\n", e)
    else:
        return print("Query executed successfully!")

#updatePlayersTeamId(UPDATE_PLAYERS_TEAMID_Q)# - COMPLETE: Players have had their team_id's added
# = - END - ==========================================================================================================