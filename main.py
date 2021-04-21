import sqlite3

conn = sqlite3.connect('Logs.db')

c = conn.cursor()
c.execute('''
            CREATE TABLE IF NOT EXISTS Logs(
            message text,
            event_type text,
            server_id integer,
            date date
            )''')

file1 = open('logs.txt', 'r')
while True:
    line = file1.readline()
    if not line:
        break

    splitLine = line.strip().split(' ')
    day = splitLine[0]
    hour = splitLine[1]
    event = splitLine[2]
    text = ''.join(splitLine[3:]).replace(':', '').replace('.', '')
    formattedDate = '2021-{}-{} {}'.format(day.split('/')[0], day.split('/')[1], hour)
    print(day, hour, event, formattedDate, text)
    sql = 'INSERT INTO Logs(message, event_type, server_id, date) VALUES(?, ?, 1, ?);'
    c.execute(sql, [text, event, formattedDate])
file1.close()
conn.commit()
