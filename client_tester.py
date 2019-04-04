import calculator
calculator_radian = calculator.Calculator(verbose=True)
calculator_degrees = calculator.Calculator(angle_measure='degrees')


statements_to_test = '1', \
                     '2(3', \
                     '4(5+6(7))8', \
                     'pi', \
                     'pi pi', \
                     'pi pi pi', \
                     '\u03C0\u03C0\u03C0\u03C0', \
                     '2sin(\u03C0 - (\u03C0/2))sin(\u03C0)', \
                     '4sin(15sin((4 + 5)/3) + sin(pi)', \
                     '2cos(4pi)', \
                     '2tan(2pi)', \
                     'arcsin(1', \
                     'sin(cos(tan(1', \
                     '\u221A(4', \
                     '45\u221A(9)', \
                     "24\u221A(16-8(3/2))/cos(2pi", \
                     "arccos(root(0.9"

statement_answers = 1, 6, 1504, 3.1416, 9.8696, 31.0063, 97.4091, 0, 3.4184, 2, 0, 1.5708, 0.0134, 2, 135, 48, 0.3218

passed = 'passed'
for i in range(0, len(statements_to_test)):
    answer = calculator_radian.parse(statements_to_test[i])
    if answer != statement_answers[i]:
        print(statements_to_test[i] + ' failed')
        print(str(answer) + ' is not equal to ' + str(statement_answers[i]))
        print()
        passed = 'failed'
    else:
        print(str(answer) + ' is correct')
        print()

print(passed)
