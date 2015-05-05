import sqlite3


class Db91:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def create_db(self):
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
        t = (keyid, )
        keys = self.cursor.execute('SELECT * FROM videos WHERE id=?', t)
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
if __name__ == "__main__":
    db = Db91()
    db.create_db()
    keys = db.cursor.execute('SELECT * FROM videos WHERE id')
    print keys.fetchall()
    # db.clear_db()
    db.close_db()
