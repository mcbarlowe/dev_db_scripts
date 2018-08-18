import os
import sys
import psycopg2

def drop_tables(cursor, connection):
    '''
    Function to drop all tables in the NHL database to prepare for
    reinsertion.
    Inputs:
    connection - Connection to the PostgreSQL database

    Outputs:
    None
    '''
    # get list of tables in the NHL database
    cursor.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
    tables = cursor.fetchall()
    tables = [table[0] for table in tables]

    print(tables)

    for table in tables:
        test = 'DROP TABLE IF EXISTS nhl_tables.{};'.format(table)
        cursor.execute(test)
        connection.commit()

def create_tables(cursor, connection):
    '''
    Function to create all the tables needed for the NHL SQL database

    Inputs:
    connection - Connection to the PostgreSQL database

    Outputs:
    None
    '''

#create schedule table of the results of every nhl game
    cursor.execute("""
                   CREATE TABLE nhl_tables.nhl_schedule(
                   game_id integer primary key,
                   game_type text,
                   season text,
                   game_date date,
                   home_team_id integer,
                   home_team text,
                   home_score integer,
                   away_team_id integer,
                   away_team text,
                   away_score integer)
                """
                  )

#create table to store all nhl teams
    cursor.execute("""
                   CREATE TABLE nhl_tables.nhl_teams(
                   team_id integer primary key,
                   name text,
                   abbrev text,
                   division text,
                   conference text,
                   active text)
                   """)

#create table to store all nhl players past and present
    cursor.execute("""
                   CREATE TABLE nhl_tables.nhl_players(
                   id integer primary key,
                   name text,
                   birth_date date,
                   nationality text,
                   height text,
                   weight integer,
                   active text,
                   shoot_catches text,
                   position text)
                   """)
def main():

    '''
    Function to drop all tables in the existing database and create new ones
    for insertion of stats to setup the database fresh
    Inputs:
    None

    Outputs:
    None
    '''
    conn = psycopg2.connect(os.environ.get('DEV_DB_CONNECT'))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)
    conn.commit()


if __name__ == '__main__':
    main()
