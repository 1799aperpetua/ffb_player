CREATE TABLE IF NOT EXISTS Players (
    player_id INTEGER PRIMARY KEY,
    name VARCHAR(255),
    position VARCHAR(255),
    position_tier INT,
    position_rank INT,
    overall_rank INT,
    adp INT,
    team_id INT,
    injury_info TEXT,
    FOREIGN KEY (team_id) REFERENCES Teams(team_id) 
);

CREATE TABLE IF NOT EXISTS Teams (
    team_id INTEGER PRIMARY KEY,
    name TEXT,
    improvements TEXT,
    disimprovements TEXT
);

CREATE TABLE IF NOT EXISTS Notes (
    note_id INTEGER PRIMARY KEY,
    player_id INT,
    note_type VARCHAR(255),
    note_content TEXT,
    FOREIGN KEY (player_id) REFERENCES Players(player_id)
);