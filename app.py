'''
Need to write a script to write in all of the players from ESPN's database
Probably just use pandas and add some columns for the data that I want, that they don't have
Might be able to find some other data sets to append onto each person's record in the db
'''

from flask import Flask, render_template
from sqlite3 import connect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Create player


# Read player


# Update player


# Delete player(s)


# Queries