import math
import re


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
    valid_functions = "sin", "cos"

    def __init__(self, verbose=default_verbose, angle_measure=default_angle_measure, round_to=default_round_to):
        self.verbose = verbose
        self.angle_measure = angle_measure
        self.round_to = round_to

    def parse(self, statement):
        """Passed the user's statement and attempts to parse it into something evaluable"""

        # Removes whitespace if there is any
        statement = statement.replace(" ", "")

        # Ensures final parentheses closed
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

        # Runs parsing logic on every function
        for function in self.valid_functions:
            if function in statement:

                # Ensures there is a multiplication operator between all instances of the function and any coefficients
                count = statement.count(function[0])
                position = 1
                for i in range(0, count):
                    position = statement.find(function[0], position)
                    if (statement[position - 1] in self.valid_characters) | (statement[position - 1] == ")"):
                        statement = statement[:position] + "*" + statement[position:]
                        position += 2  # account for new * character and move position to just after the first letter

                # Converts all instances of the function to their decimal values and replaces them
                terms = re.split('(\\*|\\+|-|/)', statement)
                for i in range(0, len(terms) - 1):
                    print(terms[i])
                    if terms[i].count("(") > terms[i + 1].count(")"):
                        print("i should do something about this")
                        terms[i:i + 2] = [''.join(terms[i:i + 2])]

                print(terms)

        result = round(eval(statement), self.round_to)
        if float(result).is_integer():  # removes unnecessary zeros if the result is an integer
            result = int(result)
        return result
