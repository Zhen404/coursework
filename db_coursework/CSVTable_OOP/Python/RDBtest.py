
import RDBTable
import json


def test1():

    rdb = RDBTable.RDBTable("people", {'host': 'localhost', 'user': 'root', 'password': 'Lz19940305sql','db': 'lahman2017', 'charset': 'utf8'})
    print("Table = ", rdb)


#test1()

def test_template(test_name, table_name, connect_info, template, fields=None, show_rows=False):
    print("\n\n*******************************")
    print("Test name = ", test_name)
    print("Template = ", template)
    print("Fields = ", fields)

    try:
        rdb = RDBTable.RDBTable(table_name, connect_info)

        if not show_rows:
            print("Table name = ", rdb.table_name)

        else:
            print(rdb)

        r = rdb.find_by_template(template, fields)
        print("Result table:")
        print(r)
    except Exception as e:
        print("Exception = ", e)


def test_insert(test_name, table_name, connect_info, row, show_rows=False):
    print("\n\n*******************************")
    print("Test name = ", test_name)
    print("Row to insert = ", row)

    try:
        rdb = RDBTable.RDBTable(table_name, connect_info)

        if not show_rows:
            print("Table name = ", rdb.table_name)

        else:
            print(rdb)

        r = rdb.insert(row)
        print("Result table:")


        if show_rows:
            print(r)

    except Exception as e:
        print("Exception = ", e)

def test_delete(test_name, table_name, connect_info, row, show_rows=False):
    print("\n\n*******************************")
    print("Test name = ", test_name)
    print("Row to insert = ", row)

    try:
        rdb = RDBTable.RDBTable(table_name, connect_info)

        if not show_rows:
            print("Table name = ", rdb.table_name)

        else:
            print(rdb)

        r = rdb.delete(row)
        print("Result table:")


        if show_rows:
            print(r)

    except Exception as e:
        print("Exception = ", e)


def test_primary_key(test_name, table_name, connect_info, s, fields=None, show_rows=False):
    print("\n\n*******************************")
    print("Test name = ", test_name)
    print("Key String = ", s)
    print("Fields = ", fields)

    try:
        rdb = RDBTable.RDBTable(table_name, connect_info)

        if not show_rows:
            print("Table name = ", rdb.table_name)

        else:
            print(rdb)

        r = rdb.find_by_primary_key(s, fields)
        print("Result table:")
        print(r)
    except Exception as e:
        print("Exception = ", e)



def test_templates():

    test_template("Template Test 1", "People", {'host': 'localhost', 'user': 'root', 'password': 'Lz19940305sql','db': 'lahman2017', 'charset': 'utf8'},
                  {"nameFirst": "Ted", "nameLast": "Williams"}, ["nameLast", "nameFirst", "birthMonth", "birthYear"],
                  False)


    test_template("Template Test 2", "Batting", {'host': 'localhost', 'user': 'root', 'password': 'Lz19940305sql','db': 'lahman2017', 'charset': 'utf8'},
                  {"playerID": "willite01", "iq": 100}, ["playerID", "yearID", "teamID", "AB", "H", "HR"],
                  False)

    test_template("Template Test 3", "Batting", {'host': 'localhost', 'user': 'root', 'password': 'Lz19940305sql','db': 'lahman2017', 'charset': 'utf8'},
                  {"playerID": "willite01", "yearID": "1961"}, ["playerID", "yearID", "teamID", "AB", "H", "iq"],
                  False)

    test_template("Template Test 4", "Batting", {'host': 'localhost', 'user': 'root', 'password': 'Lz19940305sql','db': 'lahman2017', 'charset': 'utf8'},
                  {"playerID": "willite01", "yearID": "1960"}, ["playerID", "yearID", "teamID", "AB", "H", "HR", "Age"],
                  False)


#test_templates()

def test_insert_delete():

    test_insert("Insert Test 1", "People", {'host': 'localhost', 'user': 'root', 'password': 'Lz19940305sql','db': 'lahman2017', 'charset': 'utf8'},
                {"playerID": "dff1", "nameLast": "Ferguson", "nameFirst": "Donald"},
                False)

    test_template("Find after insert 1", "People", {'host': 'localhost', 'user': 'root', 'password': 'Lz19940305sql','db': 'lahman2017', 'charset': 'utf8'},
                  {"playerID": "dff1"}, ["nameLast", "nameFirst", "birthMonth", "birthYear"],
                  False)

    test_insert("Insert Test 2", "People", {'host': 'localhost', 'user': 'root', 'password': 'Lz19940305sql','db': 'lahman2017', 'charset': 'utf8'},
                    {"playerID": "dff1", "nameLast": "Ferguson", "nameFirst": "Donald"},
                    False)

    test_delete("Delete Test 1", "People", {'host': 'localhost', 'user': 'root', 'password': 'Lz19940305sql','db': 'lahman2017', 'charset': 'utf8'},
                {"playerID": "dff1"},
                False)

    test_template("Find after delete 1", "People", {'host': 'localhost', 'user': 'root', 'password': 'Lz19940305sql','db': 'lahman2017', 'charset': 'utf8'},
                  {"playerID": "dff1"}, ["nameLast", "nameFirst", "birthMonth", "birthYear"],
                  False)

    test_delete("Delete Test 2", "People", {'host': 'localhost', 'user': 'root', 'password': 'Lz19940305sql','db': 'lahman2017', 'charset': 'utf8'},
            {"playerID": "dff1"},
            False)

    test_insert("Insert Test 3", "Batting", {'host': 'localhost', 'user': 'root', 'password': 'Lz19940305sql','db': 'lahman2017', 'charset': 'utf8'},
        {"playerID": "dff1", "teamID": "BOS", "yearID": None, "stint": "1", "AB": "100", "H": "100"},
        False)


#test_insert_delete()

def test_primary_keys():
    test_primary_key("Primary Key Test 1", "People", {'host': 'localhost', 'user': 'root', 'password': 'Lz19940305sql','db': 'lahman2017', 'charset': 'utf8'},
                  ["9", "Williams"], ["nameLast", "nameFirst", "birthMonth", "birthYear"],
                  False)

    test_primary_key("Primary Key Test 2", "Batting", {'host': 'localhost', 'user': 'root', 'password': 'Lz19940305sql','db': 'lahman2017', 'charset': 'utf8'},
              ["willite01", "1961"], ["playerID", "yearID", "teamID", "AB", "H", "iq"],
              False)

    test_primary_key("Primary Key Test 3", "Batting", {'host': 'localhost', 'user': 'root', 'password': 'Lz19940305sql','db': 'lahman2017', 'charset': 'utf8'},
          ["willite01", "1960"], ["playerID", "yearID", "teamID", "AB", "H"],
          False)

    test_primary_key("Primary Key Test 4", "People", {'host': 'localhost', 'user': 'root', 'password': 'Lz19940305sql','db': 'lahman2017', 'charset': 'utf8'},
          ["willite01"], ["nameLast", "nameFirst", "birthMonth", "birthYear"],
          False)

test_primary_keys()

