import sys
import pdb
import unittest

from pprint import pprint, pformat

from pagi.parser import Parser
from keyedlist import KeyedList

class ParserTest(unittest.TestCase):
    def setUp(self):
        self.input_args = '--make-parents  create --dir.permissions=444 -- temp'.split()
        
        self.result = KeyedList({
            'make_parents': False,
            'create': {
                'dir' : {
                    'permissions': 444,
                    'name': 'temp'
                }
            }
        })
        
    def test(self):

        p = Parser('Argument parser')
        
        p.add_option('--make-parents', default=False)
        
        c = p.add_command('create')
        c.add_option('--dir.permissions', '', default=444)
        c.add_argument('dir.name')
        
        output = p.parse(self.input_args)

        pprint(output)
        pprint(self.result)
        self.assertEqual(output, self.result)



if __name__ == '__main__':
    unittest.main()
