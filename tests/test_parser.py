from parser import Parser


p = Parser('Argument parser')

p.add_option('--make-parents', default=False)

c = p.add_command('create')
c.add_option('--dir.permissions', '', default=444)
c.add_argument('dir.name')


p.parse()


print(p.store)
