import re

items = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
items[3:6] = [''.join(items[3:6])]
print(items)
print()

statement = re.split('(\\*|\\+|-|/)', "2*sin(\u03C0 - (\u03C0/2))*sin(\u03C0)")
statement[2:4] = [''.join(statement[2:4])]
print(statement)
statement[3:5] = [''.join(statement[3:5])]
print(statement)
print()


terms = re.split('(\\*|\\+|-|/)', "2*sin(\u03C0 - (\u03C0/2))*sin(\u03C0)")
position = 0
while position < len(terms) - 1:
    print(terms)
    if (terms[position].count("(") > terms[position + 1].count(")")) & (terms[position].count("(") > 0):
        terms[position:position + 2] = [''.join(terms[position:position + 2])]
    elif (terms[position].count("(") == terms[position + 1].count(")")) & (terms[position].count("(") > 0):
        terms[position:position + 2] = [''.join(terms[position:position + 2])]
        position += 1
    else:
        position += 1
