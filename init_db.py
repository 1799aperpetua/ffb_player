import os
import sqlite3

# It would also be nice to incorporate efficiency and opportunity metrics for players.  Incorporate this later since stats will vary by position and it might get complicated
# I also want to have stats on teams.  This will accompany the improvements/disimprovements fields that I have on that table

def setupTables():
    db = os.getcwd() + '/player.db'
    try:
        connection = sqlite3.connect(db)
        with open('schema.sql') as f:
            connection.executescript(f.read())

        connection.commit()
        connection.close()
    except:
        print("\n!! Failed to setup database tables !!\n")
        return
    else:
        print("Successfully built tables in the database")
        return
#setupTables()

def setupDbConnection():
    '''
    Helper Function:  Connect to our player database and return a connection object
    '''

    # Connect to a SQL Database
    db = os.getcwd() + '/player.db'
    try:
        connection = sqlite3.connect(db)
    except:
        print("Failed to connect to database")
        return False
    else:
        return connection

def exeQuery(conn, query, data):
    '''
    Function:  Execute queries
    Params: 
        Conn(Connection Object) - Use the setupDbConnection helper function
        Query(String) - Query to be executed
        Data(Tuple) - Parameters that are passed into our query
    '''

    if conn is False: # Indicator: Failed to connect to the database
        print("Could not connect to database.  Abandoning query")
        return
    else:
        cursor = conn.cursor()
    
    try:
        print("Query:", query, data)
        if data:
            cursor.execute(query, (data))
        else:
            cursor.execute(query)
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("Failed to execute the query\n", e)
        return
    else:
        print("Successfully submitted query to the databse")
        return

# Create a player or two in the database, who belongs to a team, and capture a note on them

CREATE_DUMMY_PLAYER_QUERY_TEAM = "INSERT INTO Teams (team_id, name) VALUES (?, ?)"
TEAM_DATA = (None, "Atlanta Falcons")
TEAM_DATA2 = (None, "Seattle Seahawks")

CREATE_DUMMY_PLAYER_QUERY_PLAYER = "INSERT INTO Players (player_id, name, position, team_id) VALUES (?, ?, ?, ?)"
PLAYER_DATA = (None, "Bijan Robinson", "RB", 1)
PLAYER_DATA2 = (None, "Kenneth Walker", "RB", 2)

CREATE_DUMMY_PLAYER_QUERY_NOTE = "INSERT INTO Notes (note_id, player_id, note_type, note_content) VALUES (?, ?, ?, ?)"
NOTE_DATA = (None, 1, "General", "This guy is great, but he's in a tough system.  Risky play")
NOTE_DATA2 = (None, 2, "Injury", "This guy is great, but he hurt his hamstring in training camp.   Small amount of risk")

DELETE_TEAMS_QUERY = 'DELETE FROM Teams'

#exeQuery(setupDbConnection(), DELETE_TEAMS_QUERY, None)
#exeQuery(setupDbConnection(), CREATE_DUMMY_PLAYER_QUERY_TEAM, TEAM_DATA2)
#exeQuery(setupDbConnection(), CREATE_DUMMY_PLAYER_QUERY_PLAYER, PLAYER_DATA2)
#exeQuery(setupDbConnection(), CREATE_DUMMY_PLAYER_QUERY_NOTE, NOTE_DATA2)