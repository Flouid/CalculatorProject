import math
import re


class Calculator:
    """The software representation of the calculator. Instance variables represent modes.
    The primary purpose of this code is to take some statement from the user and parse it into
    a statement that python's eval() function can recognize and evaluate."""

    # Instance variables
    result_history = []

    # default modes
    default_verbose = False
    default_angle_measure = 'radians'
    default_round_to = 4

    # Lists of characters, functions, variables, operators etc... that the calculator should be able to parse
    valid_characters = '1234567890\u03C0\U0001D452'
    valid_names = 'pi', 'root(', 'e'
    unicode_characters = '\u03C0', '\U0001D452'
    valid_functions = 'sin(', 'cos(', 'tan(', 'arcsin(', 'arccos(', 'arctan(', '\u221A(', '^(', 'log(', 'ln('
    valid_operators = '+-/*'
    special_functions = '^(', ''  # these are valid functions but need to be handled with different syntax

    def __init__(self, verbose=default_verbose, angle_measure=default_angle_measure, round_to=default_round_to):
        self.verbose = verbose
        self.angle_measure = angle_measure
        self.round_to = round_to

    # noinspection PyTypeChecker
    def parse(self, statement, rounding=True):
        """Passed the user's statement and attempts to parse it into something evaluable.
        The rounding argument is meant for recursive calls. There are several points in this function
        when it has to call itself, when it does so it cannot lose precision at intermediate steps by rounding"""

        if self.verbose & rounding:
            print('evaluating ' + statement)
            print()

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
                if name == 'e':
                    statement = statement.replace(name, '\U0001D452')
                    if self.verbose:
                        print('replaced e with \U0001D452 in ' + statement)

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

        # Converts the character for pi into the mathematical value for pi
        if '\u03C0' in statement:
            statement = statement.replace('\u03C0', str(math.pi))
            if self.verbose:
                print('pi converted to numerical value in ' + statement)

        # Converts the character for e into the mathematical value for e
        if '\U0001D452' in statement:
            statement = statement.replace('\U0001D452', str(math.e))
            if self.verbose:
                print('e converted into numerical value in ' + statement)

        # Runs parsing logic on every function
        for function in self.valid_functions:
            if function in statement:

                # Checks if the function also contains arc, if so it skips this iteration of the loop
                if statement.find(function) != 0:
                    if statement[statement.find(function) - 1] == 'c':
                        continue

                # Ensures there is a multiplication operator between all instances of the function and any coefficients
                if function not in self.special_functions:
                    count = statement.count(function[0])
                    position = 1
                    i = 0
                    while i < count:
                        position = statement.find(function[0], position)
                        if position == -1:
                            break
                        elif (statement[position - 1] in self.valid_characters) | (statement[position - 1] == ')'):
                            statement = statement[:position] + '*' + statement[position:]
                            position += 2  # account for new * character and move position to just after the next letter
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

                # Checks for terms surrounded by parentheses and replaces them with their parsed value
                for i in range(len(terms)):
                    if (terms[i][0] == '(') & (terms[i][len(terms[i]) - 1] == ')'):
                        terms[i] = str(self.parse(terms[i][1:len(terms[i]) - 1], False))

                # Replaces function terms with their decimal values
                for i in range(len(terms)):
                    if function in terms[i]:

                        # Logic for normal functions with the argument inside the parentheses
                        if function not in self.special_functions:
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
                                terms[i] = math.sqrt(inside)
                                if self.verbose:
                                    print('evaluated \u221A(' + str(inside) + ') as ' + str(terms[i]))

                            if function == 'log(':
                                # if inside < 0:
                                    # raise AssertionError("Cannot take the log of a negative value")
                                terms[i] = math.log10(inside)
                                if self.verbose:
                                    print('evaluated log(' + str(inside) + ') as ' + str(terms[i]))

                            if function == 'ln(':
                                if inside < 0:
                                    raise AssertionError("Cannot take the natural log of a negative value")
                                terms[i] = math.log(inside)
                                if self.verbose:
                                    print('evaluate ln(' + str(inside) + ') as ' + str(terms[i]))
                                    pass

                        # Parsing logic for special functions with part of their evaluation outside the parenthesis
                        # I.e functions like 4^(2) must become math.pow(4, 2)
                        else:
                            if function == '^(':
                                position = terms[i].find(function)  # find where the function occurs in the term
                                start_position = 0  # assume the beginning of the term is the base
                                if '(' in terms[i][:position]:
                                    # move the start position past any left parentheses in the term before the function
                                    start_position = terms[i].find('(') + 1
                                base = self.parse(terms[i][start_position:position], False)
                                exponent = self.parse(terms[i][position + len(function):len(terms[i]) -
                                                               terms[i].count(")", position)], False)
                                # takes the part of the term ignored earlier and concatenates the evaluated function
                                terms[i] = terms[i][:start_position] + str(math.pow(base, exponent))
                                if self.verbose:
                                    print(str(base) + '^(' + str(exponent) + ') converted to ' + terms[i])

                # Recombines the list of terms into a statement string
                statement = ''
                for term in terms:
                    statement += str(term)

        if self.verbose & rounding:
            print('final statement is ' + statement)
            print()

        result = eval(statement)

        if float(result).is_integer():  # removes unnecessary zeros if the result is an integer
            result = int(result)

        self.result_history += [result]

        if rounding:
            result = round(result, self.round_to)

        return result
