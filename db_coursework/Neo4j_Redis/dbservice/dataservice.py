
import pymysql.cursors
import json
from HW4Template.utils import utils as ut
from HW4Template.utils import dffutils as db
from HW4Template.redis_cache import data_cache as dc


db_schema = None                                # Schema containing accessed data
cnx = None                                      # DB connection to use for accessing the data.
key_delimiter = '_'                             # This should probably be a config option.


def set_config():
    """
    Creates the DB connection and sets the global variables.

    :param cfg: Application configuration data.
    :return: None
    """
    global db_schema
    global cnx

    db_params = {
        "dbhost": "localhost",
        "port": 3306,
        "dbname": "lahman2017raw",
        "dbuser": "dbuser",
        "dbpw": "dbuser",
        "cursorClass": pymysql.cursors.DictCursor,
        "charset": 'utf8mb4'
    }

    db_schema = "lahman2017"

    cnx = db.get_new_connection(db_params)


# Given one of our magic templates, forms a WHERE clause.
# { a: b, c: d } --> WHERE a=b and c=d. Currently treats everything as a string.
# We can fix this by using PyMySQL connector query templates.
def templateToWhereClause(t):
    s = ""
    for k,v in t.items():
        if s != "":
            s += " AND "
        s += k + "='" + v + "'"

    if s != "":
        s = "WHERE " + s;

    return s


# Given a table, template and list of fields. Return the result.
def retrieve_by_template(table, t, fields=None, limit=None, offset=None, orderBy=None):

    result = dc.check_query_cache(table, t, fields)
    
    if result is not None:
        print("Caching hit")
        return result
    else:
        print("Cache missing...")
        if t is not None:
            w = templateToWhereClause(t)
        else:
            w = ""

        if orderBy is not None:
            o = "order by " + ",".join(orderBy['fields']) + " " + orderBy['direction'] + " "
        else:
            o = ""

        if limit is not None:
            w += " LIMIT " + str(limit)
        if offset is not None:
            w += " OFFSET " + str(offset)

        if fields is None:
            f = "*"
        else:
            f = " " + ",".join(fields) + " "

        cursor=cnx.cursor()
        q = "SELECT " + f + " FROM " + table + " " + w + ";"


        r = db.run_q(cnx, q, None, fetch=True, commit=True)
        print("Insert Result to Cache...")
        m = dc.add_to_query_cache(table, t, fields, r)
        print("Insert Finished...")
        return r











