import calculator
test = calculator.Client()

while True:
    statement = input()
    print(test.parse(statement))