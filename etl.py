import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    1. This procedure processes a song file whose filepath has been provided as an arugment.
    2. It extracts the song information in order to store it into the songs table.
    3. Then it extracts the artist information in order to store it into the artists table.

    INPUTS: 
    * cur: the cursor variable
    * filepath: the file path to the song file
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[["song_id", "title", "artist_id", "year", "duration"]].values.tolist()[0]
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[["artist_id", "artist_name", "artist_location", "artist_latitude", "artist_longitude"]].values.tolist()[0]
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    1. This procedure processes a log file whose filepath has been provided as an arugment.
    2. It filters data with "NextSong" Action.
    3. Secondly, It transforms `ts` column from milliseconds to datetime format.
    4. Then it extracts the time information in order to store it into the time table.
    5. After that, it extracts the user information in order to store it into the users table.
    6. Next, it gets song_id and artist_id for songplays table.
    7. Finally, it extracts the songplay information in order to store it into the songplays table.

    INPUTS: 
    * cur: the cursor variable
    * filepath: the file path to the log file
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df["page"] == "NextSong"]

    # convert timestamp column to datetime
    t = pd.to_datetime(df["ts"])
    
    # insert time data records
    time_data = [t.dt.time, t.dt.hour, t.dt.day, t.dt.weekofyear, t.dt.month, t.dt.year, t.dt.weekday]
    column_labels = ('start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday')
    time_df = time_df = pd.DataFrame({column_labels[i]: [row[i] for row in list(map(list, zip(*time_data)))] for i in range(len(column_labels))})

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[["userId", "firstName", "lastName", "gender", "level"]] 

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = time_df[["start_time"]].values.tolist()[0] +\
        df[["userId", "level"]].values.tolist()[0] + \
        [songid, artistid] + \
        df[["sessionId", "location", "userAgent"]].values.tolist()[0] 
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    1. This procedure gets all files matching an extension whose filepath has been provided as an arugment.
    2. It gets the total number of files found in the filepath.
    3. Then it iterates over these files and process them with the function that has been provided as an arugment.

    INPUTS: 
    * cur: the cursor variable
    * conn: the connection variable
    * filepath: the file path to the files
    * func: the function used for processing
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    This procedure connects to database.
    It processes the files needed.
    Then it closes the connection.
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
