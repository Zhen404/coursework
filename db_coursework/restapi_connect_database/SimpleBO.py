import pymysql
import json
import RDBTable

cnx = pymysql.connect(host='localhost',
                              user='dbuser',
                              password='dbuser',
                              db='lahman2017raw',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)


def run_q(q, args, fetch=False):
    cursor = cnx.cursor()
    cursor.execute(q, args)
    if fetch:
        result = cursor.fetchall()
    else:
        result = None
    cnx.commit()
    return result

def template_to_where_clause(t):
    s = ""

    if t is None:
        return s

    for (k, v) in t.items():
        if s != "":
            s += " AND "
        s += k + "='" + v[0] + "'"

    if s != "":
        s = "WHERE " + s;

    return s


def find_by_template(table, template, fields=None):
    wc = template_to_where_clause(template)

    q = "select " + fields[0] + " from " + table + " " + wc
    result = run_q(q, None, True)
    return result


def insert(table, r):
    '''
    Insert a new row into the table.
    :param r: New row.
    :return: None.
    '''   

    col = ""
    val = ""
    for k, v in r.items():
        if col != "":
            col += ", "
        if val != "":
            val += ", "

        col += k
        val += "%s"

    col = "(" + col + ")"
    val = "(" + val + ")"

    insert_query = "insert into {0} {1} values {2};".format(table, col, val)
    print(insert_query)
    insert_cursor = cnx.cursor()
    insert_cursor.execute(insert_query, list(r.values()))
    
    cnx.commit()

# def primary_key_to_where_clause(s):
#     c = ""

#     if s is None:
#         return c

#     for i in s:
#         if c != "":
#             c += " and "
#         c += 

def find_by_primary_key(table, s, fields=None):
    """
    Return a table containing the rows matching the template and fields selector.
    :param s: string of values.
    : param fields: A list of columns to include in responses.
    :return: query result containing the answer.
    """

    if fields is None:
        fields = self.columns

    f = ", ".join(fields)
    query = "select " + f + " from " + self.table_name + " "

    condition = ""
    for i in range(self.pk_len):
        if condition != "":
            condition += " and "
        condition += self.pk[i] + " = '" + s[i] + "'"

    if condition != "":
        condition = "where " + condition

    query = query + condition + ";"
    print(query)
    query_by_pk = self.cnx.cursor()
    query_by_pk.execute(query)
    result = query_by_pk.fetchall()
    if len(result) == 0:
        result = None
    else:
        result = json.dumps(result, indent=2)
    return result



query = "select * from appearances limit 10"

cursor = cnx.cursor()
cursor.execute(query)
result = cursor.fetchall()
print(result)


