import csv  # Python package for reading and writing CSV files.
import sys
sys.path.append('..')
from src import DataTableExceptions
from src import CSVCatalog
from src import CSVTable

import time
import json

data_dir = "../Data/"

def cleanup():
    """
    Deletes previously created information to enable re-running tests.
    :return: None
    """
    cat = CSVCatalog.CSVCatalog()
    cat.drop_table("people")
    cat.drop_table("batting")
    cat.drop_table("teams")

def print_test_separator(msg):
    print("\n")
    lot_of_stars = 20*'*'
    print(lot_of_stars, '  ', msg, '  ', lot_of_stars)
    print("\n")


def test_join_not_optimized(optimize=False):
    """

    :return:
    """

    print_test_separator("Starting test_optimizable_1, optimize = " + str(optimize))
    print("\n\nDude. This takes 30 minutes. Trust me.\n\n")
    return

    cleanup()
    print_test_separator("Starting test_optimizable_1, optimize = " + str(optimize))

    cat = CSVCatalog.CSVCatalog()
    cds = []

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameLast", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameFirst", column_type="text"))
    cds.append(CSVCatalog.ColumnDefinition("birthCity", "text"))
    cds.append(CSVCatalog.ColumnDefinition("birthCountry", "text"))
    cds.append(CSVCatalog.ColumnDefinition("throws", column_type="text"))

    t = cat.create_table(
        "people",
        data_dir + "People.csv",
        cds)
    print("People table metadata = \n", json.dumps(t.describe_table(), indent=2))

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("H", "number", True))
    cds.append(CSVCatalog.ColumnDefinition("AB", column_type="number"))
    cds.append(CSVCatalog.ColumnDefinition("teamID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("yearID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("stint", column_type="number", not_null=True))

    t = cat.create_table(
        "batting",
        data_dir + "Batting.csv",
        cds)
    print("Batting table metadata = \n", json.dumps(t.describe_table(), indent=2))

    people_tbl = CSVTable.CSVTable("people")
    batting_tbl = CSVTable.CSVTable("batting")

    print("Loaded people table = \n", people_tbl)
    print("Loaded batting table = \n", batting_tbl)

    start_time = time.time()

    tmp = {"playerID": "willite01"}
    join_result = people_tbl.join(batting_tbl,['playerID'], tmp, optimize=optimize)

    end_time = time.time()

    print("Result = \n", join_result)
    elapsed_time = end_time - start_time
    print("\n\nElapsed time = ", elapsed_time)

    print_test_separator("Complete test_join_optimizable")


def test_join_optimizable_2(optimize=False):
    """
    Calling this with optimize=True turns on optimizations in the JOIN code.
    :return:
    """
    cleanup()
    print_test_separator("Starting test_optimizable_2, optimize = " + str(optimize))

    cat = CSVCatalog.CSVCatalog()
    cds = []

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameLast", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameFirst", column_type="text"))
    cds.append(CSVCatalog.ColumnDefinition("birthCity", "text"))
    cds.append(CSVCatalog.ColumnDefinition("birthCountry", "text"))
    cds.append(CSVCatalog.ColumnDefinition("throws", column_type="text"))

    t = cat.create_table(
        "people",
        data_dir + "People.csv",
        cds)
    print("People table metadata = \n", json.dumps(t.describe_table(), indent=2))
    t.define_index("playerID", ['playerID'], "INDEX")

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("H", "number", True))
    cds.append(CSVCatalog.ColumnDefinition("AB", column_type="number"))
    cds.append(CSVCatalog.ColumnDefinition("teamID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("yearID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("stint", column_type="number", not_null=True))

    t = cat.create_table(
        "batting",
        data_dir + "Batting.csv",
        cds)
    print("Batting table metadata = \n", json.dumps(t.describe_table(), indent=2))

    people_tbl = CSVTable.CSVTable("people")
    batting_tbl = CSVTable.CSVTable("batting")

    print("Loaded people table = \n", people_tbl)
    print("Loaded batting table = \n", batting_tbl)

    start_time = time.time()

    join_result = people_tbl.join(batting_tbl,['playerID'], None, optimize=optimize)

    end_time = time.time()

    print("Result = \n", join_result)
    elapsed_time = end_time - start_time
    print("\n\nElapsed time = ", elapsed_time)

    print_test_separator("Complete test_join_optimizable_2")


def test_join_optimizable_3(optimize=False):
    """

    :return:
    """
    cleanup()
    print_test_separator("Starting test_optimizable_3, optimize = " + str(optimize))

    cat = CSVCatalog.CSVCatalog()
    cds = []

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameLast", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameFirst", column_type="text"))
    cds.append(CSVCatalog.ColumnDefinition("birthCity", "text"))
    cds.append(CSVCatalog.ColumnDefinition("birthCountry", "text"))
    cds.append(CSVCatalog.ColumnDefinition("throws", column_type="text"))

    t = cat.create_table(
        "people",
        data_dir + "People.csv",
        cds)
    t.define_index("playerID", ['playerID'], "INDEX")
    print("People table metadata = \n", json.dumps(t.describe_table(), indent=2))

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("H", "number", True))
    cds.append(CSVCatalog.ColumnDefinition("AB", column_type="number"))
    cds.append(CSVCatalog.ColumnDefinition("teamID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("yearID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("stint", column_type="number", not_null=True))

    t = cat.create_table(
        "batting",
        data_dir + "Batting.csv",
        cds)
    print("Batting table metadata = \n", json.dumps(t.describe_table(), indent=2))
    t.define_index("playerID", ['playerID'], "INDEX")

    people_tbl = CSVTable.CSVTable("people")
    batting_tbl = CSVTable.CSVTable("batting")

    print("Loaded people table = \n", people_tbl)
    print("Loaded batting table = \n", batting_tbl)

    start_time = time.time()

    tmp = {"playerID": "willite01"}
    join_result = people_tbl.join(batting_tbl,['playerID'], tmp, optimize=optimize)

    end_time = time.time()

    print("Result = \n", join_result)
    elapsed_time = end_time - start_time
    print("\n\nElapsed time = ", elapsed_time)

    print_test_separator("Complete test_join_optimizable_3")

def test_join_optimizable_4(optimize=False):
    """
    Calling this with optimize=True turns on optimizations in the JOIN code.
    :return:
    """
    cleanup()
    print_test_separator("Starting test_optimizable_4, optimize = " + str(optimize))

    cat = CSVCatalog.CSVCatalog()
    cds = []

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameLast", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameFirst", column_type="text"))
    cds.append(CSVCatalog.ColumnDefinition("birthCity", "text"))
    cds.append(CSVCatalog.ColumnDefinition("birthCountry", "text"))
    cds.append(CSVCatalog.ColumnDefinition("throws", column_type="text"))

    t = cat.create_table(
        "people",
        data_dir + "People.csv",
        cds)
    print("People table metadata = \n", json.dumps(t.describe_table(), indent=2))
    t.define_index("playerID", ['playerID'], "INDEX")

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("H", "number", True))
    cds.append(CSVCatalog.ColumnDefinition("AB", column_type="number"))
    cds.append(CSVCatalog.ColumnDefinition("teamID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("yearID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("stint", column_type="number", not_null=True))

    t = cat.create_table(
        "batting",
        data_dir + "Batting.csv",
        cds)
    print("Batting table metadata = \n", json.dumps(t.describe_table(), indent=2))

    people_tbl = CSVTable.CSVTable("people")
    batting_tbl = CSVTable.CSVTable("batting")

    print("Loaded people table = \n", people_tbl)
    print("Loaded batting table = \n", batting_tbl)

    start_time = time.time()

    join_result = people_tbl.join(batting_tbl,['yearID'], None, optimize=optimize)

    end_time = time.time()

    print("Result = \n", join_result)
    elapsed_time = end_time - start_time
    print("\n\nElapsed time = ", elapsed_time)

    print_test_separator("Complete test_join_optimizable_4")

def test_select_no_index_1():
    """

    :return:
    """

    print_test_separator("Starting test_select_no_index_1")

    cleanup()

    cat = CSVCatalog.CSVCatalog()
    cds = []

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameLast", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameFirst", column_type="text"))
    cds.append(CSVCatalog.ColumnDefinition("birthCity", "text"))
    cds.append(CSVCatalog.ColumnDefinition("birthCountry", "text"))
    cds.append(CSVCatalog.ColumnDefinition("throws", column_type="text"))

    t = cat.create_table(
        "people",
        data_dir + "People.csv",
        cds)
    print("People table metadata = \n", json.dumps(t.describe_table(), indent=2))


    people_tbl = CSVTable.CSVTable("people")

    print("Loaded people table = \n", people_tbl)

    start_time = time.time()

    select_result = people_tbl.find_by_template({'nameLast': 'Williams', 'nameFirst': 'Ted'})

    end_time = time.time()

    print("Result = \n", select_result)
    elapsed_time = end_time - start_time
    print("\n\nElapsed time = ", elapsed_time)

    print_test_separator("Complete test_select_no_index_1")

def test_select_no_index_2():
    """

    :return:
    """

    print_test_separator("Starting test_select_no_index_2")

    cleanup()

    cat = CSVCatalog.CSVCatalog()
    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("H", "number", True))
    cds.append(CSVCatalog.ColumnDefinition("AB", column_type="number"))
    cds.append(CSVCatalog.ColumnDefinition("teamID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("yearID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("stint", column_type="number", not_null=True))

    t = cat.create_table(
        "batting",
        data_dir + "Batting.csv",
        cds)
    print("Batting table metadata = \n", json.dumps(t.describe_table(), indent=2))
#    t.define_index("pid_idx", "INDEX", ['playerID'])




    batting_tbl = CSVTable.CSVTable("batting")

    print("Loaded batting table = \n", batting_tbl)

    start_time = time.time()

    select_result = batting_tbl.find_by_template({'teamID': 'BOS', 'yearID': '1961'})

    end_time = time.time()

    print("Result = \n", json.dumps(select_result, indent=2))
    elapsed_time = end_time - start_time
    print("\n\nElapsed time = ", elapsed_time)

    print_test_separator("Complete test_select_no_index_2")

def test_select_with_index_2():
    """

    :return:
    """

    print_test_separator("Starting test_select_with_index_2")

    cleanup()

    cat = CSVCatalog.CSVCatalog()
    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("H", "number", True))
    cds.append(CSVCatalog.ColumnDefinition("AB", column_type="number"))
    cds.append(CSVCatalog.ColumnDefinition("teamID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("yearID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("stint", column_type="number", not_null=True))

    t = cat.create_table(
        "batting",
        data_dir + "Batting.csv",
        cds)
    t.define_index("playerID", ['playerID'], 'INDEX')
    t.define_index("teamID_yearID", ['teamID', 'yearID'], "INDEX")
    print("Batting table metadata = \n", json.dumps(t.describe_table(), indent=2))



    batting_tbl = CSVTable.CSVTable("batting")

    print("Loaded batting table = \n", batting_tbl)

    start_time = time.time()

    select_result = batting_tbl.find_by_template({'teamID': 'BOS', 'yearID': '1961'})

    end_time = time.time()

    print("Result = \n", json.dumps(select_result, indent=2))
    elapsed_time = end_time - start_time
    print("\n\nElapsed time = ", elapsed_time)

    print_test_separator("Complete test_select_with_index_2")

def test_select_no_index_3():
    """

    :return:
    """

    print_test_separator("Starting test_select_no_index_3")

    cleanup()

    cat = CSVCatalog.CSVCatalog()
    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("H", "number", True))
    cds.append(CSVCatalog.ColumnDefinition("AB", column_type="number"))
    cds.append(CSVCatalog.ColumnDefinition("teamID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("yearID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("stint", column_type="number", not_null=True))

    t = cat.create_table(
        "batting",
        data_dir + "Batting.csv",
        cds)
    print("Batting table metadata = \n", json.dumps(t.describe_table(), indent=2))
#    t.define_index("pid_idx", "INDEX", ['playerID'])




    batting_tbl = CSVTable.CSVTable("batting")

    print("Loaded batting table = \n", batting_tbl)

    start_time = time.time()

    select_result = batting_tbl.find_by_template({'playerID': 'willste01'})

    end_time = time.time()

    print("Result = \n", json.dumps(select_result, indent=2))
    elapsed_time = end_time - start_time
    print("\n\nElapsed time = ", elapsed_time)

    print_test_separator("Complete test_select_no_index_3")

def test_select_with_index_3():
    """

    :return:
    """

    print_test_separator("Starting test_select_with_index_3")

    cleanup()

    cat = CSVCatalog.CSVCatalog()
    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("H", "number", True))
    cds.append(CSVCatalog.ColumnDefinition("AB", column_type="number"))
    cds.append(CSVCatalog.ColumnDefinition("teamID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("yearID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("stint", column_type="number", not_null=True))

    t = cat.create_table(
        "batting",
        data_dir + "Batting.csv",
        cds)
    t.define_index("playerID", ['playerID'], 'INDEX')
#    t.define_index("teamID_yearID", ['teamID', 'yearID'], "INDEX")
    print("Batting table metadata = \n", json.dumps(t.describe_table(), indent=2))



    batting_tbl = CSVTable.CSVTable("batting")

    print("Loaded batting table = \n", batting_tbl)

    start_time = time.time()

    select_result = batting_tbl.find_by_template({'playerID': 'willste01'})

    end_time = time.time()

    print("Result = \n", json.dumps(select_result, indent=2))
    elapsed_time = end_time - start_time
    print("\n\nElapsed time = ", elapsed_time)

    print_test_separator("Complete test_select_with_index_3")

test_join_not_optimized(optimize=False)
test_join_optimizable_2(optimize=True)
test_join_optimizable_3(optimize=True)
test_join_optimizable_4(optimize=True)
test_select_no_index_1()
test_select_no_index_2()
test_select_with_index_2()
test_select_no_index_3()
test_select_with_index_3()
