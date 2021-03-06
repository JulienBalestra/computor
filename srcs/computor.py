#!/usr/bin/env python
import re
import os
import argparse


def my_sqrt(x):
    try:
        if x >= 0:
            return x ** 0.5
    except TypeError:
        raise TypeError("not an int or float type")
    raise ValueError("math domain error")


def convert_float(number):
    if number is None:
        return None
    if number - int(number) == 0:
        return int(number)
    return number


def my_abs(nb):
    if nb < 0:
        return -nb
    return nb


def my_hcf(a, b):
    """
    Highest Common Factor
    """
    if a - int(a) != 0 or b - int(b) != 0:
        raise TypeError
    a = int(a)
    b = int(b)
    if a == 0 or b == 0:
        raise ZeroDivisionError
    if my_abs(a) < my_abs(b):
        a, b = b, a
    r = a % b
    if r == 0:
        return b
    else:
        a, b = b, r
        return my_hcf(a, b)


def process_result(a, b):
    if a == 0:
        return 0
    if a - int(a) != 0 or b - int(b) != 0:
        return convert_float(a / b)
    hcf = my_hcf(a, b)
    a = a / hcf
    b = b / hcf
    if a < 11 and b < 101 and b != 1:
        result = str(convert_float(a)) + " / " + str(convert_float(b))
        if result.count("-") == 1:
            result = result.replace("-", "")
            result = "-" + result

        return result
    else:
        return convert_float(float(a) / float(b))


class Equation:
    error = "The equation is not coherent, should be quoted like \"5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0\""

    def __init__(self, eq_input, goodies=False):
        self.user_input = eq_input
        self.f_input = self._parse_input(eq_input)
        self.reduced = {}
        self.degree = None
        self.solution = None
        self.discriminant = None
        self.goodies = goodies

    @staticmethod
    def _translate_input(eq_input):
        for change in [("**", "^"), ("x", "X"), (" ", ""), ("\t", ""), ("\n", ""), (",", ".")]:
            eq_input = eq_input.replace(change[0], change[1])
        return eq_input

    @staticmethod
    def _format_natural_form(eq_input):
        try:
            left, right = Equation._translate_input(eq_input).split("=")
        except ValueError:
            raise ArithmeticError(Equation.error)

        def substitute(side):
            if re.match("^[\-\+]?0+\.?(0+)?$", side) is not None:
                return "0"

            regex_group = list()

            # Remove useless 0
            regex_group.append((re.compile("(?P<prev>^|\^|[\*\+\-])0+(?P<pow>([0-9]+))"),
                                "\g<prev>\g<pow>"))

            # 5X -> 5*X
            regex_group.append((re.compile("(?P<cf>([0-9]+(\.[0-9]+)?))(?P<unk>(X))"),
                                "\g<cf>*\g<unk>"))

            # X*2 -> 2*X
            regex_group.append((re.compile("(?P<unk>(X|X\^[0-9]+))[\*](?P<cf>([0-9]+(\.[0-9]+)?))"),
                                "\g<cf>*\g<unk>"))

            # 1 -> 1*X^0
            regex_group.append((re.compile("(?P<psign>(^|[\+\-]))(?P<cf>([0-9]+(\.[0-9]+)?))(?P<asign>([\+\-]|$))"),
                                "\g<psign>\g<cf>*X^0\g<asign>"))

            # X -> X^1
            regex_group.append((re.compile("(?P<unk>(X))(?P<asign>([\+\-]|$))"),
                                "\g<unk>^1\g<asign>"))

            # X -> 1*X
            regex_group.append((re.compile("(?P<psign>(^|[\+\-]))(?P<unk>(X))"),
                                "\g<psign>1*\g<unk>"))

            for regex in regex_group:
                change = True
                while change is True:
                    new_side = regex[0].sub(regex[1], side)
                    if new_side == side:
                        change = False
                    else:
                        side = new_side

            return side

        left = substitute(left)
        right = substitute(right)

        return left + "=" + right

    def _parse_input(self, eq_input):
        eq_input = self._format_natural_form(eq_input)

        pattern = "[\-\+]?([0-9]+\.?[0-9]*\*X\^[0-9]+[\+\-])*[0-9]+\.?[0-9]*\*X\^[0-9]+"
        if re.match(pattern + "=" + pattern + "$", eq_input) is not None:
            pass
        elif re.match(pattern + "=[\-\+]?0+\.?(0+)?$", eq_input) is not None:
            eq_input = eq_input.split("=")
            eq_input = eq_input[0] + "=0"
        elif re.match("[\-\+]?0+\.?(0+)?=" + pattern + "$", eq_input) is not None:
            eq_input = eq_input.split("=")
            eq_input = "0=" + eq_input[1]
        else:
            raise ArithmeticError(self.error)

        for sign in ["+", "-", "*", "="]:
            eq_input = eq_input.replace(sign, " %s " % sign)
        eq_input = eq_input.replace("=  +", "= ")

        while "  " in eq_input:
            eq_input = eq_input.replace("  ", " ")

        if " - " == eq_input[:3]:
            eq_input = eq_input[1:]
        elif " + " == eq_input[:3]:
            eq_input = eq_input[3:]

        return eq_input

    def __repr__(self):
        return self.f_input

    def _process_reduced_form(self):
        for power in re.findall("X\^([0-9]+)", self.__repr__()):
            power = int(power)
            if power > self.degree:
                self.degree = power
            self.reduced["X^" + str(power)] = 0
        self.f_input = self.f_input.replace("- ", "-").split(" ")

        side = 1  # if side == 1 : left part of the equation else side == -1
        for i, elt in enumerate(self.f_input):
            if elt in self.reduced:
                self.reduced[elt] += side * float(self.f_input[i - 2])
            elif elt == "=":
                side = -1
        return self.reduced

    def _process_degree(self):
        try:
            for i in range(self.degree, -1, -1):
                if self.get_value("X^" + str(i), self.reduced) != 0:
                    self.degree = i
                    return self.degree
            self.degree = 0
        except TypeError:
            self._process_reduced_form()
            self._process_degree()
        return self.degree

    @staticmethod
    def get_value(key, dictionary):
        try:
            return dictionary[key]
        except KeyError:
            return 0

    def _solve_zero(self):
        if self.get_value("X^0", self.reduced) == 0:
            self.solution = (True,)
        else:
            self.solution = (False,)

    def _solve_one(self):
        a = self.reduced["X^1"]
        b = self.get_value("X^0", self.reduced)
        self.solution = (process_result(-b, a),)

    def _solve_two(self):
        a = self.reduced["X^2"]
        b = self.get_value('X^1', self.reduced)
        c = self.get_value("X^0", self.reduced)
        self.discriminant = b * b - 4 * a * c
        if self.discriminant > 0:
            x1 = process_result((-b + my_sqrt(self.discriminant)), (2 * a))
            x2 = process_result((-b - my_sqrt(self.discriminant)), (2 * a))
            self.solution = x1, x2
        elif self.discriminant == 0:
            if b != 0 or a != 0:
                self.solution = (process_result(-b, (2 * a)),)
            else:
                self.solution = (0,)
        else:
            real = process_result(-b, (2 * a))
            imaginary = process_result(my_sqrt(- self.discriminant), (2 * a))
            x1 = str(real) + " + i" + str(imaginary)
            x2 = str(real) + " - i" + str(imaginary)
            self.solution = x1, x2

    def solve(self):
        if self.degree is None:
            self._process_reduced_form()
            self._process_degree()
            self.solve()

        elif self.degree == 0:
            self._solve_zero()
        elif self.degree == 1:
            self._solve_one()
        elif self.degree == 2:
            self._solve_two()
        else:
            self.solution = (False,)

    def _string_reduced_form(self):
        equation = []
        for i in range(self.degree + 1):
            if self.get_value("X^" + str(i), self.reduced) != 0:
                equation.append(str(convert_float(self.reduced["X^" + str(i)])))
                equation.append("*")
                equation.append("X^" + str(i))
                equation.append("+")
        if equation:
            equation.pop(-1)
            equation.append("=")
            equation.append("0")
            return "Reduced form: " + self._goodies_reduced(" ".join(equation).replace("+ -", "- "))
        return "No reduced form"

    def _goodies_degree(self, string):
        if self.goodies is True:
            return "\033[0;36m\033[1m[ %s ]\033[0m" % str(string)
        return str(string)

    def _goodies_reduced(self, string):
        if self.goodies is True:
            return "\033[0;33m\033[1m( %s )\033[0m" % string
        return string

    def _goodies_solution(self, string):
        if self.goodies is True:
            return "\033[0;32m\033[1m\t[ %s ]\033[0m" % str(string)
        return str(string)

    def build_display_message(self):
        if self.solution is None:
            self.solve()

        message = list()
        message.append("Original Equation: %s" % self.user_input)
        formatted = " ".join(self.f_input).replace("-", "- ")
        if formatted != self.user_input:
            message.append("Formatted Equation: %s" % formatted)
        message.append(self._string_reduced_form())
        message.append("Polynomial degree: %s" % self._goodies_degree(self.degree))
        if self.degree == 0:
            if self.solution == (False,):
                message.append("There is no solution")
            else:
                message.append("Every complex number is solution")
        elif self.degree == 1:
            message.append("The solution is:")
            message.append(self._goodies_solution(self.solution[0]))
        elif self.degree == 2:
            if self.discriminant > 0:
                message.append("Discriminant is strictly positive, the two solutions are:")
                message.append(self._goodies_solution(self.solution[0]))
                message.append(self._goodies_solution(self.solution[1]))
            elif self.discriminant == 0:
                message.append("Discriminant is null, the solution is:")
                message.append(self._goodies_solution(self.solution[0]))
            else:
                message.append("Discriminant is strictly negative, the two solutions are:")
                message.append(self._goodies_solution(self.solution[0]))
                message.append(self._goodies_solution(self.solution[1]))
        else:
            message.append("The polynomial degree is strictly greater than 2, I can't solve")
        return message

    def display_solution(self, fd=1):
        for line in self.build_display_message():
            os.write(fd, line + "\n")

    def get_discriminant(self):
        if self.discriminant is None and self.degree is None:
            self.solve()
        return convert_float(self.discriminant)

    def get_degree(self):
        if self.degree is None:
            return self._process_degree()
        return self.degree

    def get_reduced(self):
        if self.reduced == {}:
            return self._process_reduced_form()
        return self.reduced


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("equation", help="Should be quoted like \"5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0\"")
    args.add_argument('-g', '--goodies', type=bool, default=False, help='Activate the pretty print ?')
    args.add_argument('-e', '--error', type=bool, default=True, help='Add the python exception ?')
    goodies = args.parse_args().goodies
    if args.parse_args().error is True:
        try:
            solver = Equation(args.parse_args().equation, goodies=goodies)
            solver.solve()
            solver.display_solution()
        except ArithmeticError:
            os.write(2, "The equation is not coherent, should be quoted like :\n"
                        "\"5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0\"\n")
            exit(1)
    else:
        solver = Equation(args.parse_args().equation, goodies=goodies)
        solver.solve()
        solver.display_solution()