
import CSVTable
import json
import sys, os

print (os.path.realpath('.'))

def test1():

    csvt = CSVTableV2.CSVTable("People", "PeopleSmall.csv", ["playerID"])
    csvt.load()
    print("Table = ", csvt)


test1()

def test_template(test_name, table_name, table_file, key_columns, template, fields=None, show_rows=False):
    print("\n\n*******************************")
    print("Test name = ", test_name)
    print("Template = ", template)
    print("Fields = ", fields)

    try:
        csvt = CSVTableV2.CSVTable(table_name, table_file, key_columns)
        csvt.load()

        if not show_rows:
            print("Table name = ", csvt.table_name)
            print("Table file = ", csvt.table_file)
            print("Table keys = ", csvt.key_columns)
        else:
            print(csvt)

        r = csvt.find_by_template(template, fields)
        print("Result table:")
        print(r)
    except ValueError as ve:
        print("Exception = ", ve)


def test_insert(test_name, table_name, table_file, key_columns, row, show_rows=False):
    print("\n\n*******************************")
    print("Test name = ", test_name)
    print("Row to insert = ", row)

    try:
        csvt = CSVTableV2.CSVTable(table_name, table_file, key_columns)
        csvt.load()

        if not show_rows:
            print("Table name = ", csvt.table_name)
            print("Table file = ", csvt.table_file)
            print("Table keys = ", csvt.key_columns)
        else:
            print(csvt)

        r = csvt.insert(row)
        print("Result table:")

        csvt.save()

        if show_rows:
            print(r)

    except ValueError as ve:
        print("Exception = ", ve)


def test_primary_key(test_name, table_name, table_file, key_columns, s, fields=None, show_rows=False):
    print("\n\n*******************************")
    print("Test name = ", test_name)
    print("Key String = ", s)
    print("Fields = ", fields)

    try:
        csvt = CSVTableV2.CSVTable(table_name, table_file, key_columns)
        csvt.load()

        if not show_rows:
            print("Table name = ", csvt.table_name)
            print("Table file = ", csvt.table_file)
            print("Table keys = ", csvt.key_columns)
        else:
            print(csvt)

        r = csvt.find_by_primary_key(s, fields)
        print("Result table:")
        print(r)
    except ValueError as ve:
        print("Exception = ", ve)



def test_templates():
    test_template("Template Test1", "People", "People.csv", ["playerID"],
                  {"birthMonth": "9", "nameLast": "Williams"}, ["nameLast", "nameFirst", "birthMonth", "birthYear"],
                  False)

    test_template("Template Test2", "People", "People.csv", ["playerID"],
                  {"nameFirst": "Ted", "nameLast": "Williams"}, ["nameLast", "nameFirst", "birthMonth", "birthYear"],
                  False)

    test_template("Template Test3", "People", "People.csv", ["canary"],
                  {"nameFirst": "Ted", "nameLast": "Williams"}, ["nameLast", "nameFirst", "birthMonth", "birthYear"],
                  False)

    test_template("Template Test4", "Batting", "Batting.csv", ["playerID", "yearID", "teamID", "stint"],
                  {"playerID": "willite01"}, ["playerID", "yearID", "teamID", "AB", "H", "HR"],
                  False)

    test_template("Template Test5", "Batting", "Batting.csv", ["playerID", "yearID", "teamID", "stint"],
                  {"playerID": "willite01", "iq": 100}, ["playerID", "yearID", "teamID", "AB", "H", "HR"],
                  False)

    test_template("Template Test6", "Batting", "Batting.csv", ["playerID", "yearID", "teamID", "stint"],
                  {"playerID": "willite01", "yearID": "1961"}, ["playerID", "yearID", "teamID", "AB", "H", "iq"],
                  False)

    test_template("Template Test7", "Batting", "Batting.csv", ["playerID", "yearID", "teamID", "stint"],
                  {"playerID": "willite01", "yearID": "1960"}, ["playerID", "yearID", "teamID", "AB", "H", "HR", "Age"],
                  False)

    test_template("Template Test8", "Batting", "Batting.csv", ["yearID", "teamID", "stint"],
              {"playerID": "willite01"}, ["playerID", "yearID", "teamID", "AB", "H", "HR"],
              False)

#test_templates()

def test_inserts():

    test_insert("Insert Test 1", "People", "PeopleSmall.csv", ["playerID"],
                {"playerID": "dff1", "nameLast": "Ferguson", "nameFirst": "Donald"},
                False)

    test_template("Find after insert 1", "People", "PeopleSmall.csv", ["playerID"],
                  {"nameLast": "Ferguson"}, ["nameLast", "nameFirst", "birthMonth", "birthYear"],
                  False)

    try:
        test_insert("Insert Test 2", "People", "PeopleSmall.csv", ["playerID"],
                    {"playerID": "dff1", "nameLast": "Ferguson", "nameFirst": "Donald"},
                    False)

        raise ValueError("That insert should not have worked!")

    except ValueError as ve:
        print("OK. Did not insert duplicate key.")


    test_insert("Insert Test 3", "Batting", "BattingSmall.csv", ["playerID", "yearID", "teamID", "stint"],
                {"playerID": "dff1", "teamID": "BOS", "yearID": "2018", "stint": "1",
                    "AB": "100", "H": "100"},
                False)

    test_template("Find after insert 3", "Batting", "BattingSmall.csv", ["playerID", "yearID", "teamID", "stint"],
                  {"playerID": "dff1"}, None,
                  False)

    test_insert("Insert Test 4", "Batting", "BattingSmall.csv", ["playerID", "yearID", "teamID", "stint"],
            {"playerID": "dff1", "teamID": "BOS", "stint": "1", "AB": "100", "H": "100"},
            False)

    test_insert("Insert Test 5", "Batting", "BattingSmall.csv", ["playerID", "yearID", "teamID", "stint"],
        {"playerID": "dff1", "teamID": "BOS", "yearID": None, "stint": "1", "AB": "100", "H": "100"},
        False)

    test_insert("Insert Test 6", "Batting", "BattingSmall.csv", ["playerID", "yearID", "teamID", "stint"],
    {"playerID": "dff1", "teamID": "BOS", "yearID": "", "stint": "1", "AB": "100", "H": "100"},
    False)

#test_inserts()
def test_primary_keys():
    test_primary_key("Primary Key Test1", "People", "People.csv", ["playerID"],
                  ["9", "Williams"], ["nameLast", "nameFirst", "birthMonth", "birthYear"],
                  False)

    test_primary_key("Primary Key Test2", "Batting", "Batting.csv", ["playerID", "yearID"],
              ["willite01", "1961"], ["playerID", "yearID", "teamID", "AB", "H", "iq"],
              False)

    test_primary_key("Primary Key Test3", "Batting", "Batting.csv", ["playerID", "yearID"],
          ["willite01", "1960"], ["playerID", "yearID", "teamID", "AB", "H"],
          False)

#test_primary_keys()

