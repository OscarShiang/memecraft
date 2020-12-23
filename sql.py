import os
import psycopg2

DATABASE_URL = os.getenv('DATABASE_URL')

class Database():
    def __init__(self):
        self.conn = psycopg2.connect(DATABASE_URL)
        self.cursor = self.conn.cursor()
    
    def insertMeme(self, name, url):
        query = f'''INSERT INTO meme_templates (name, url) VALUES ('{name}', '{url}');'''
        self.cursor.execute(query)
        self.conn.commit()

    def getMemes(self):
        query = '''SELECT * FROM meme_templates order by id'''
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def getBlesses(self):
        query = '''SELECT * FROM bless_templates order by id'''
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def getURL(self, kind):
        query = f'''SELECT url FROM meme_templates WHERE name = '{kind}';'''
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def getBlessURL(self, kind):
        query = f'''SELECT url FROM bless_templates WHERE name = '{kind}';'''
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def getConfigs(self, kind):
        query = f'''SELECT pos, color, font, fontsize FROM meme_configs WHERE kind = '{kind}';'''
        self.cursor.execute(query)
        
        data = self.cursor.fetchall()
        print(data)

        configs, color, font, fontsize = data[0]
        configs = eval(configs)
        color = eval(color)
        font = f'font/{font}'

        return configs, color, font, fontsize

    def getBlessConfigs(self, kind):
        query = f'''SELECT pos, color, outline, font, fontsize FROM bless_configs WHERE kind = '{kind}';'''
        self.cursor.execute(query)
        
        data = self.cursor.fetchall()
        print(data)

        configs, color, outline, font, fontsize = data[0]
        configs = eval(configs)
        color = eval(color)
        outline = eval(outline)
        font = f'font/{font}'

        return configs, color, outline, font, fontsize

    def uploadGallery(self, kind, url):
        query = f'''INSERT INTO meme_gallery (kind, url) VALUES ('{kind}', '{url}');'''
        self.cursor.execute(query)
        self.conn.commit()

    def getMemesFromGallery(self, kind=None):
        query = f'''SELECT * FROM meme_gallery'''
        if kind:
            query += f''' WHERE kind = {kind}'''
        query += ' order by id DESC LIMIT 10;'

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
