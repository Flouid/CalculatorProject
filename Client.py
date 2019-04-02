import math


class Client:
    """The client through which the user interacts with the calculator"""

    def __init__(self, verbose=False, notation="default", mode="radian"):
        self.verbose = verbose
        self.notation = notation
        self.mode = mode

    def parse(self, statement):
        """Passed the user's statement and attempts to parse it into something evaluable"""
        statement = statement.replace(" ", "")  # removes whitespace if there is any

        valid_digits = "1234567890"

        # Converts strings in the form a(b) or (b)a to a*(b) or (b)*a.
        group_count = statement.count("(")
        position = 0
        for i in range(0, group_count):

            position = statement.find("(", position)
            if (position > 0) & (statement[position - 1] in valid_digits):
                statement = statement[:position] + "*" + statement[position:]

            position = statement.find(")", position)
            if (position != -1) & (position + 1 < len(statement)):
                if statement[position + 1] in valid_digits:
                    statement = statement[:position + 1] + "*" + statement[position + 1:]

        # Converts strings in the form (a to (a)
        if (statement.find(")", statement.rfind("(")) == -1) & (statement.find("(") != -1):
            statement = statement + ")"

        # Converts strings in the form "sin(a)" into the actual value of sin(a)
        group_count = statement.count("sin(")
        start_position = 0
        end_position = 0
        for i in range(0, group_count):

            start_position = statement.find("sin(", start_position)
            end_position = statement.find(")", end_position) + 1
            if start_position > 0:
                if self.mode == "radian":
                    statement_middle = str(math.sin(float(statement[start_position + 4:end_position - 1])))
                else:
                    statement_middle = str(math.sin(float(statement[start_position + 4:end_position - 1] * 180/math.pi)))
                statement = statement[:start_position] + statement_middle + statement[end_position:]

        if self.verbose:
            print(statement)
        return eval(statement)

