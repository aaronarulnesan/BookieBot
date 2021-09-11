from discord.ext.commands.core import command
from database.config import config
import psycopg2
from psycopg2.extensions import AsIs


# SERVER_PASSWORD = os.environ.get('SERVER_PASSWORD')
# connection = psycopg2.connect(host="localhost", port="5432", database="main", user="postgres", password=SERVER_PASSWORD)

class DBManagement:

    # initilizes DBManagement object 
    # opens new connection and cursor
    # inits tables if they do not already exist
    def __init__(self):
        params = config()
        print('Connecting to the BookieBot database ...')
        try:
            self.conn = psycopg2.connect(**params)
            self.cur = self.conn.cursor()
            self.initDatabase()
            print('Connected to BookieBot database')
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)

    # close cursor and connection to database
    def close(self):
        try:
            self.cur.close()
            self.conn.close()
            print('BookieBot database connection closed')
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)

    # initializes tables and functions
    def initDatabase(self):
        try:
            self.cur.execute(open("database/sql/initDatabase.sql", "r").read());
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        print('Database Ready');

    # inserts a wager without outcomes into wagers table
    def insertWager(self, wagerName):
        command = """INSERT INTO wagers(wager_name)
                    VALUES('%s') 
                    RETURNING wager_name"""
        wager_name = None
        try:
            self.cur.execute(command, (AsIs(wagerName),))
            wager_name = self.cur.fetchone()[0]
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        print("{} has been inserted".format(wager_name))
    
    # insert an Outcome and links it to a wager
    def insertOutcome(self, wagerName, outcomeName):
        try:
            wager_id = self.findWagerID(wagerName)
            command = """INSERT INTO outcomes(outcome_name, wager_id)
                        VALUES( '%s', '%s')
                        RETURNING outcome_name"""
            try:
                self.cur.execute(command, (AsIs(outcomeName), wager_id))
                self.conn.commit()
                print("Outcome: {} has been made and placed under {}".format(outcomeName, wagerName))
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    

    def findWagerID(self, wagerName):
        try:
            self.cur.callproc('get_wager_id', (wagerName,))
            wager_id = self.cur.fetchone()[0]
            return wager_id
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

