import calculator
test = calculator.Client(angle_measure="degrees")

while True:
    statement = input()
    print(test.parse(statement))
