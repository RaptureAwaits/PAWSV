#!/usr/bin/env python3

import sqlite3

conn = sqlite3.connect('resource/tunes.db')
c = conn.cursor()

def print_db():
    c.execute('SELECT * FROM tunes')
    data = c.fetchall()

    head = ('title:', 'artist:', 'path:')
    for i in data:
        for j in range(0,3):
            print (head[j], i[j])
        print ('\n')
        
print_db()
while True:
    string = input('Command (Leave blank to reprint):\n')
    if string == '':
        print_db()
    else:
        c.execute(string)
        results = c.fetchall()
        for i in results:
            print(i)
            print('\n')
        conn.commit()
    
