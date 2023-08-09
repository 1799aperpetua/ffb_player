'''
Need to write a script to write in all of the players from ESPN's database
Probably just use pandas and add some columns for the data that I want, that they don't have
Might be able to find some other data sets to append onto each person's record in the db
'''

from flask import Flask, render_template
import sqlite3
import os
from werkzeug.exceptions import abort

def get_db_connection():
    conn = sqlite3.connect(os.getcwd() + '/player.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_player(player_id):
    conn = get_db_connection()
    player = conn.execute("SELECT Players.*, Teams.*, Teams.name AS team_name FROM Players INNER JOIN Teams ON Players.team_id = Teams.team_id WHERE Players.player_id= ?", (player_id,)).fetchone()
    # I'm going to need to decouple Notes and players and pass them into my HTML template separately.  I have a fetchone right above, and since I could have multiple notes... I'd need fetchall
    # Which would only further complicate template info
    conn.close()
    if player is None:
        abort(404)
    else:
        return player

app = Flask(__name__)

@app.route('/')
def index():
    conn = get_db_connection()
    # Join your player and team on player_id, then you'll be able to display a player's team when you query them
    playerAndTeamQuery = '''
        SELECT
            Players.player_id,
            Players.name AS player_name,
            Players.position,
            Players.adp,
            Teams.name AS team_name
        FROM 
            Players
        INNER JOIN Teams ON Players.team_id = Teams.team_id;
    '''
    players = conn.execute(playerAndTeamQuery).fetchall()
    conn.close()
    return render_template('index.html', players=players)

# Create player


# Read player
@app.route('/<int:player_id>')
def viewPlayer(player_id):
    player = get_player(player_id)
    return render_template('player.html', player=player)

# Update player

# Might use the query below for building out my database
mapPlayersToTeamsQuery = '''
    UPDATE Players 
    SET team_id = Teams.team_id
    FROM Teams
    WHERE Players.name = ? and Teams.name = ?
'''
player_name = "Justin Jefferson"
team_name = "Minnesota Vikings"
PLAYER_TEAM_DATA = (player_name, team_name)

# Delete player(s)


# Queries