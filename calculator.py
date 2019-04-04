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
    valid_functions = "sin(", "cos("

    def __init__(self, verbose=default_verbose, angle_measure=default_angle_measure, round_to=default_round_to):
        self.verbose = verbose
        self.angle_measure = angle_measure
        self.round_to = round_to

    def parse(self, statement):
        """Passed the user's statement and attempts to parse it into something evaluable"""

        # Removes whitespace if there is any
        if statement.__contains__(" "):
            statement = statement.replace(" ", "")
            if self.verbose:
                print("removed the white space from " + statement)
        # Logic for dealing with parentheses
        if "(" in statement:

            # Ensures final parentheses closed
            if statement.find(")", statement.rfind("(")) == -1:
                statement = statement + ")"
                if self.verbose:
                    print("closed all parentheses in " + statement)

            # Ensures that all parentheses with a coefficient have proper multiplication operators I.e. a(b)c => a*(b)*c
            i = 1
            while i < len(statement) - 1:
                if i > 0:
                    if (statement[i] == "(") & ((statement[i - 1] in self.valid_characters) | (statement[i - 1] == ")")):
                        statement = statement[:i] + "*" + statement[i:]
                if (statement[i] == ")") & ((statement[i + 1] in self.valid_characters) | (statement[i + 1] == "(")):
                        statement = statement[:i + 1] + "*" + statement[i + 1:]
                i += 1
            if self.verbose:
                print("ensured proper operators around parentheses in " + statement)

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
                if self.verbose:
                    print("ensured proper operators around " + character + " in " + statement)

        # Converts the character for pi into the mathematical value for pi.
        if "\u03C0" in statement:
            statement = statement.replace("\u03C0", str(math.pi))
            if self.verbose:
                print("pi converted to numerical value in " + statement)

        # Runs parsing logic on every function
        for function in self.valid_functions:
            if function in statement:

                # Ensures there is a multiplication operator between all instances of the function and any coefficients
                count = statement.count(function[0])
                print(count)
                position = 1
                i = 0
                while i < count:
                    position = statement.find(function[0], position)
                    if position == -1:
                        break
                    elif (statement[position - 1] in self.valid_characters) | (statement[position - 1] == ")"):
                        statement = statement[:position] + "*" + statement[position:]
                        position += 2  # account for new * character and move position to just after the first letter
                    else:
                        position += 1  # check the next character
                if self.verbose:
                    print("ensured all instances of " + function + " have proper operators in " + statement)

                # Converts all instances of the function to their decimal values and replaces them

                # Converts the statement to a list of terms separated by operators
                terms = re.split('(\\*|\\+|-|/)', statement)
                position = 0
                while position < len(terms) - 1:
                    if (terms[position].count("(") > terms[position + 1].count(")")) & (terms[position].count("(") > 0):
                        terms[position:position + 2] = [''.join(terms[position:position + 2])]
                    elif (terms[position].count("(") == terms[position + 1].count(")")) & (
                            terms[position].count("(") > 0):
                        terms[position:position + 2] = [''.join(terms[position:position + 2])]
                        position += 1
                    else:
                        position += 1
                if self.verbose:
                    print("converted the statement to a list of terms " + str(terms))

                # Replaces function terms with their decimal values
                for i in range(0, len(terms)):
                    if terms[i].__contains__(function):
                        if self.angle_measure == "radians":
                            print(terms[i][len(function):len(terms[i]) - 1])
                            terms[i] = math.sin(self.parse(terms[i][len(function):len(terms[i]) - 1]))
                        else:
                            terms[i] = math.sin(self.parse(terms[i][len(function):len(terms[i]) - 1]) * (math.pi/180))

                # Recombines the list of terms into a statement string
                statement = ''
                for term in terms:
                    statement = statement + str(term)

        result = round(eval(statement), self.round_to)
        if float(result).is_integer():  # removes unnecessary zeros if the result is an integer
            result = int(result)
        return result
