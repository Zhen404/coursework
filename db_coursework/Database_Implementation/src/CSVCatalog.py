import pymysql
import csv
import logging
import json

class ColumnDefinition:
    """
    Represents a column definition in the CSV Catalog.
    """

    # Allowed types for a column.
    column_types = ("text", "number")

    def __init__(self, column_name, column_type="text", not_null=False):
        """

        :param column_name: Cannot be None.
        :param column_type: Must be one of valid column_types.
        :param not_null: True or False
        """
        self.column_name = column_name
        self.column_type = column_type
        self.not_null = not_null

    def __str__(self):
        pass

    def to_json(self):
        """

        :return: A JSON object, not a string, representing the column and it's properties.
        """

        return {'column_name': self.column_name, 'column_type':self.column_type, 'not_null': self.not_null}


class IndexDefinition:
    """
    Represents the definition of an index.
    """
    index_types = ("PRIMARY", "UNIQUE", "INDEX")

    def __init__(self, index_name, index_type):
        """

        :param index_name: Name for index. Must be unique name for table.
        :param index_type: Valid index type.
        """
        self.index_name = index_name
        self.index_type = index_type

class TableDefinition:
    """
    Represents the definition of a table in the CSVCatalog.
    """

    def __init__(self, t_name=None, csv_f=None, column_definitions=None, index_definitions=None, cnx=None):
        """

        :param t_name: Name of the table.
        :param csv_f: Full path to a CSV file holding the data.
        :param column_definitions: List of column definitions to use from file. Cannot contain invalid column name.
            May be just a subset of the columns.
        :param index_definitions: List of index definitions. Column names must be valid.
        :param cnx: Database connection to use. If None, create a default connection.
        """
        self.table_name = t_name
        self.path = csv_f
        if not column_definitions:
            self.column_definitions = []
        else:
            self.column_definitions = column_definitions
        if not index_definitions:
            self.index_definitions = {}
        else:
            self.index_definitions = index_definitions
        self.cnx = cnx
        self.table = []
        with open(self.path) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                self.table.append(row)



    def __str__(self):
        pass

    @classmethod
    def load_table_definition(cls, cnx, table_name):
        """

        :param cnx: Connection to use to load definition.
        :param table_name: Name of table to load.
        :return: Table and all sub-data. Read from the database tables holding catalog information.
        """ 
        try:
            select_query = "SELECT * FROM catalog WHERE tb_name = '{}'".format(table_name)
            select_cursor = cnx.cursor()
            select_cursor.execute(select_query)
            result = select_cursor.fetchall()


            column_definitions = result[0]['columns']
            definitions = result[0]['definition']
            indexes = result[0]['indexes']

            column_definitions = json.loads(column_definitions)

            definitions = json.loads(definitions)

            indexes = json.loads(indexes)

            return  cls(t_name=table_name, csv_f=definitions['path'], column_definitions=column_definitions, 
                index_definitions=indexes, cnx=cnx)
        
        
        except:
            raise

        

    def add_column_definition(self, c):
        """
        Add a column definition.
        :param c: New column. Cannot be duplicate or column not in the file.
        :return: None
        """
        try:
            duplicate = False
            for column_object in self.column_definitions:
                if c.column_name == column_object['column_name']:
                    duplicate = True

            if duplicate:
                raise ValueError("Add duplicate column")
            else:
                self.column_definitions.append(c.to_json())
                col_def = json.dumps(self.column_definitions)
                update_query = "UPDATE catalog SET columns = %s WHERE tb_name = %s"
                val = (col_def, self.table_name)
                update_cursor = self.cnx.cursor()

                update_cursor.execute(update_query, val)
                self.cnx.commit()
                return

        except ValueError as ve:
            print("Exception= ", ve)

    def drop_column_definition(self, c):
        """
        Remove from definition and catalog tables.
        :param c: Column name (string)
        :return:
        """
        try:
            exist = True
            for column_object in self.column_definitions:
                if c.column_name != column_object.column_name:
                    exist = False

            if not exist:
                raise ValueError("Column not in Table")
            else:
                self.column_definitions.remove(c)
                col_def = json.dumps(self.column_definitions)
                update_query = "UPDATE catalog SET columns = %s WHERE tb_name = %s"
                val = (col_def, self.table_name)
                update_cursor = self.cnx.cursor()

                update_cursor.execute(update_query, val)
                self.cnx.commit()                
                return

        except ValueError as ve:
            print("Exception= ", ve)



    def to_json(self):
        """

        :return: A JSON representation of the table and it's elements.
        """

        return {'definition':{'name': self.table_name, 'path': self.path}, 
                'columns': self.column_definitions, 'indexes': self.index_definitions}

    def define_primary_key(self, columns):
        """
        Define (or replace) primary key definition.
        :param columns: List of column values in order.
        :return:
        """
        try:
            exist = True
            column_list = []
            for column_object in self.column_definitions:
                column_list.append(column_object['column_name'])
            for col in columns:
                if col not in column_list:
                    exist = False

            if not exist:
                raise ValueError("Cannot define primary key because Column not in Table")
            else:
                self.index_definitions["PRIMARY"] = {'index_name': "PRIMARY", "columns": columns, "kind": "PRIMARY"}
                index_def = json.dumps(self.index_definitions)
                update_query = "UPDATE catalog SET indexes = %s WHERE tb_name = %s"
                val = (index_def, self.table_name)
                update_cursor = self.cnx.cursor()

                update_cursor.execute(update_query, val)
                self.cnx.commit()                               
                return

        except ValueError as ve:
            print("Exception= ", ve)        

    def define_index(self, index_name, columns, kind='index'):
        """
        Define or replace and index definition.
        :param index_name: Index name, must be unique within a table.
        :param columns: Valid list of columns.
        :param kind: One of the valid index types.
        :return:
        """
        try:
            if index_name in self.index_definitions.keys():
                raise ValueError("Index name already exists")
            else:
                self.index_definitions[index_name] = {'index_name': index_name, "columns": columns, "kind": kind}
                index_def = json.dumps(self.index_definitions)
                update_query = "UPDATE catalog SET indexes = %s WHERE tb_name = %s"
                val = (index_def, self.table_name)
                update_cursor = self.cnx.cursor()

                update_cursor.execute(update_query, val)
                self.cnx.commit()  
                return

        except ValueError as ve:
            print("Exception= ", ve)
        

    def drop_index(self, index_name):
        """
        Remove an index.
        :param index_name: Name of index to remove.
        :return:
        """
        try:
            if index_name not in self.index_definitions.keys():
                raise ValueError("Index name not exist")
            else:
                self.index_definitions.pop(index_name)
                index_def = json.dumps(self.index_definitions)
                update_query = "UPDATE catalog SET indexes = %s WHERE tb_name = %s"
                val = (index_def, self.table_name)
                update_cursor = self.cnx.cursor()

                update_cursor.execute(update_query, val)
                self.cnx.commit() 
                return

        except ValueError as ve:
            print("Exception=", ve)


    def get_index_selectivity(self, index_name):
        """
        :param index_name: Do not implement for now. Will cover in class.
        :return:
        """
        index_name = index_name.split("_")
        try:
            exist = False
            for name in self.index_definitions.keys():
                if index_name == self.index_definitions[name]['columns']:
                    exist = True

            if not exist:
                raise ValueError("Index name not defined in the table")

            else:
                num_tuple = len(self.table)
                index_val = []
                for row in self.table:
                    index_row = []
                    for name in index_name:
                        index_row.append(str(row[name]))

                    index_val.append('_'.join(index_row))

                num_distinct_index = len(set(index_val))

                return round(num_tuple/num_distinct_index)

        except ValueError as ve:
            print("Exception= ", ve)


    def describe_table(self):
        """
        Simply wraps to_json()
        :return: JSON representation.
        """
        return self.to_json()


class CSVCatalog:

    def __init__(self, dbhost="localhost", dbport="127.0.0.1:3306",
                 dbname="hw3", dbuser="dbuser", dbpw="dbuser", debug_mode=None):
        self.cnx = pymysql.connect(host=dbhost,
                              user=dbuser,
                              password=dbpw,
                              db=dbname,
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)

    def __str__(self):
        pass

    def create_table(self, table_name, file_name, column_definitions=None, primary_key_columns=None):
        

        with open(file_name, newline='') as f:
            reader = csv.reader(f)
            colnames = next(reader)
        f.close()

        column_json_list = []
        exist = True
        if column_definitions:
            
            for column_object in column_definitions:
                column_json_list.append(column_object.to_json())

            input_col = []
            for column_object in column_definitions:
                input_col.append(column_object.column_name)

            
            for name in input_col:
                if name not in colnames:
                    exist = False

        try:
            if not exist:
                raise ValueError("Some defined column not in underlying CSV")
            else:
                definition = json.dumps({"name": table_name, "path": file_name})
                column_string = json.dumps(column_json_list)
                primary_key_string = json.dumps(primary_key_columns)
                
                insert_query = "INSERT INTO catalog (tb_name, definition, columns, indexes) VALUES (%s, %s, %s, %s);"
                val = (table_name, definition, column_string, primary_key_string)
                insert_cursor = self.cnx.cursor()
                insert_cursor.execute(insert_query, val)
                self.cnx.commit()

                t = self.get_table(table_name)

                return t

        except ValueError as ve:
            print("Exception= ", ve)


    def drop_table(self, table_name):
        drop_query = "DELETE FROM catalog WHERE tb_name = '{}'".format(table_name)
        drop_cursor = self.cnx.cursor()
        drop_cursor.execute(drop_query)
        self.cnx.commit()


    def get_table(self, table_name):
        """
        Returns a previously created table.
        :param table_name: Name of the table.
        :return:
        """
        select_query = "SELECT * FROM catalog WHERE tb_name = '{}'".format(table_name)
        select_cursor = self.cnx.cursor()
        select_cursor.execute(select_query)
        result = select_cursor.fetchall()

        column_definitions = result[0]['columns']
        definitions = result[0]['definition']
        indexes = result[0]['indexes']

        column_definitions = json.loads(column_definitions)

        definitions = json.loads(definitions)

        indexes = json.loads(indexes)

        t = TableDefinition(t_name=table_name, csv_f=definitions['path'], column_definitions=column_definitions, 
            index_definitions=indexes, cnx=self.cnx) 

        return t
        














