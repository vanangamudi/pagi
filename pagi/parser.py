import sys
from collections import OrderedDict
from keyedlist import KeyedList

def create_valid_python_variable_name(s):
    return s.strip('-').replace('-', '_')

class Action:
    def __init__(self, name, store, dest='', default='', type_=None):

        self.name  = name
        self.store = store
        
        if dest:
            self.dest = dest
        else:
            self.dest = create_valid_python_variable_name(self.name)

            
        self.default = default
        if type_:
            self.type_ = type_
        else:
            self.type_ = type(self.default)


        self.store[self.dest] = self.default

    def __call__(self, *args, **kwargs):
        value = kwargs['value']
        self.store[self.dest] = self.type_(value)

class CountAction(Action):
    def __init__(self, name, store, dest='', default='', type_=None):
        super().__init__(name, store, dest, default, type_)

    def __call__(self, *args, **kwargs):
        self.store[self.dest] += 1
        
class AppendAction(Action):
    def __init__(self, name, store, dest='', default='', type_=None):
        super().__init__(name, store, dest, default, type_)

    def __call__(self, *args, **kwargs):
        value = kwargs['value']
        self.store[self.dest].append(value)


class StoreAction(Action):
    pass

class StoreConstAction(Action):
    def __init__(self, name, store, dest='', default='', type_=None):
        super().__init__(name, store, dest, default, type_)

    def __call__(self, *args, **kwargs):
        super().__call__(value = self.default)
        
class StoreTrueAction(Action):
    def __init__(self, name, store, dest='', default=True):
        super().__init__(name, store, dest, type_)

class StoreFalseAction(Action):
    def __init__(self, name, store, dest='', default=False):
        super().__init__(name, store, dest, type_)

class ArgumentAction(Action):
    def __init__(self, name, store, dest='', default='', type_=None):
        super().__init__(name, store, dest, default, type_)



# Exceptions
class UnrecognizedOptionError(Exception):
    pass


class Parser:
    def __init__(self, name, store=None, parent=None):
        self.name = name
        self.parent = parent
        
        self._commands  = {}
        self._arguments = OrderedDict()
        self._options   = {}
        
        if store is not None:
            self.store = store
        else:
            self.store = KeyedList()


    def full_name(self, name):
        if self.parent:
            return '{}.{}'.format(self.name, name)
        else:
            return name
    
    def add_command(self, name):
        assert name not in self._commands
        self._commands[name] = Parser(self.full_name(name), self.store, self)
        return self._commands[name]

    def add_argument(self, name, dest='', default='', type_=None):
        assert name not in self._arguments
        self._arguments[name] = Action(self.full_name(name), self.store, dest, default, type_)

    def add_option(self, name,  dest='', default='', type_=None):
        name = name.strip('-')
        assert name not in self._options
        self._options[name] = Action(self.full_name(name),  self.store, dest, default, type_)

    def print_usage(self):
        print('usage')


    def split(self, s):
        try:
            index = s.index('=')
            args, value = s[:index], s[index+1:]

        except:
            args, value = s, ''

        return args, value
            
    def parse(self, args=None):
        if not args:
            args = sys.argv[1:]

        while len(args):
            arg = args.pop(0)
            if arg == '--':
                [self._arguments[k](value=v) for k, v in zip(self._arguments.keys(), args)]
                args=[]
                
            else:
                if arg.startswith('--'):
                    arg, value = self.split(arg.lstrip('-'))
                    if arg not in self._options:
                        raise UnrecognizedOptionError

                    self._options[arg](value=value)

                elif arg in self._commands:
                    self._commands[arg].parse(args)
                    
        return self.store
