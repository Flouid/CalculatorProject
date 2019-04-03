import calculator
calculator_radian = calculator.Client()
calculator_degrees = calculator.Client(angle_measure="degrees")

statements_to_test = "1", \
                     "2(3", \
                     "4(5+6(7))8", \
                     "sin(15)", \
                     "2sin(90)", \
                     "2sin(2\u03C0", \
                     "sin(3\u03C0)(2)", \
                     "\u03C0", \
                     "\u03C0\u03C0", \
                     "\u03C0\u03C0\u03C0", \
                     "\u03C0\u03C0\u03C0\u03C0",\
                     "sin(2\u03C0)sin(\u03C0)"

for statement in statements_to_test:
    print(calculator_radian.parse(statement))

