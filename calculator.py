import math
import re


class Calculator:
    """The software representation of the calculator. Instance variables represent modes.
    The primary purpose of this code is to take some statement from the user and parse it into
    a statement that python's eval() function can recognize and evaluate."""

    # default modes
    default_verbose = False
    default_angle_measure = 'radians'
    default_round_to = 4

    # Lists of characters, functions, and variables that the calculator should be able to parse
    valid_characters = '1234567890\u03C0'
    valid_names = 'pi', 'root('
    unicode_characters = '\u03C0'
    valid_functions = 'sin(', 'cos(', 'tan(', 'arcsin(', 'arccos(', 'arctan(', '\u221A('

    def __init__(self, verbose=default_verbose, angle_measure=default_angle_measure, round_to=default_round_to):
        self.verbose = verbose
        self.angle_measure = angle_measure
        self.round_to = round_to

    # noinspection PyTypeChecker
    def parse(self, statement, rounding=True):
        """Passed the user's statement and attempts to parse it into something evaluable.
        The rounding argument is meant for recursive calls. There are several points in this function
        when it has to call itself, when it does so it cannot lose precision at intermediate steps by rounding"""

        # Removes whitespace if there is any
        if ' ' in statement:
            statement = statement.replace(' ', '')
            if self.verbose:
                print('removed the white space from ' + statement)

        # Replaces names of variables with single character unicode representations
        for name in self.valid_names:
            if name in statement:
                if name == 'pi':
                    statement = statement.replace(name, '\u03C0')
                    if self.verbose:
                        print('replaced pi with \u03C0 in ' + statement)
                if name == 'root(':
                    statement = statement.replace(name, '\u221A(')
                    if self.verbose:
                        print('replaced root( with \u221A( in ' + statement)

        # Logic for dealing with parentheses
        if '(' in statement:

            # Ensures final parentheses closed
            while statement.count('(') > statement.count(')'):
                statement = statement + ')'
                if self.verbose:
                    print('closed all parentheses in ' + statement)

            # Ensures that all parentheses with a coefficient have proper multiplication operators I.e. a(b)c => a*(b)*c
            i = 1
            while i < len(statement) - 1:
                if i > 0:
                    if (statement[i] == '(') & ((statement[i - 1] in self.valid_characters) | (statement[i - 1] == ')')):
                        statement = statement[:i] + '*' + statement[i:]
                if (statement[i] == ')') & ((statement[i + 1] in self.valid_characters) | (statement[i + 1] == '(')):
                        statement = statement[:i + 1] + '*' + statement[i + 1:]
                i += 1
            if self.verbose:
                print('ensured proper operators around parentheses in ' + statement)

        # Ensures that every unicode character variable with coefficients has proper multiplication operators
        for character in self.unicode_characters:
            if character in statement:
                i = 0
                while i < len(statement) - 1:
                    if i > 0:
                        if (statement[i] == character) & (statement[i - 1] in self.valid_characters):
                            statement = statement[:i] + '*' + statement[i:]
                    if (statement[i] == character) & (statement[i + 1] in self.valid_characters):
                        statement = statement[:i + 1] + '*' + statement[i + 1:]
                    i += 1
                if self.verbose:
                    print('ensured proper operators around ' + character + ' in ' + statement)

        # Converts the character for pi or the word 'pi' into the mathematical value for pi.
        if '\u03C0' in statement:
            statement = statement.replace('\u03C0', str(math.pi))
            if self.verbose:
                print('pi converted to numerical value in ' + statement)

        # Runs parsing logic on every function
        for function in self.valid_functions:
            if function in statement:

                # Checks if the function also contains arc, if so it skips this iteration of the loop
                if statement.find(function) != 0:
                    if statement[statement.find(function) - 1] == 'c':
                        continue

                # Ensures there is a multiplication operator between all instances of the function and any coefficients
                count = statement.count(function[0])
                position = 1
                i = 0
                while i < count:
                    position = statement.find(function[0], position)
                    if position == -1:
                        break
                    elif (statement[position - 1] in self.valid_characters) | (statement[position - 1] == ')'):
                        statement = statement[:position] + '*' + statement[position:]
                        position += 2  # account for new * character and move position to just after the first letter
                    else:
                        position += 1  # check the next character
                if self.verbose:
                    print('ensured all instances of ' + function + ' have proper operators in ' + statement)

                # Converts the statement to a list of terms separated by operators
                terms = re.split('([*+\-/])', statement)
                position = 0
                while position < len(terms) - 1:
                    if (terms[position].count('(') > terms[position].count(')')) & (terms[position].count('(') > 0):
                        terms[position:position + 2] = [''.join(terms[position:position + 2])]
                    else:
                        position += 1
                if self.verbose:
                    print('converted the statement to a list of terms ' + str(terms))

                # Replaces function terms with their decimal values
                for i in range(0, len(terms)):
                    if function in terms[i]:

                        inside = self.parse(terms[i][len(function):len(terms[i]) - 1], False)
                        if self.verbose:
                            print('the inside of the ' + function + ' function is ' + str(inside))

                        if function == 'sin(':
                            if self.angle_measure == 'radians':
                                terms[i] = math.sin(inside)
                            else:
                                terms[i] = math.sin(inside * (math.pi/180))
                            if self.verbose:
                                print('evaluated sin(' + str(inside) + ') as ' + str(terms[i]))

                        if function == 'cos(':
                            if self.angle_measure == 'radians':
                                terms[i] = math.cos(inside)
                            else:
                                terms[i] = math.cos(inside * (math.pi/180))
                            if self.verbose:
                                print('evaluated cos(' + str(inside) + ') as ' + str(terms[i]))

                        if function == 'tan(':
                            if self.angle_measure == 'radians':
                                terms[i] = math.tan(inside)
                            else:
                                terms[i] = math.tan(inside * (math.pi/180))
                            if self.verbose:
                                print('evaluated tan(' + str(inside) + ') as ' + str(terms[i]))

                        if function == 'arcsin(':
                            if self.angle_measure == 'radians':
                                terms[i] = math.asin(inside)
                            else:
                                terms[i] = math.asin(inside * (math.pi/180))
                            if self.verbose:
                                print('evaluated arcsin(' + str(inside) + ') as ' + str(terms[i]))

                        if function == 'arccos(':
                            if self.angle_measure == 'radians':
                                terms[i] = math.acos(inside)
                            else:
                                terms[i] = math.acos(inside * (math.pi/180))
                            if self.verbose:
                                print('evaluated arcsin(' + str(inside) + ') as ' + str(terms[i]))

                        if function == 'arctan(':
                            if self.angle_measure == 'radians':
                                terms[i] = math.atan(inside)
                            else:
                                terms[i] = math.atan(inside * (math.pi/180))
                            if self.verbose:
                                print('evaluated arcsin(' + str(inside) + ') as ' + str(terms[i]))

                        if function == '\u221A(':
                            if self.angle_measure == 'radians':
                                terms[i] = math.sqrt(inside)
                            else:
                                terms[i] = math.sqrt(inside * (math.pi/180))
                            if self.verbose:
                                print('evaluated \u221A(' + str(inside) + ') as ' + str(terms[i]))

                # Recombines the list of terms into a statement string
                statement = ''
                for term in terms:
                    statement = statement + str(term)
        if self.verbose & rounding:
            print('final statement is ' + statement)
            print()
        result = eval(statement)
        if float(result).is_integer():  # removes unnecessary zeros if the result is an integer
            result = int(result)
        if rounding:
            return round(result, self.round_to)
        else:
            return result
