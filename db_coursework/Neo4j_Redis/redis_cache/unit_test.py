import data_cache
from HW4Template.utils import utils as ut

ut.set_debug_mode(True)

#t = {"playerID": "willite01", "nameLast": "Williams", "bats": "R"}
#r = data_cache.compute_key("people", {"playerID": "willite01", "nameLast": "Williams", "bats": "R"}, \
#                           ['nameLast', "birthCity"])


def test1():
    data_cache.add_to_cache(r, t)


def test2():
    result = data_cache.get_from_cache(r)
    print("Result = ", result)

#test1()
#test2()
t2 = {"playerID":"pedrodu01"}
r2 = data_cache.compute_key("people", {"playerID":"pedrodu01"}, ['nameLast', 'birthCity'])
def test3():	
	result = data_cache.get_from_cache(r2)
	print("Result=", result)

#test3()

def test4():
	result = data_cache.add_to_cache(r2, t2)

def test5():
	result = data_cache.get_from_cache(r2)
	print('Result = ', result)

# test4()
# test5()

def test6():
	print("add")
	data_cache.add_to_query_cache("people", {"playerID":"pedrodu01"}, ['nameLast', 'birthCity'], {"playerID":"pedrodu01"})
	print('finish')
test6()

def test7():
	result = data_cache.check_query_cache("people", {"playerID":"pedrodu01"}, ['nameLast', 'birthCity'])
	print("checked:", result)
test7()

