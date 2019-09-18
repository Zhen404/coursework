from HW4Template.dbservice import dataservice
from HW4Template.utils import utils as ut
import json
import time

ut.set_debug_mode(True)
dataservice.set_config()

template = {
    "nameLast": "Williams",
    "nameFirst": "Ted"
}

fields = ['playerID', 'nameFirst', 'bats', 'birthCity']


def test_get_resource():
    start_time = time.time()
    result = dataservice.retrieve_by_template("people", template, fields)
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print("Result = ", json.dumps(result, indent=2))
    print("Elapsed time:", elapsed_time)
# test_get_resource()
# test_get_resource()


template2 = {
    "nameLast": 'Williams'
}

fields2 = ['playerID', 'nameFirst', 'bats', 'birthCity']

def test_get_resource2():
    start_time = time.time()
    result = dataservice.retrieve_by_template("people", template2, fields2)
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print("Result = ", json.dumps(result[0:3], indent=2))
    print("Elapsed time:", elapsed_time)
test_get_resource2()
test_get_resource2()
