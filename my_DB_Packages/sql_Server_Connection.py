import pandas as pd

import pyodbc


class Sql_Server_DataBase:
    def __init__(self, server_name, db_Name):
        self.server_name = server_name
        self.db_Name = db_Name
        self.myDB = self.getConnection()

    def getConnection(self):
        myDB = pyodbc.connect('Driver={SQL Server};'
                              'Server='+self.server_name+';'
                              'Database='+self.db_Name+';'
                              'Trusted_Connection=yes;')

        return myDB
    
    # Function returnes dataframe (pandas)
    def query_To_Pandas(self, query):
        df = pd.read_sql_query(query, self.myDB)
        return df

    # Function sends query 
    def send_Query(self, query):
        cursor = self.myDB.cursor()
        cursor.execute(query)

# Create Connection Object
# Example: DB_For_Project = Sql_Server_DataBase("XPS\SQLEXPRESS", "Project_For_DB")



