from __future__ import print_function

import rethinkdb as r
from future.utils import iteritems, with_metaclass

from mockthink.db import MockThink
from mockthink.test.common import as_db_and_table, make_test_registry

TESTS = {}
register_test = make_test_registry(TESTS)

class Meta(type):
    def __new__(cls, name, bases, attrs):
        result = super(Meta, cls).__new__(cls, name, bases, attrs)
        tests = [name for name in attrs.keys() if 'test' in name]
        register_test(result, result.__name__, tests)
        return result

class Base(with_metaclass(Meta, object)):
    pass

class MockTest(Base):
    @staticmethod
    def get_data():
        return {
            'dbs': {
                'default': {
                    'tables': {}
                }
            }
        }

def run_tests(conn, grep):
    for test_name, test_fn in iteritems(TESTS):
        if not grep or grep == 'ALL':
            test_fn(conn)
        elif grep in test_name:
            test_fn(conn)
        else:
            print('skipping: %s' % test_name)

def run_tests_with_mockthink(grep):
    think = MockThink(as_db_and_table('nothing', 'nothing', []))
    run_tests(think.get_conn(), grep)

def run_tests_with_rethink(grep):
    conn = r.connect('localhost', 30000)
    run_tests(conn, grep)
