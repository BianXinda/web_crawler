import sys
import sqlite3

class Db91:
    def __init__(self):
        self.conn = sqlite3.connect('video91.db')
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute('CREATE TABLE videos (id varchar(50) PRIMARY KEY)')
        except sqlite3.OperationalError:
            print 'table already created'

    def insert_db(self, keyid):
        self.cursor.execute('INSERT INTO videos (id) VALUES (\'' + keyid + '\')')
        self.conn.commit()

    def select_db(self, keyid):
        keys = self.cursor.execute('SELECT * FROM videos WHERE id = \'' + keyid + '\'')
        if len(keys.fetchall()) > 0:
            print 'This video already in database:', keyid
            return True
        else:
            return False

    def clear_db(self):
        self.cursor.execute('DELETE FROM videos')
        self.conn.commit()

    def close_db(self):
        self.cursor.close()
        self.conn.close()

#used for check database status and clear data
#./db91.py               # show all keys
#./db91.py clear         # clear all keys
if __name__ == "__main__":
    if len(sys.argv) > 2:
        print './db91.py \t\t# show all keys \n./db91.py clear \t# clear all keys'
    db = Db91()
    #show all keys
    if len(sys.argv) == 1: 
        keys = db.cursor.execute('SELECT * FROM videos')
        print keys.fetchall()
    #delete all keys
    elif sys.argv[1] == 'clear': 
        db.clear_db()
    db.close_db()
