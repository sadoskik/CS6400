from mysql.connector import connect, Error


class Database:
    def __init__(self):
        self.conn = connect(
            host="localhost",
            user="root",
            password="root",
            database="SIEM"
        )
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS routers (id INTEGER PRIMARY KEY, hostname text, brand text, ram integer, flash integer)")
        self.conn.commit()

    def fetch(self, table='', searchTerm='', attribute=''):
        self.cur.execute(
            "SELECT * FROM "+table+" WHERE "+attribute+" LIKE %s", (searchTerm,))
        rows = self.cur.fetchall()
        return rows
    def query(self, query="SELECT * FROM alerts"):
        self.cur.execute(
            query)
        rows = self.cur.fetchall()
        return rows
    def insert(self, table='', values=[]):
        self.cur.execute("INSERT INTO %s VALUES (%s)",
                         (table, values))
        self.conn.commit()

    def remove(self, table, id):
        self.cur.execute("DELETE FROM %s WHERE id=%s", (table, id))
        self.conn.commit()

    def update(self, id, hostname, brand, ram, flash):
        self.cur.execute("UPDATE routers SET hostname = ?, brand = ?, ram = ?, flash = ? WHERE id = ?",
                         (hostname, brand, ram, flash, id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
    
    def getColumns(self, table):
        columnQuery = """
        SELECT `COLUMN_NAME` 
        FROM `INFORMATION_SCHEMA`.`COLUMNS` 
        WHERE `TABLE_SCHEMA`='SIEM' 
        AND `TABLE_NAME`=%s"""
        self.cur.execute(columnQuery, (table,))
        rows = self.cur.fetchall()
        return rows
