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
        

    def fetch(self, table, searchTerm=None, attribute=None):
        fetchQuery = "SELECT * FROM "+table
        if searchTerm and attribute:
            fetchQuery+=" WHERE "+attribute+" LIKE "+str(searchTerm)
        self.cur.execute(fetchQuery
            )
        rows = self.cur.fetchall()
        return rows
    def query(self, query="SELECT *", table=""):
        self.cur.execute(
            "FROM "+table+" "+query)
        rows = self.cur.fetchall()
        return rows
    def insert(self, table='', values={}):
        columns = self.getColumns(table=table)
        insertCommand = "INSERT INTO "+table+"("
        for attribute in values:
            insertCommand+=attribute
            insertCommand+=","
        insertCommand=insertCommand[:-1]+") VALUES ("
        for attribute in values:
            if not "INT" in columns[attribute]:
                insertCommand+="'"
            insertCommand+=values[attribute]
            if not "INT" in columns[attribute]:
                insertCommand+="',"
        insertCommand=insertCommand[:-1]+")"
        print(insertCommand)
        self.cur.execute(insertCommand)
        self.conn.commit()

    def remove(self, table, id):
        self.cur.execute("DELETE FROM "+table+" WHERE id="+str(id))
        self.conn.commit()

    def update(self, table: str, id: int, values: dict):
        columns = self.getColumns(table=table)
        updateCommand = "UPDATE "+ table +" SET "
        
        for attribute in values:
            if attribute == 'id':
                continue
            if not "INT" in columns[attribute]:
                updateCommand += attribute + " = '" + values[attribute] + "',"
            else:
                updateCommand += attribute + " = " + values[attribute] + ","
        updateCommand = updateCommand[:-1]
        updateCommand += "WHERE id="+str(id)
        print(updateCommand)
        self.cur.execute(updateCommand)
        self.conn.commit()


    def __del__(self):
    
        self.conn.close()
    
    def getColumns(self, table: str)->dict:
        columnQuery = """
        SELECT `COLUMN_NAME`, `DATA_TYPE` 
        FROM `INFORMATION_SCHEMA`.`COLUMNS` 
        WHERE `TABLE_SCHEMA`='SIEM' 
        AND `TABLE_NAME`=%s"""
        self.cur.execute(columnQuery, (table,))
        rows = self.cur.fetchall()
        columnDict = dict()
        for row in rows:
            columnDict[row[0]] = row[1]
        return columnDict
    
    def getTables(self) -> list:
        self.cur.execute("SHOW TABLES")
        rows = self.cur.fetchall()
        tableList = []
        for row in rows:
            tableList.append(row[0])
        return tableList
