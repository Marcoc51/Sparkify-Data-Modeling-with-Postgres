# DROP TABLES

songplay_table_drop = "drop table if exists songplays;"
user_table_drop = "drop table IF EXISTS users;"
song_table_drop = "drop table if exists songs;"
artist_table_drop = "drop table if exists artists;"
time_table_drop = "drop table if exists time;"

# CREATE TABLES

songplay_table_create = ("""create table if not exists songplays(
                            start_time bigint, user_id int not null, level varchar not null, song_id varchar, artist_id varchar, 
                            session_id int not null, location varchar, user_agent varchar not null,
                            primary key(session_id, start_time)
                            );
""")

user_table_create = ("""create table if not exists users(
                            user_id int primary key, first_name varchar, last_name varchar, gender varchar, level varchar
                            );
""")

song_table_create = ("""create table if not exists songs(
                            song_id varchar primary key, title varchar not null, artist_id varchar, year int, duration numeric not null
                            );
""")

artist_table_create = ("""create table if not exists artists(
                            artist_id varchar primary key, name varchar not null, location varchar, latitude text, longitude text
                            );
""")

time_table_create = ("""create table if not exists time(
                            start_time varchar, hour int, day int, week int, month int, year int, weekday int
                            );
""")

# INSERT RECORDS

songplay_table_insert = ("""insert into songplays(
                            start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT DO NOTHING;
""")

user_table_insert = ("""insert into users(
                            user_id, first_name, last_name, gender, level
                            ) VALUES (%s, %s, %s, %s, %s)
                            ON CONFLICT DO NOTHING;
""")

song_table_insert = ("""insert into songs(
                        song_id, title, artist_id, year, duration
                        ) VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT DO NOTHING;
""")

artist_table_insert = ("""insert into artists(
                            artist_id, name, location, latitude, longitude
                            ) VALUES (%s, %s, %s, %s, %s)
                            ON CONFLICT DO NOTHING;
""")


time_table_insert = ("""insert into time(
                            start_time, hour, day, week, month, year, weekday
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT DO NOTHING;
""")

# FIND SONGS

song_select = ("""select s.song_id, a.artist_id\
                  from songs s join artists a on s.artist_id=a.artist_id\
                  where s.title = %s and a.name = %s and s.duration = %s;
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]