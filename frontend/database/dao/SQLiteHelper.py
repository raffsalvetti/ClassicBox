import sqlite3 as sqlite

# verificar uso do ORM SQLAlchemy

class SQLiteHelper(object):
    def __init__(self, dbfile):
        self.dbfile = dbfile
        self.connection = None

    def __dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def connect(self):
        self.connection = sqlite.connect(self.dbfile)
        self.connection.row_factory = self.__dict_factory
    
    def close(self):
        if self.connection:
            self.connection.close()
            
    def is_connected(self):
        return self.connection
    
    def Select(self, sql):
        data = None
        try:
            con = sqlite.connect(self.dbfile)
            con.row_factory = self.__dict_factory
            cur = con.cursor()
            #cur = self.connection.cursor()
            cur.execute(sql)
            data = cur.fetchall()
        except sqlite.Error as e:
            print "Erro executando: " + sql + ": " + e.args[0]
        finally:    
            if con:    
                con.close()
        return data
    
    def InsertUpdateDelete(self, sql, retrive_last = False):
        last_row = 0
        try:
            con = sqlite.connect(self.dbfile)
            con.row_factory = self.__dict_factory
            cur = con.cursor()
            #cur = self.connection.cursor()
            cur.execute(sql)
            con.commit()
            #self.connection.commit()
            if retrive_last:
                last_row = cur.lastrowid
            else:
                last_row = cur.rowcount
        except sqlite.Error as e:
            print "Erro executando " + sql + ": " + e.args[0]
            con.rollback()
            #self.connection.rollback()
        finally:    
            if con:    
                con.close()
        return last_row
