import sqlite3
import csv

conn = sqlite3.connect('tracks.sqlite')
cur = conn.cursor()

cur.executescript(''' 
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Genre;                  
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;
                  
CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT Unique
);
                  
CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title    TEXT UNIQUE                
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title   TEXT UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER            
);                  
''')

with open('tracks.csv', 'r') as file:
    csv_reader = csv.DictReader(file)

    headers = csv_reader.fieldnames
    print("CSV Headers:", headers)

    for row in csv_reader:
        artist = row['Artist']
        genre = row['Genre']
        album = row['Album']
        track = row['Track']
        length = row['Length']
        rating = row['Rating']
        count = row['Play count']

        if not artist or not genre or not album or not track:
            continue


        cur.execute('INSERT OR IGNORE INTO Artist (name) VALUES (?)', (artist,))
        cur.execute('SELECT id FROM Artist WHERE name = ?', (artist,))
        artist_id = cur.fetchone()[0]


        cur.execute('INSERT OR IGNORE INTO Genre (name) VALUES (?)', (genre,))
        cur.execute('SELECT id FROM Genre WHERE name = ?', (genre,))
        genre_id = cur.fetchone()[0]


        cur.execute('INSERT OR IGNORE INTO Album (title, artist_id) VALUES (?, ?)', (album, artist_id))
        cur.execute('SELECT id FROM Album WHERE title = ?', (album,))
        album_id = cur.fetchone()[0]


        cur.execute(''' INSERT OR REPLACE INTO Track (title, album_id, genre_id, len, rating, count)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (track, album_id, genre_id, length, rating, count)
        )

conn.commit()


cur.execute('''
    SELECT Track.title, Artist.name, Album.title, Genre.name
    FROM TRACK
    JOIN Genre ON Track.genre_id = Genre.id
    JOIN Album ON Track.album_id = Album.id
    JOIN Artist ON Album.artist_id = Artist.id
    ORDER BY Artist.name
    LIMIT 3
''')

for row in cur.fetchall():
    print(row)

conn.close()