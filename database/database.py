from database.config import config
import psycopg2


# SERVER_PASSWORD = os.environ.get('SERVER_PASSWORD')
# connection = psycopg2.connect(host="localhost", port="5432", database="main", user="postgres", password=SERVER_PASSWORD)

class DBConnection:

    def __init__(self):
        params = config()
        print('Connecting to the BookieBot database ...')
        try:
            self.conn = psycopg2.connect(**params)
            self.cur = self.conn.cursor()
            self.initTables()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)


    def close(self):
        self.cur.close()
        self.conn.close()
        print('BookieBot database connection closed')

    def initTables(self):
        commands = (
            """ CREATE TABLE IF NOT EXISTS wagers (
	            wager_id SERIAL PRIMARY KEY,
	            wager_name VARCHAR(255) NOT NULL,
	            wager_choices VARCHAR(255) NOT NULL
            );
            """,
            """ CREATE TABLE IF NOT EXISTS bets (
	            bets_id SERIAL PRIMARY KEY,
	            bet_value DOUBLE PRECISION NOT NULL
            );
            """,
            """ CREATE TABLE IF NOT EXISTS players (
	            player_id VARCHAR(255) PRIMARY KEY
            );
            """
        )
        for command in commands:
            self.cur.execute(command);
        self.conn.commit()
        print('Tables initialized');