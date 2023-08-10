'''
Need to write a script to write in all of the players from ESPN's database
Probably just use pandas and add some columns for the data that I want, that they don't have
Might be able to find some other data sets to append onto each person's record in the db
'''

from flask import Flask, render_template, request, url_for, flash, redirect
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
    
def get_team(team_id):
    conn = get_db_connection()
    team = conn.execute("SELECT * FROM Teams WHERE team_id=?", (team_id,)).fetchone()
    conn.close()
    if team is None:
        abort(404)
    else:
        return team

app = Flask(__name__)
app.config['SECRET_KEY'] = '473891rpunqt8-0ut-u180ruc28-08ru30'

# View all players
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

# View all teams
@app.route('/teamIndex')
def teamIndex():
    conn = get_db_connection()
    teams = conn.execute("SELECT * FROM Teams").fetchall()
    conn.close()
    return render_template('teamIndex.html', teams = teams)

# Create player


# Read player
@app.route('/player/<int:player_id>')
def viewPlayer(player_id):
    player = get_player(player_id)
    return render_template('player.html', player=player)

# Read individual team
@app.route('/team/<int:team_id>')
def viewTeam(team_id):
    team = get_team(team_id)
    return render_template('team.html', team = team)
    # Would be nice if we passed in all of the players associated with a team broken out by position/position rank within team


# Update player info (Will need to be able to update team info as-well)
@app.route('/updatePlayer/<int:player_id>', methods=('GET', 'POST'))
def updatePlayer(player_id):
    player = get_player(player_id)

    if request.method == 'POST':
        position_tier = request.form['position_tier']
        position_rank = request.form['position_rank']
        overall_rank = request.form['overall_rank']
        adp = request.form['adp']
        # will need a special method for updating team_id incase anybody changes teams
        injury_info = request.form['injury_info']

        conn = get_db_connection()
        conn.execute("UPDATE Players SET position_tier = ?, position_rank = ?, overall_rank = ?, adp = ?, injury_info = ? WHERE player_id = ?",
                     (position_tier, position_rank, overall_rank, adp, injury_info, player_id))
        conn.commit()
        conn.close()
        return redirect(url_for('viewPlayer', player_id=player_id))
    
    return render_template('editPlayer.html', player=player)

# Update a team's information
@app.route('/updateTeam/<int:team_id>', methods = ('GET', 'POST'))
def updateTeam(team_id):
    team = get_team(team_id)

    if request.method == 'POST':
        improvements = request.form['improvements']
        disimprovements = request.form['disimprovements']

        conn = get_db_connection()
        conn.execute("UPDATE Teams SET improvements = ?, disimprovements = ? WHERE team_id = ?",
                     (improvements, disimprovements, team_id))
        
        conn.commit()
        conn.close()
        return redirect(url_for('viewTeam', team_id=team_id))
    
    return render_template('updateTeam.html', team=team)
        

# Create a note that belongs to a player
@app.route('/createNote/<int:player_id>', methods=('GET', 'POST'))
def createNote(player_id):
    if request.method == 'POST':
        print("You received a POST request to create a Note for #", player_id, "\nNote Type of:", request.form['note_type'], "\nNote Content:", request.form['note_content'])
        note_type = request.form['note_type']
        note_content = request.form['note_content']

        if not note_type or not note_content:
            flash("Type of note and content are required!")
        else:
            conn = get_db_connection()
            conn.execute("INSERT INTO Notes (note_id, player_id, note_type, note_content) VALUES (?, ?, ?, ?)",
                         (None, player_id, note_type, note_content))
            conn.commit()
            conn.close()
            return redirect(url_for('viewPlayer', player_id=player_id))
    
    
    player = get_player(player_id)
    return render_template('createNote.html', player=player)

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