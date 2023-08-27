#==========================File Header=============================================================
'''
This file is an object file that creates a class called database. This object is supposed to be 
used to create a database using sqlite
'''
#==========================File Header=============================================================
import sqlite3

class sqlite():
    
    #==========================Function Header=========================================================
    '''
    This constructor creates the connection with sqlite file and creates the cursor to excute queries
    within the self
    
    PARAMS:
            filename(str) - connects to file with this name
    '''
    #==========================Function Header=========================================================
    def __init__(self, fileName):
        self.conn = sqlite3.connect(f"{fileName}.sqlite")
        self.cur = self.conn.cursor() 
    
    #==========================Function Header=========================================================
    '''
    This function creates table of the given name with the given columns
    
    PARAMS:
            name(str) - name of the table
            headersWithProperties(str) - list of column names with properties separated by space
    '''
    #==========================Function Header=========================================================
    def createTable(self, name, headersWithProperties):
        query = f'''
        DROP TABLE IF EXISTS {name};
        CREATE TABLE {name} (
        '''
        query += headersWithProperties[0]
        #parsing through the list and creating the query from 
        #creating table with correct columns
        for i in range (1,len(headersWithProperties)):
                query += ","
                query += f"{headersWithProperties[i]}"
        query += ");"
        #executing query
        self.cur.executescript(query)
    
    #==========================Function Header=========================================================
    '''
    This function inserts values to a table

    PARAMS:
            table(str) - name of the table
            columns(str/list/tuple) - str/list/tuple of column names
            values(str/list/tuple/int) - str/list/tuple/int of values to be added
    
    RETURN:
            true if values added to the database
    '''
    #==========================Function Header=========================================================
    def insertValues(self, table, columns, values):
        #when columns is str and values is str/int
        if isinstance(columns, str) and (isinstance(values, str) or isinstance(values, int)):
            query = f"insert into {table}({columns}) values ({values})"
        #when columns is tuple
        elif isinstance(columns, tuple): 
            #when values is tuple
            if  isinstance(values, tuple) and len(columns) == len(values):
                query = f"insert into {table}{columns} values {values}"
            #when values is list
            elif isinstance(values, list) and len(columns) == len(values):
                valtup = tuple()
                for val in values:
                    valtup += (val,)
                query = f"insert into {table}{columns} values {valtup}"
            #when length of values and columns is not equal
            else: 
                return False;
        #when columns is list
        elif isinstance(columns, list):
            coltup = tuple()
            for col in columns:
                coltup += (col,)
            #when values is tuple
            if  isinstance(values, tuple) and len(columns) == len(values):
                query = f"insert into {table}{coltup} values {values}"
            #when values is list
            elif isinstance(values, list) and len(columns) == len(values):
                valtup = tuple()
                for val in values:
                    valtup += (val,)
                query = f"insert into {table}{coltup} values {valtup}"
            #when length of values and columns is not equal
            else: 
                return False;
        #when columns is none of the expected data types
        else:
            return False
        self.cur.executescript(query)
        return True

    #==========================Function Header=========================================================
    '''
    This function extracts values from a single table

    PARAMS:
            table(str) - name of the table
            whereCondition(str) - condition for the where clause; set to "" by default
            column(str/tuple) - column(s) to be extracted; set to "*" by default
    
    RETURN:
            extraction(list of tuples) - each tuple containing elements of the row
    '''
    #==========================Function Header=========================================================
    def extractValuesSingleTable(self, table, columns="*", whereCondition=""):
        query = f"select {columns} from {table}"
        #if where clause is required
        if whereCondition != "" and whereCondition != None:
            query += f" where {whereCondition}"
        self.cur.execute(query)
        extraction = self.cur.fetchall()
        return extraction
    
    #==========================Function Header=========================================================
    '''
    This function extracts values from multiple tables joined together

    PARAMS:
            tables(list) - list of the tables
            onCondition(str) - condition connecting tables
            column(str/tuple/list) - column(s) to be extracted; set to "*" by default
            whereCondition(str) - condition for the where clause; set to "" by default

    RETURN:
            extraction(list of tuples) - each tuple containing elements of the row
    '''
    #==========================Function Header=========================================================
    def extractValuesMultipleTables(self, tables, onCondition, columns="*", whereCondition=""):
        query = f"select {columns[0]}"
        for i in range (1,len(columns)):
            query += f",{columns[i]}"
        query += f" from {tables[0]} "
        for i in range (1,len(tables)):
            query += f"join {tables[i]} "
        query += f"on {onCondition}"
        if whereCondition != "" and whereCondition != None:
            query += f" where {whereCondition}"
        #print(query)
        self.cur.execute(query)
        extraction = self.cur.fetchall()
        return extraction
        
    #==========================Function Header=========================================================
    '''
    This function updates the value of an already existing row in the database

    PRARAMS:
            table(str) - name of the table
            setCondition(str) - condition which will set the updation (column = newVal)
            whereCondition(str) - condition for the where clause to find the row to be updated
    '''
    #==========================Function Header=========================================================
    def updateValues(self, table, setCondition, whereCondition):
        query = f"update {table} set {setCondition} where {whereCondition}"
        self.cur.executescript(query)