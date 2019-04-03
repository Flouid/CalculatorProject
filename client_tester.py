import calculator
calculator_radian = calculator.Client()
calculator_degrees = calculator.Client(angle_measure="degrees")

statements_to_test = "1", \
                     "2(3", \
                     "4(5+6(7))8", \
                     "\u03C0", \
                     "\u03C0\u03C0", \
                     "\u03C0\u03C0\u03C0", \
                     "\u03C0\u03C0\u03C0\u03C0",\
                 #    "sin(2\u03C0)sin(\u03C0)", \

for statement in statements_to_test:
    print(calculator_radian.parse(statement))

# print(calculator_radian.parse("cos(\u03C0/4) + cos(\u03C0)sin(2\u03C0)"))
# print("cos(\u03C0/4) + cos(\u03C0)sin(2\u03C0)".find("sin(", 0))
# print("cos(\u03C0/4) + cos(\u03C0)sin(2\u03C0)".find(""))

