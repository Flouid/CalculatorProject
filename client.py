import calculator

print('debugging mode? (y/n)')
verbose_string = input()
if (verbose_string == 'y') | (verbose_string == 'Y'):
    test = calculator.Calculator(angle_measure='degrees', verbose=True)
else:
    test = calculator.Calculator(angle_measure='degrees')

print(test.parse('45\u221A(9)'))

while True:
    statement = input()
    print(test.parse(statement))
