For CSVTable class, the attributions are table_name, table_file, key_columns, len_key_columns, table, updated, columns.

For find_by_primary_key method, the validity of primary key is checked. In this method, we also checked if length of s is consistent with the number of primary key and if the fields includes undefined columns in original table

Similarly, for find_by_template method, the only difference from find_by_primary_key method is if the template includes undefined columns in original table.

For insert method, we check all things related to validity of primary key, insert columns. Apart from this, when we insert rows, we should check if the primary key is duplicated. 

For RDBTable class, it is similar to CSVTable. But for this class, we do not define exception by ourselves. It relies on the exception of mysql in this class.

All test case follows the rule that checking different exception and normal cases for the methods under the class.