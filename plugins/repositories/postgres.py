# pull the data from the API and then Insert it directly into a landing table in the database
from psycopg2.extras import execute_values
import psycopg2
from typing import List
from pprint import pprint


class Postgres:
    def __init__(self,
                 dbname: str,
                 user: str,
                 password: str,
                 host: str,
                 port: int,
                 isolation_level: str = None):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.isolation_level = isolation_level
        self.conn = None
        self.cursor = None

    def __enter__(self) -> None:
        self.conn = psycopg2.connect(  
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port)
        if self.isolation_level:
            print("Isolation Level: ", self.isolation_level)
            self.conn.set_isolation_level(self.isolation_level)
        self.cursor = self.conn.cursor()
        return self.cursor 

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.cursor.close()
            self.conn.close()



def create_teams_table(cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS teams (
    id                integer PRIMARY KEY,
    conference        varchar(40),
    division          varchar(40),
    city              varchar(40),
    name              varchar(40),
    full_name         varchar(40),
    abbreviation      varchar(40)
);
""")
                   
def insert_teams(cursor, team_data: tuple):
    try:
        query = """
                INSERT INTO teams (id, conference, division, city, name, full_name, abbreviation)
                VALUES %s
                ON CONFLICT (id) DO NOTHING;
                """
        execute_values(cursor, query, team_data)
        print("Inserted data")
    except Exception as e:
        raise ValueError(f"Failed to insert dummy users, {e}")


def create_players_table(cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS players (
    id              integer PRIMARY KEY,
    first_name      varchar(40),
    last_name       varchar(40),
    position        varchar(5),
    height          varchar(10),
    weight          integer,
    jersey_number   varchar(4),    
    college         varchar(60),
    country         varchar(10),
    draft_year      integer,
    draft_round     integer,
    draft_number    integer,
    team_id         integer,
    CONSTRAINT fk_team_id
        FOREIGN KEY(team_id)
            REFERENCES teams(id)
   ); """)
    
def insert_players(cursor, players_data: List[tuple]):
    try:
        query = """
                INSERT INTO players (id, first_name, last_name, position, height, weight, jersey_number, college, country, draft_year, draft_round, draft_number, team_id)              VALUES %s
                ON CONFLICT (id) DO NOTHING;
                """
        execute_values(cursor, query, players_data)
        cursor.connection.commit()
    except Exception as e:
        raise ValueError(f"Failed to insert dummy users, {e}")