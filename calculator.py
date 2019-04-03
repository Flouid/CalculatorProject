import math


class Client:
    """The software representation of the calculator. Instance variables represent modes.
    The primary purpose of this code is to take some statement from the user and parse it into
    a statement that python's eval() function can recognize and evaluate."""

    # default modes
    default_verbose = False
    default_angle_measure = "radians"
    default_round_to = 4

    # Lists of characters and functions that the calculator should be able to parse
    valid_characters = "1234567890" \
                       "\u03C0"  # pi
    unicode_characters = "\u03C0"
    valid_functions = "sin("

    def __init__(self, verbose=default_verbose, angle_measure=default_angle_measure, round_to=default_round_to):
        self.verbose = verbose
        self.angle_measure = angle_measure
        self.round_to = round_to

    def parse(self, statement):
        """Passed the user's statement and attempts to parse it into something evaluable"""

        # Removes whitespace if there is any
        statement = statement.replace(" ", "")

        # Ensures all parentheses closed
        if "(" in statement:
            if statement.find(")", statement.rfind("(")) == -1:
                statement = statement + ")"

        # Ensures that all parentheses with a coefficient have proper multiplication operators I.e. a(b)c => a*(b)*c
        i = 1
        while i < len(statement) - 1:
            if i > 0:
                if (statement[i] == "(") & ((statement[i - 1] in self.valid_characters) | (statement[i - 1] == ")")):
                    statement = statement[:i] + "*" + statement[i:]
            if (statement[i] == ")") & ((statement[i + 1] in self.valid_characters) | (statement[i + 1] == "(")):
                    statement = statement[:i + 1] + "*" + statement[i + 1:]
            i += 1

        # Ensures that every unicode character variable with coefficients has proper multiplication operators
        for character in self.unicode_characters:
            if character in statement:
                i = 0
                while i < len(statement) - 1:
                    if i > 0:
                        if (statement[i] == character) & (statement[i - 1] in self.valid_characters):
                            statement = statement[:i] + "*" + statement[i:]
                    if (statement[i] == character) & (statement[i + 1] in self.valid_characters):
                        statement = statement[:i + 1] + "*" + statement[i + 1:]
                    i += 1

        # Converts the character for pi into the mathematical value for pi.
        if "\u03C0" in statement:
            statement = statement.replace("\u03C0", str(math.pi))

        # Converts strings in the form "sin(a)" into the actual value of sin(a)
        statement = self.function_parse("sin(", statement)
        print(statement)
        '''if "sin(" in statement:
            if (statement[statement.find("sin(") - 1] in self.valid_characters)
                    | (statement[statement.find("sin(") - 1] == ")") & (statement.find("sin(") > 0):
                statement = statement[:statement.find("sin(")] + "*" + statement[statement.find("sin("):]
            count = statement.count("sin(")
            start_position = 0
            end_position = 0
            for i in range(0, count):
                start_position = statement.find("sin(", start_position)
                end_position = statement.find(")", end_position) + 1
                if self.angle_measure == "radians":
                    sin_value = math.sin(float(eval(statement[start_position + 4:end_position - 1])))
                else:
                    sin_value = math.sin(float(eval(statement[start_position + 4:end_position - 1]))
                                         * (math.pi/180))  # degree conversion

                statement = statement[:start_position] + str(sin_value) + statement[end_position:]'''

        result = round(eval(statement), self.round_to)
        if float(result).is_integer():  # removes unnecessary zeros if the result is an integer
            result = int(result)
        return result

    def function_parse(self, function, statement):
        if function in statement:
            if (statement[statement.find(function) - 1] in self.valid_characters) \
                    | (statement[statement.find(function) - 1] == ")") & (statement.find(function) > 0):
                statement = statement[:statement.find(function)] + "*" + statement[statement.find(function):]
            count = statement.count(function)
            start_position = 0
            end_position = 0
            for i in range(0, count):
                start_position = statement.find(function, start_position)
                end_position = statement.find(")", end_position) + 1
                if function == "sin(":
                    if self.angle_measure == "radians":
                        sin_value = math.sin(self.parse(statement[start_position + len(function):end_position - 1]))
                    else:
                        sin_value = math.sin(self.parse(statement[start_position + len(function):end_position - 1])
                                             * (math.pi/180))  # degree conversion
                    return statement[:start_position] + str(sin_value) + statement[end_position:]
                else:
                    return statement
        else:
            return statement
