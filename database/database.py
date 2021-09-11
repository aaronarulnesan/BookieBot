from database.config import config
import psycopg2
from psycopg2.extensions import AsIs


# SERVER_PASSWORD = os.environ.get('SERVER_PASSWORD')
# connection = psycopg2.connect(host="localhost", port="5432", database="main", user="postgres", password=SERVER_PASSWORD)

class DBManagement:

    def __init__(self):
        params = config()
        print('Connecting to the BookieBot database ...')
        try:
            self.conn = psycopg2.connect(**params)
            self.cur = self.conn.cursor()
            self.initTables()
            print('Connected to BookieBot database')
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)


    def close(self):
        self.cur.close()
        self.conn.close()
        print('BookieBot database connection closed')

    def initTables(self):
        commands = (
            """ CREATE TABLE IF NOT EXISTS wagers (
	            wager_id VARCHAR(255) NOT NULL,
	            wager_choices VARCHAR(255),
                PRIMARY KEY(wager_id)
            );
            """,
            """ CREATE TABLE IF NOT EXISTS players (
	            player_id VARCHAR(255),
                PRIMARY KEY(player_id)
            );
            """,
            """ CREATE TABLE IF NOT EXISTS bets (
	            bet_id SERIAL,
	            bet_value NUMERIC(3) NOT NULL,
                PRIMARY KEY(bet_id),
                wager_id VARCHAR(255) references wagers ON UPDATE CASCADE ON DELETE CASCADE,
                player_id VARCHAR(255) references players ON UPDATE CASCADE ON DELETE CASCADE
            );
            """
        )
        try:
            for command in commands:
                self.cur.execute(command);
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        print('Tables initialized');

    def insertWager(self, wagerName):
        command = """INSERT INTO wagers(wager_id)
                    VALUES('%s') 
                    RETURNING wager_id"""
        wager_id = None
        print(wagerName)
        try:
            self.cur.execute(command, (AsIs(wagerName),))
            wager_id = self.cur.fetchone()[0]
            self.conn.commit()
            
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        print("{} has been inserted".format(wager_id))
