import pymysql
import sys
import json


class RDBTable():

	def __init__(self, table_name, connect_info):
		"""
		:param connect_info: connect information to mysql (dictionary)
		"""
		self.connect_info = connect_info
		self.table_name = table_name
		self.cnx = pymysql.connect(host=self.connect_info['host'], user=self.connect_info['user'],
									password=self.connect_info['password'], db=self.connect_info['db'],
									charset=self.connect_info['charset'], cursorclass=pymysql.cursors.DictCursor)

		show_columns_string = "DESCRIBE {};".format(self.table_name)
		columns_cursor = self.cnx.cursor()
		columns_cursor.execute(show_columns_string)
		columns_content = columns_cursor.fetchall()
		self.columns_len = len(columns_content)
		self.columns = []
		for i in range(self.columns_len):
			self.columns.append(columns_content[i]['Field'])


		show_pk_string = "SHOW KEYS FROM {} WHERE Key_name = 'PRIMARY';".format(self.table_name)
		pk_cursor = self.cnx.cursor()
		pk_cursor.execute(show_pk_string)
		pk_content = pk_cursor.fetchall()
		self.pk_len = len(pk_content)
		self.pk = []
		for i in range(self.pk_len):
			self.pk.append(pk_content[i]['Column_name'])

	def __str__(self):
		s = "Columns: " + str(self.columns) + "\n" + "Primary Key: " + str(self.pk)
		return s

	def load(self):
		pass


	def save(self):
		pass


	def find_by_template(self, t, fields=None, offset=0, limit=10):
		'''
        Return a table containing the rows matching the template and field selector.
        :param t: Template that the rows much match.
        :param fields: A list of columns to include in responses.
        :return: query result containing the answer.
        '''

		if fields is None:
			fields = self.columns

		f = ", ".join(fields)
		query = "select " + f + " from " + self.table_name + " "

		condition = ""
		for k, v in t.items():
			if condition != "":
				condition += " and "
			condition += k + " = '" + v[0] + "'"

		if condition != "":
			condition = "where " + condition



		query = query + condition + " limit {} ".format(limit) + "offset {}".format(offset) +";"
		print(query)
		query_by_template = self.cnx.cursor()
		query_by_template.execute(query)
		result = query_by_template.fetchall()
		if len(result) == 0:
			result = None
		else:
			result = result
		return result



	def find_by_primary_key(self, s, fields=None, offset=0, limit=10):
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

		query = query + condition + " limit {} ".format(limit) + "offset {}".format(offset) + ";"
		print(query)
		query_by_pk = self.cnx.cursor()
		query_by_pk.execute(query)
		result = query_by_pk.fetchall()
		if len(result) == 0:
			result = None
		else:
			result = result
		return result


	def insert(self, r):
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

		insert_query = "insert into {0} {1} values {2};".format(self.table_name, col, val)
		print(insert_query)
		insert_cursor = self.cnx.cursor()
		insert_cursor.execute(insert_query, list(r.values()))
		
		self.cnx.commit()


	def delete(self, r):
		'''
		Delete all tuples matching the template.
		:param t: Template
		:return: None.
		'''


		condition = ""
		for k, v in r.items():
			if condition != "":
				condition += " and "
			condition = k + " = '" + v + "'"

		if condition != "":
			condition = "where " + condition

		delete_query = "delete from {} ".format(self.table_name) + condition
		print(delete_query)
		delete_cursor = self.cnx.cursor()
		delete_cursor.execute(delete_query)

		self.cnx.commit()

	def update_given_primary_key(self, r, primary_key):

		set_clause = ""
		for k, v in r.items():
			if set_clause != "":
				set_clause += ","
			set_clause += k + " = '" + v + "'"
		where_clause = ""
		for i in range(self.pk_len):
			if where_clause != "":
				where_clause += " and "
			where_clause += self.pk[i] + " = '" + primary_key[i] + "'"
		update_query = "update {0} set {1} where {2}".format(self.table_name, set_clause, where_clause)
		print(update_query)
		update_cursor = self.cnx.cursor()
		update_cursor.execute(update_query)

		self.cnx.commit()


	def delete_given_primary_key(self, primary_key):

		where_clause = ""
		for i in range(self.pk_len):
			if where_clause != "":
				where_clause += " and "
			where_clause += self.pk[i] + " = '" + primary_key[i] + "'"
		delete_query = "delete from {0} where {1}".format(self.table_name, where_clause)
		print(delete_query)
		delete_cursor = self.cnx.cursor()
		delete_cursor.execute(delete_query)

		self.cnx.commit()
		




# table = RDBTable('people', {'host': 'localhost', 'user': 'root', 'password': 'Lz19940305sql','db': 'lahman2017', 'charset': 'utf8'})
# print(table)

# table.find_by_template({'playerID': 'willite01'}, ['nameFirst', 'nameLast'])

# table.find_by_primary_key(['willite01'], ['nameFirst', 'nameLast'])

# table.insert({'playerID': 'dff1', 'nameLast': 'Ferguson', 'nameFirst': 'Donald'})

# table.find_by_template({'playerID': 'dff1'}, ['nameFirst', 'nameLast'])

# table.delete({'playerID': 'dff1'})

# table.find_by_template({'playerID': 'dff1'}, ['nameFirst', 'nameLast'])
