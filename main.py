import sqlite3

conn = sqlite3.connect('Logs.db')

c = conn.cursor()
c.execute('''CREATE TABLE LOGS
             ([generated_id] INTEGER PRIMARY KEY,[Text] text, [Server_ID] integer, [Date] date)''')

conn.commit()
