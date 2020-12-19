import os
import psycopg2

DATABASE_URL = os.getenv('DATABASE_URL')

class Database():
    def __init__(self):
        self.conn = psycopg2.connect(DATABASE_URL)
        self.cursor = self.conn.cursor()
    
    def insertMeme(name, url):
        query = f'''INSERT INTO meme_templates (name, url) VALUES ('{name}', '{url}');'''
        self.cursor.execute(query)
        self.conn.commit()

    def getMemes(self):
        query = '''SELECT * FROM meme_templates'''
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()
        

# with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
#     cursor = conn.cursor()

#     # query = 'DROP TABLE meme_templates'

#     # query = '''CREATE TABLE IF NOT EXISTS meme_templates (
#     #         id SERIAL PRIMARY KEY, name VARCHAR(128) NOT NULL, url VARCHAR(256) NOT NULL );'''

#     # query = '''INSERT INTO meme_templates (name, url) VALUES ('surprised-pikachu', 'https://i.imgur.com/rgRSjMW.png');'''

#     # query = '''DELETE FROM meme_templates WHERE id = 2;'''

#     query = '''SELECT * FROM meme_templates'''
#     cursor.execute(query)

#     data = []
#     while True:
#         temp = cursor.fetchone()
#         if temp:
#             data.append(temp)
#         else:
#             break
#     print(data)

#     # conn.commit()

#     cursor.close()
