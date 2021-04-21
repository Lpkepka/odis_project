import sqlite3

conn = sqlite3.connect('Logs.db')

c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS LOGS
             ([generated_id] INTEGER PRIMARY KEY,[Text] text, [Server_ID] integer, [Date] date)''')



conn.commit()
