import csv  # Python package for reading and writing CSV files.

import sys
sys.path.append('..')
from src import DataTableExceptions
from src import CSVCatalog
# You MAY have to modify to match your project's structure.
import time

import json

max_rows_to_print = 10


class CSVTable:
    # Table engine needs to load table definition information.
    

    def __init__(self, t_name, load=True):
        """
        Constructor.
        :param t_name: Name for table.
        :param load: Load data from a CSV file. If load=False, this is a derived table and engine will
            add rows instead of loading from file.
        """
        self.__catalog__ = CSVCatalog.CSVCatalog()
        self.__table_name__ = t_name

        # Holds loaded metadata from the catalog. You have to implement  the called methods below.
        self.__description__ = None
        if load:
            self.__load_info__()  # Load metadata
            self.__rows__ = []
            self.__load__()  # Load rows from the CSV file.

            # Build indexes defined in the metadata. We do not implement insert(), update() or delete().
            # So we can build indexes on load.
            self.__build_indexes__()
        else:
            self.__file_name__ = "DERIVED"

    def __load_info__(self):
        """
        Loads metadata from catalog and sets __description__ to hold the information.
        :return:
        """
        self.t = self.__catalog__.get_table(self.__table_name__)
        self.__description__ = self.t.describe_table()

        return


    def __get_file_name__(self):
        return self.__description__['definition']['path']

    # Load from a file and creates the table and data.
    def __load__(self):

        try:
            fn = self.__get_file_name__()
            with open(fn, "r") as csvfile:
                # CSV files can be pretty complex. You can tell from all of the options on the various readers.
                # The two params here indicate that "," separates columns and anything in between " ... " should parse
                # as a single string, even if it has things like "," in it.
                reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')

                # Get the names of the columns defined for this table from the metadata.
                column_names = self.__get_column_names__()

                # Loop through each line (well dictionary) in the input file.
                for r in reader:
                    # Only add the defined columns into the in-memory table. The CSV file may contain columns
                    # that are not relevant to the definition.
                    projected_r = self.project([r], column_names)[0]
                    self.__add_row__(projected_r)

        except IOError as e:
            raise DataTableExceptions.DataTableException(
                code=DataTableExceptions.DataTableException.invalid_file,
                message="Could not read file = " + fn)

    def __add_row__(self, r):
        """
        append row in table list
        param r: row
        """
        self.__rows__.append(r)
        return

    def __get_column_names__(self):
        colnames = []
        for column_object in self.__description__['columns']:
            colnames.append(column_object["column_name"])

        return colnames


    def __str__(self):
        """
        :return:
        """
        s = "Name: {0} File: {1} \n".format(self.__description__['definition']['name'], self.__description__['definition']['path'])
        s += "Row count: {} \n".format(len(self.__rows__))
        s += json.dumps(self.__description__, indent=2)
        s += "\n"
        s += "Index Infromation: \n"
        for idx in self.__description__['indexes'].keys():

            s += "Name: {0}, Columns: {1} \n".format(self.__description__['indexes'][idx]['index_name'], 
                                                    self.__description__['indexes'][idx]['columns'])
        s += "No. of entries: {}".format(len(self.__rows__))
        s += "\n"
        s += "Sample rows"
        s += " ".join(self.__get_column_names__())
        s += "\n"
        for i in range(5):
            s += " ".join(self.__rows__[i].values())
            s += "\n"
        s += " ".join(['...']*len(self.__get_column_names__()))
        s += "\n"
        for i in range(5):
            s += " ".join(self.__rows__[len(self.__rows__)-5+i].values())
            s += "\n"
        return s



    def __build_indexes__(self):
        """
        Create a dictionary to store index value combined as a string
        """
        self.index_info = {}
        for name in self.__description__['indexes'].keys():
            print("Building index for {0} in {1}...".format(name, self.__table_name__))
            value_dict = {}
            value_list = []
            for row in self.__rows__:
                value_list.append('_'.join([row[field] for field in self.__description__['indexes'][name]['columns']]))
            value_set = set(value_list)
            self.index_info[name] = {}

            for distinct_value in value_set:
                index_info_col = {}
                index_info_col[distinct_value] = [self.__rows__[index] for index, value in enumerate(value_list) if value == distinct_value]
                self.index_info[name].update(index_info_col)



    def __get_access_path__(self, tmp):
        """
        Returns best index matching the set of keys in the template.

        Best is defined as the most selective index, i.e. the one with the most distinct index entries.

        An index name is of the form "colname1_colname2_coluname3" The index matches if the
        template references the columns in the index name. The template may have additional columns, but must contain
        all of the columns in the index definition.
        :param tmp: Query template.
        :return: Index or None
        """
        tmp_name = list(tmp.keys())
        valid_idx = []
        for name in self.__description__['indexes'].keys():
            exist = True
            for col in self.__description__['indexes'][name]['columns']:
                if col not in tmp_name:
                    exist = False
            if exist:
                valid_idx.append('_'.join(self.__description__['indexes'][name]['columns']))
        if len(valid_idx) != 0:

            selectivity_list = []
            for idx in valid_idx:
                selectivity_list.append(self.t.get_index_selectivity(idx))

            min_id = selectivity_list.index(min(selectivity_list))
            best_path = valid_idx[min_id]

        else:
            best_path = None

        return best_path




    def matches_template(self, row, t):
        """

        :param row: A single dictionary representing a row in the table.
        :param t: A template
        :return: True if the row matches the template.
        """

        # Basically, this means there is no where clause.
        if t is None:
            return True

        try:
            c_names = list(t.keys())
            for n in c_names:
                if row[n] != t[n]:
                    return False
            else:
                return True
        except Exception as e:
            raise (e)

    def project(self, rows, fields):
        """
        Perform the project. Returns a new table with only the requested columns.
        :param fields: A list of column names.
        :return: A new table derived from this table by PROJECT on the specified column names.
        """
        try:
            if fields is None:  # If there is not project clause, return the base table
                return rows  # Should really return a new, identical table but am lazy.
            else:
                result = []
                for r in rows:  # For every row in the table.
                    tmp = {}  # Not sure why I am using range.
                    for j in range(0, len(fields)):  # Make a new row with just the requested columns/fields.
                        v = r[fields[j]]
                        tmp[fields[j]] = v
                    else:
                        result.append(tmp)  # Insert into new table when done.

                return result

        except KeyError as ke:
            # happens if the requested field not in rows.
            raise DataTableExceptions.DataTableException(-2, "Invalid field in project")

    def __find_by_template_scan__(self, t, fields=None, limit=None, offset=None):
        """
        Returns a new, derived table containing rows that match the template and the requested fields if any.
        Returns all row if template is None and all columns if fields is None.
        :param t: The template representing a select predicate.
        :param fields: The list of fields (project fields)
        :param limit: Max to return. Not implemented
        :param offset: Offset into the result. Not implemented.
        :return: New table containing the result of the select and project.
        """

        if limit is not None or offset is not None:
            raise DataTableExceptions.DataTableException(-101, "Limit/offset not supported for CSVTable")

        # If there are rows and the template is not None
        if self.__rows__ is not None:

            result = []

            # Add the rows that match the template to the newly created table.
            for r in self.__rows__:
                if self.matches_template(r, t):
                    result.append(r)

            result = self.project(result, fields)
        else:
            result = None

        return result

    def __find_by_template_index__(self, t, idx, fields=None, limit=None, offset=None):
        """
        Find using a selected index
        :param t: Template representing a where clause/
        :param idx: Name of index to use.
        :param fields: Fields to return.
        :param limit: Not implemented. Ignore.
        :param offset: Not implemented. Ignore
        :return: Matching tuples.
        """
        if limit is not None or offset is not None:
            raise DataTableExceptions.DataTableException(-101, "Limit/offset not supported for CSVTable")

        idx_columns = idx.split("_")
        idx_v = [t[field] for field in idx_columns]
        idx_string = "_".join(list(map(str, idx_v)))
        
        

        if self.__rows__ is not None:    
            result = []
            # for name in idx_columns:
            #     t.pop(name)


            for r in self.index_info[idx][idx_string]:
                if self.matches_template(r, t):
                    result.append(r)

            result = self.project(result, fields)

        else:
            result = None

        return result

    def find_by_template(self, t, fields=None, limit=None, offset=None):
        # 1. Validate the template values relative to the defined columns.
        # 2. Determine if there is an applicable index, and call __find_by_template_index__ if one exists.
        # 3. Call __find_by_template_scan__ if not applicable index.
        try:
            exist = True
            for name in t.keys():
                if name not in self.__get_column_names__():
                    exist = False

            if not exist:
                raise ValueError("Template includes undefined columns")
            else:
                best_path = self.__get_access_path__(t)
                if best_path:
                    result = self.__find_by_template_index__(t, best_path, fields)
                else:
                    result = self.__find_by_template_scan__(t, fields)

                return result
        except ValueError as ve:
            print("Exception= ", ve)

    def insert(self, r):
        raise DataTableExceptions.DataTableException(
            code=DataTableExceptions.DataTableException.not_implemented,
            message="Insert not implemented"
        )

    def delete(self, t):
        raise DataTableExceptions.DataTableException(
            code=DataTableExceptions.DataTableException.not_implemented,
            message="Delete not implemented"
        )

    def update(self, t, change_values):
        raise DataTableExceptions.DataTableException(
            code=DataTableExceptions.DataTableException.not_implemented,
            message="Updated not implemented"
        )

    def nested_join(self, right_r, on_fields, where_template=None, project_fields=None):
        """
        Brut Force way to do join
        """
        join_tb = []
        for r1 in self.__rows__:
            r1_value = self.project(r1, on_fields)
            for r2 in right_r.__rows__:
                r2_value = self.project(r2, on_fields)
                if r1_value == r2_value:
                    r = {**r1, **r2}
                    join_tb.append(r)

        if len(join_tb) != 0:
            result = []
            for r in join_tb:
                if self.matches_template(r, where_template):
                    result.append(r)

            result = self.project(result, project_fields)
        else:
            result = None

        return result

    def optimized_join_1(self, right_r, on_fields, project_fields=None):
        """
        Using one block-nested loop
        """
        try:
            on_fields_string = '_'.join(on_fields)
            if on_fields_string in self.__description__['indexes'].keys():
                index_table = self
                other_table = right_r
            elif on_fields_string in right_r.__description__['indexes'].keys():
                index_table = right_r
                other_table = self
            else:
                raise ValueError("Neither tables have index related to on_fields, Cannot be improved")
             
        
            join_tb = []
            
            for r1 in other_table.__rows__:
                r1_value = [r1[field] for field in on_fields]
                r1_string = "_".join(r1_value)
                if r1_string in index_table.index_info[on_fields_string].keys():
                    for r2 in index_table.index_info[on_fields_string][r1_string]:
                        r = {**r1, **r2}
                        join_tb.append(r)

            if len(join_tb) != 0:

                result = self.project(join_tb, project_fields)
            else:
                result = None

            return result

        except ValueError as ve:
            print("Exception= ", ve)

    
    def optimized_join_2(self, right_r, on_fields, where_template=None, project_fields=None):
        """
        Select by index then join 
        """
        left_template = {}
        right_template = {}
        for name in where_template.keys():
            if name in self.__get_column_names__():
                left_template[name] = where_template[name]
            if name in right_r.__get_column_names__():
                right_template[name] = where_template[name]
        left_select = self.find_by_template(left_template)
        right_select = right_r.find_by_template(right_template)
        join_tb = []
        for r1 in left_select:
            for r2 in right_select:
                r = {**r1, **r2}
                join_tb.append(r)

        if len(join_tb) != 0:

            result = self.project(join_tb, project_fields)
        else:
            result = None

        return result


    def join(self, right_r, on_fields, where_template=None, project_fields=None, optimize=False):
        """
        Implements a JOIN on two CSV Tables. Support equi-join only on a list of common
        columns names.
        :param left_r: The left table, or first input table
        :param right_r: The right table, or second input table.
        :param on_fields: A list of common fields used for the equi-join.
        :param where_template: Select template to apply to the result to determine what to return.
        :param project_fields: List of fields to return from the result.
        :return: List of dictionary elements, each representing a row.
        """


        # If not optimizations are possible, do a simple nested loop join and then apply where_clause and
        # project clause to result.
        #
        # At least two vastly different optimizations are be possible. You should figure out two different optimizations
        # and implement them.
        #
        if not optimize:
            join_tb = self.nested_join(right_r, on_fields, where_template, project_fields)
        else:
            if not where_template:
                join_tb = self.optimized_join_1(right_r, on_fields, project_fields)
            else:
                join_tb = self.optimized_join_2(right_r, on_fields, where_template, project_fields)

        
        if join_tb:
            s = "Name: Join({0} {1}) File: DERIVED \n".format(self.__table_name__, right_r.__table_name__)
            s += "Row count: {} \n".format(len(join_tb))
            s += "\n\n"
            s += " ".join(join_tb[0].keys())
            s += "\n"
            if len(join_tb) > 10:
                for i in range(5):
                    s += " ".join(join_tb[i].values())
                    s += "\n"
                s += " ".join(['...']*len(self.__get_column_names__()))
                s += "\n"
                for i in range(5):
                    s += " ".join(join_tb[len(join_tb)-5+i].values())
                    s += "\n"
            else:
                for i in range(len(join_tb)):
                    s += " ".join(join_tb[i].values())
                    s += "\n"
        else:
            s = "No table derived"



        return s




















