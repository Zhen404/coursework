import RDBTable
import pymysql

def find_by_template(table, template, fields, offset, limit):
	dt = RDBTable.RDBTable(table, {'host': 'localhost', 'user': 'dbuser', 'password': 'dbuser','db': 'lahman2017raw', 'charset': 'utf8mb4'})
	result = dt.find_by_template(template, fields, offset, limit)

	return result

def insert(table, r):
	dt = RDBTable.RDBTable(table, {'host': 'localhost', 'user': 'dbuser', 'password': 'dbuser','db': 'lahman2017raw', 'charset': 'utf8mb4'})
	dt.insert(r)

def find_by_primary_key(table, s, fields, offset, limit):
	dt = RDBTable.RDBTable(table, {'host': 'localhost', 'user': 'dbuser', 'password': 'dbuser','db': 'lahman2017raw', 'charset': 'utf8mb4'})
	result = dt.find_by_primary_key(s, fields, offset, limit)

	return result

def update_given_primary_key(table, r, primary_key):
	dt =RDBTable.RDBTable(table, {'host': 'localhost', 'user': 'dbuser', 'password': 'dbuser','db': 'lahman2017raw', 'charset': 'utf8mb4'})
	dt.update_given_primary_key(r, primary_key)

def delete_given_primary_key(table, primary_key):
	dt =RDBTable.RDBTable(table, {'host': 'localhost', 'user': 'dbuser', 'password': 'dbuser','db': 'lahman2017raw', 'charset': 'utf8mb4'})
	dt.delete_given_primary_key(primary_key)

# dependent resource related function
def get_foreign_key(table1, table2):

	query = "SELECT TABLE_NAME,COLUMN_NAME,CONSTRAINT_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME \
			FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE \
			WHERE TABLE_NAME = '{0}' AND REFERENCED_TABLE_NAME = '{1}';".format(table1, table2)
	cnx = pymysql.connect(host="localhost", user="dbuser",
							password="dbuser", db='lahman2017raw',
							charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)
	cursor = cnx.cursor()
	cursor.execute(query)
	result = cursor.fetchall()
	return result

def get_reference(table1, table2):

	fk1 = get_foreign_key(table1, table2)
	fk2 = get_foreign_key(table2, table1)
	ref_dict = {}
	if len(fk1) != 0:
		for i in range(len(fk1)):
			ref_dict[fk1[i]['COLUMN_NAME']] = fk1[i]['REFERENCED_COLUMN_NAME']
		depend_table = table1
		referenced_table = table2
	else:
		for i in range(len(fk2)):
			ref_dict[fk2[i]['COLUMN_NAME']] = fk2[i]['REFERENCED_COLUMN_NAME']
		depend_table = table2
		referenced_table = table1

	return depend_table, referenced_table, ref_dict

def get_primary_key(table):
	dt = RDBTable.RDBTable(table, {'host': 'localhost', 'user': 'dbuser', 'password': 'dbuser','db': 'lahman2017raw', 'charset': 'utf8mb4'})
	return dt.pk

def generate_dependent_result(resource, primary_key, related_resource, fields, offset, limit):
	resource_pk = get_primary_key(resource)
	related_resource_pk = get_primary_key(related_resource)

	primary_key_dict = {}
	for i in range(len(resource_pk)):
		primary_key_dict[resource_pk[i]] = list()
		primary_key_dict[resource_pk[i]].append(primary_key[i])

	depend_table, referenced_table, ref_dict = get_reference(resource, related_resource)
	

	if referenced_table == related_resource:

		template = {}
		for k, v in ref_dict.items():
			if ref_dict[k] in primary_key_dict.keys():
				template[v] = primary_key_dict[ref_dict[k]]
		pk = ref_dict.values()


	if referenced_table == resource:

		template = primary_key_dict
		pk = ref_dict.keys()

	result = find_by_template(related_resource, template, fields, offset, limit)

	for key in pk:
		for item in result:
			item[key] = {'values': template[key],
							'link': {'rel': referenced_table,
									'href': "/api/{0}/{1}".format(referenced_table, template[key][0])}}
	
	return result

def insert_dependent(resource, primary_key, related_resource, r):
	resource_pk = get_primary_key(resource)
	related_resource_pk = get_primary_key(related_resource)

	primary_key_dict = {}
	for i in range(len(resource_pk)):
		primary_key_dict[resource_pk[i]] = list()
		primary_key_dict[resource_pk[i]].append(primary_key[i])

	depend_table, referenced_table, ref_dict = get_reference(resource, related_resource)
	

	if referenced_table == related_resource:

		template = {}
		for k, v in ref_dict.items():
			if ref_dict[k] in primary_key_dict.keys():
				template[v] = primary_key_dict[ref_dict[k]]
		pk = ref_dict.values()


	if referenced_table == resource:

		template = primary_key_dict
		pk = ref_dict.keys()

	insert_row = template.copy()
	insert_row.update(r)

	insert(related_resource, insert_row)


def generate_next_url(current_url, offset, limit):
	if offset:
		offset = int(offset[0])
		limit = int(limit[0])
		next_offset = offset + 10
		next_limit = limit + 10

		cl1 = current_url.split("?")
		cl2 = cl1[1].split("&")
		next_url = cl1[0] + "?"

		for i in range(len(cl2)-2):
			next_url += "{}&".format(cl2[i])
		next_url = next_url + "offset={}&".format(next_offset) + "limit={}".format(next_limit)		
	else:
		offset = 0
		limit = 10
	
		next_offset = offset + 10
		next_limit = limit + 10


		next_url = current_url + "?offset={}&".format(next_offset) + "limit={}".format(next_limit)
	return next_url, offset, limit


def generate_teammate(playerID, offset, limit):
	query = "select playerID, teammate, min(yearID) as first_year, \
	max(yearID) as last_year, count(*) as count_season \
	from (select a1.playerID, a2.playerID as teammate, a1.yearID from (select * from appearances \
	where playerID = '{}') a1 join appearances a2 \
	on a1.teamID = a2.teamID and a1.yearID = a2.yearID) a3 \
	group by playerID, teammate;".format(playerID)

	cnx = pymysql.connect(host="localhost", user="dbuser",
							password="dbuser", db='lahman2017raw',
							charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)
	print(query)
	cursor = cnx.cursor()
	cursor.execute(query)
	result = cursor.fetchall()
	return result

def generate_career_stats(playerID, offset, limit):
	query = "select t1.playerID, t1.teamID, t1.yearID, g_all, hits, ABs, Assists, errors from \
		(select playerID, teamID, yearID, sum(G) as g_all, sum(H) as hits, sum(AB) as ABs from batting \
		group by playerID, teamID, yearID having playerID = '{0}') t1 join \
		(select playerID, teamID, yearID, sum(A) as Assists, sum(E) as errors from fielding \
		group by playerID, teamID, yearID having playerID = '{1}') t2 on \
		t1.playerID = t2.playerID and t1.teamID = t2.teamID and t1.yearID = t2.yearID;".format(playerID, playerID)

	cnx = pymysql.connect(host="localhost", user="dbuser",
							password="dbuser", db='lahman2017raw',
							charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)
	print(query)
	cursor = cnx.cursor()
	cursor.execute(query)
	result = cursor.fetchall()
	return result

def generate_roster(teamID, yearID, offset, limit):
	query ="select t3.nameLast, t3.nameFirst, t1.playerID, t1.teamID, t1.yearID, g_all, hits, ABs, Assists, errors from \
		(select playerID, teamID, yearID, sum(A) as Assists, sum(E) as errors from fielding \
		group by playerID, teamID, yearID) t1 join \
		(select playerID, teamID, yearID, sum(G) as g_all, sum(H) as hits, sum(AB) as ABs from batting \
		group by playerID, teamID, yearID) t2 on \
		t1.playerID = t2.playerID and t1.teamID = t2.teamID and t1.yearID = t2.yearID \
		join people t3 on t3.playerID = t1.playerID \
		where t1.teamID = '{0}' and t1.yearID = '{1}';".format(teamID, yearID)

	cnx = pymysql.connect(host="localhost", user="dbuser",
							password="dbuser", db='lahman2017raw',
							charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)
	print(query)
	cursor = cnx.cursor()
	cursor.execute(query)
	result = cursor.fetchall()
	return result	


