'''
Need to write a script to write in all of the players from ESPN's database
Probably just use pandas and add some columns for the data that I want, that they don't have
Might be able to find some other data sets to append onto each person's record in the db
'''

from flask import Flask, render_template
from sqlite3 import connect
import os

def setupDbConnection():
    # Connect to a SQL Database
    db = os.getcwd() + '/player.db'
    try:
        cursor = connect(db) # Create a cursor for interacting with the database we've connected to
    except:
        print("Failed to connect to database")
        return False
    else:
        return cursor

def BuildTables(cursor, query):
    if cursor is False: # Indicator: Failed to connect to the database
        print("Could not connect to database.  Abandoning query")
        return
    
    try:
        cursor.execute(query)
    except:
        print("Failed to execute the query")
        return
    else:
        print("Successfully submitted query to the databse")

# Build tables - Would be nice to have opportunity and efficiency metrics, I'm sure that's easy data to capture.  Rankings from last year would be nice too.  Make a separate table?
CREATE_PLAYERS_TABLE_QUERY = '''
CREATE TABLE Players (
player_id INT PRIMARY KEY,
name VARCHAR(255),
position_tier INT,
position_rank INT,
overall_rank INT,
adp INT,
team_id INT,
injury_info TEXT,
FOREIGN KEY (team_id) REFERENCES Teams(team_id)
)
'''

CREATE_TEAMS_TABLE_QUERY = '''
CREATE TABLE Teams (
team_id INT PRIMARY KEY,
name TEXT,
improvements TEXT,
disimprovements TEXT
)
'''

CREATE_NOTES_TABLE_QUERY = '''
CREATE TABLE Notes (
note_id INT PRIMARY KEY,
player_id INT,
note_type VARCHAR(255),
note_content TEXT,
FOREIGN KEY (player_id) REFERENCES Players(player_id)
)
'''

#BuildTables(setupDbConnection(), CREATE_PLAYERS_TABLE_QUERY)
#BuildTables(setupDbConnection(), CREATE_TEAMS_TABLE_QUERY)
#BuildTables(setupDbConnection(), CREATE_NOTES_TABLE_QUERY)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Create player


# Read player


# Update player


# Delete player(s)


# Queries