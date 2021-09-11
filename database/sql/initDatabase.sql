
CREATE TABLE IF NOT EXISTS wagers (
wager_id SERIAL,
wager_name VARCHAR(255) UNIQUE NOT NULL,
total_pot NUMERIC(3),
PRIMARY KEY(wager_id)
);

CREATE TABLE IF NOT EXISTS outcomes (
outcome_id SERIAL,
outcome_name VARCHAR(255) UNIQUE NOT NULL,
outcome_total NUMERIC(3),
PRIMARY KEY(outcome_id),
wager_id INTEGER references wagers ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS players (
player_id VARCHAR(255),
PRIMARY KEY(player_id)
);

CREATE TABLE IF NOT EXISTS bets (
bet_id SERIAL,
bet_value NUMERIC(3) NOT NULL,
PRIMARY KEY(bet_id),
outcome_id integer references outcomes ON UPDATE CASCADE ON DELETE CASCADE,
player_id VARCHAR(255) references players ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE OR REPLACE FUNCTION get_wager_id(wager VARCHAR)
    RETURNS TABLE(wager_id INTEGER) AS
$$
#variable_conflict use_column
BEGIN
    RETURN QUERY
       
    SELECT wager_id
    FROM wagers
    WHERE wager_name = wager;

END; $$

LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_outcome_id(outcome VARCHAR)
    RETURNS TABLE(outcome_id INTEGER) AS
$$
#variable_conflict use_column
BEGIN
    RETURN QUERY
       
    SELECT outcome_id
    FROM outcomes
    WHERE outcome_name = outcome;

END; $$

LANGUAGE plpgsql;
