import csv          # Python package for reading and writing CSV files.
import copy         # Copy data structures.
import json

import sys,os

# You can change to wherever you want to place your CSV files.
rel_path = os.path.realpath('./Data')

class CSVTable():

    # Change to wherever you want to save the CSV files.
    data_dir = rel_path + "/"

    def __init__(self, table_name, table_file, key_columns):
        '''
        Constructor
        :param table_name: Logical names for the data table.
        :param table_file: File name of CSV file to read/write.
        :param key_columns: List of column names the form the primary key.
        '''

        self.table_name = table_name
        self.table_file = table_file
        self.key_columns = key_columns
        self.len_key_columns = len(self.key_columns)
        self.table = []
        self.updated = False
        self.columns = []

    def __str__(self):
        '''
        Pretty print the table and state.
        :return: String
        '''
        s = json.dumps(self.table, indent =2)
        s = s + "\n" + "Table Status: " + str(self.updated)
        return s

    def load(self):
        '''
        Load information from CSV file.
        :return: None
        '''
        with open(self.data_dir + self.table_file) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                self.table.append(row)
        self.columns = self.table[0].keys()
        #check validity of key_columns


    def find_by_primary_key(self, s, fields=None):
        """
        Return a table containing the rows matching the template and fields selector.
        :param s: string of values.
        : param fields: A list of columns to include in responses.
        :return: CSVTable containing the answer.
        """
        try:
            self.pk_validity_check()

            if len(s) != self.len_key_columns:
                raise ValueError("The length of primary key is not consistent")


            for field in fields:
                if field not in self.columns:
                    raise ValueError("Field including undefined columns {}".format(field))


            result = []
            for row in self.table:
                match = True
                for index, value in enumerate(s):
                    if row[self.key_columns[index]] != value:
                        match = False
                        break
                if match:
                    result_dict = {}
                    for field in fields:
                        result_dict[field] = row[field]
                    result.append(result_dict)
            result_list = self.result_convertor(result)
            return result_list  

        except ValueError as ve:
            print("Exception = ", ve)



    def find_by_template(self, t, fields=None):
        '''
        Return a table containing the rows matching the template and field selector.
        :param t: Template that the rows much match.
        :param fields: A list of columns to include in responses.
        :return: CSVTable containing the answer.
        '''
        try:
            if fields is None:
                fields = self.columns

            self.pk_validity_check()

            for k in t.keys():
                if k not in self.columns:
                    raise ValueError("Template including undefined columns {}".format(k))

            for field in fields:
                if field not in self.columns:
                    raise ValueError("Field including undefined columns {}".format(field))


            result = []
            for row in self.table:
                match = True
                for key, value in t.items():
                    if row[key] != value:
                        match = False
                        break
                if match:
                    result_dict = {}
                    for field in fields:
                        result_dict[field] = row[field]
                    result.append(result_dict)
            result_list = self.result_convertor(result)
            return result_list

        except ValueError as ve:
            print("Exception = ", ve)



    def save(self):
        '''
        Write updated CSV back to the original file location.
        :return: None
        '''

        with open(self.table_file, "w") as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=self.columns)
            csv_writer.writeheader()
            for row in self.table:
                csv_writer.writerow(row)

        self.updated = False

    def insert(self, r):
        '''
        Insert a new row into the table.
        :param r: New row.
        :return: None. Table state is updated.
        '''
        try:
            self.pk_validity_check()

            for key in r.keys():
                if key not in self.columns:
                    raise ValueError("Insert undefined columns")
        

            for key in self.key_columns:
                if key not in r.keys():
                    raise ValueError("Primary key {} not included in inserted row".format(key))
                

            for key in self.key_columns:
                if r[key] is None:
                    raise ValueError("Primary key {} has None value".format(key))
            
            for key in self.key_columns:
                if r[key] == "":
                    raise ValueError("Primary key {} including empty string".format(key))    

            for row in self.table:
                for key in self.key_columns:
                    if row[key] == r[key]:
                        raise ValueError("Duplicated primary key")
                    

            row_list = {}
            for key in self.columns:
                if key in r.keys():
                    row_list[key] = value
                else:
                    row_list[key] = None
            self.table.append(row_list)
            self.status = True

        except ValueError as ve:
            print("Exception = ", ve)


    def delete(self, t):
        '''
        Delete all tuples matching the template.
        :param t: Template
        :return: None. Table is updated.
        '''
        for key in t.keys():
            if key not in self.columns:
                print("Template including undefined columns")
                return

        for index, row in enumerate(self.table):
            match = True
            for key, value in t.items():
                if row[key] != value:
                    match = False
                    break
            if match:
                del self.table[index]

        self.updated = True
        

    def result_convertor(self, result):
        """
        Convert result dictionary into a pretty format
        :param result: result dictionary 
        """
        try:
            if len(result) == 0:
                raise ValueError("No matching data found")

            result_list = str(list(result[0].keys())) + "\n"
            for row in result:
                row_list = []
                for key, value in row.items():
                    row_list.append(value)
                result_list += str(row_list) + "\n"
            return result_list
        except ValueError as ve:
            print("Exception = ", ve)

    def pk_validity_check(self):
        for key in self.key_columns:
            if key not in self.columns:
                raise ValueError("Key columns is not defined in the csv file")
        key_row = []
        for row in self.table:
            s = ""
            for key in self.key_columns:
                s += str(row[key])
            key_row.append(s)
        if len(set(key_row)) < len(key_row):
            raise ValueError("Key columns combination duplicated, not valid as primary key")




