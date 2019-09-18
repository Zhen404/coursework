In Folder /src

There are three files. 

1. DataTableExceptions.py file as Professor added. 

2. CSVCatalog.py, which is mainly used to save the metadata for tables. This file can save the metadata for different tables including file path, columns definitions and index definitions into one catalog table. This file mainly realizes creating metadata(add row in catalog table in db), get metadata, delete metadata. In table definition, it realize view other metadata under current table class, add column info, delete column info, add index info, delete index info, calculate index selectivity and format data.

3. CSVTable.py. This file is mainly used to realize optimization of selection and join. **find_by_template** function includes full table scan(the original way in hw1) and index selection(indexing the data with **build_index** function when creating table based on catalog table, then select data according to indexing with best access path from **get_access_path** function). For join optimization, there is two methods. One is when there is no where clause but one of the two tables includes index equal to on_fields, we use one block nested loop for join. The other is when there is where clause, we apply where clause in each table according to each table, then apply join.

In Folder /test

1. unit_test_catalog.py: Add case of test get_index_selectivity

2. unit_test_csv_table: Add join case for optimization 1 on_field not exist in any of table's indexes. Add selection test for no optimization and optimization cases and some invalid index and columns cases.