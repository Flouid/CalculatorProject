import Client
calculator = Client.Client()

print(calculator.parse("2"))                       # test the form a
print(calculator.parse("3(4)"))                    # test the form a(b)
print(calculator.parse("(5)6"))                    # test the form (b)a
print(calculator.parse("7(8)9(10)"))               # test the form a(b)c(d)
print(calculator.parse("11(12)13(14"))             # test the form a(b)c(d
print(calculator.parse("15 + sin(16) + 17"))       # test the form a + sin(b) + c

