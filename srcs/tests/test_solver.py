import unittest
import os
from math import sqrt

import computorv1.solver as solver


class TestSolver(unittest.TestCase):
	context_path = os.path.split(os.path.dirname(__file__))[0] + "/computorv1"
	pos_eq = "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0"
	neg_eq = "7 * X^0 + 5 * X^1 + 3 * X^2 = 0"
	null = open(os.devnull, 'w')

	def test_check_n_format_true(self):
		check = solver.Equation(self.pos_eq)
		self.assertEqual(self.pos_eq, str(check))

		check = solver.Equation(self.neg_eq)
		self.assertEqual(self.neg_eq, str(check))

		eq = "5 * X^0 = 5 * X^0"
		check = solver.Equation(eq)
		self.assertEqual(eq, str(check))

		eq = "5*X^0=5*X^0"
		check = solver.Equation(eq)
		self.assertEqual('5 * X^0 = 5 * X^0', str(check))

		eq = "5    *X^0=5*X^0"
		check = solver.Equation(eq)
		self.assertEqual('5 * X^0 = 5 * X^0', str(check))

		eq = "5    *X^0   =   5*\tX^0"
		check = solver.Equation(eq)
		self.assertEqual('5 * X^0 = 5 * X^0', str(check))

		eq = "5 * X^0=5 * X^0"
		check = solver.Equation(eq)
		self.assertEqual('5 * X^0 = 5 * X^0', str(check))

	def test_check_n_format_raise(self):
		eq = "5 * X^0="
		with self.assertRaises(ArithmeticError):
			check = solver.Equation(eq)
			self.assertEqual(None, check.input)

		eq = "zzzzzz"
		with self.assertRaises(ArithmeticError):
			check = solver.Equation(eq)
			self.assertEqual(None, check.input)

		eq = "0 = 0"
		with self.assertRaises(ArithmeticError):
			check = solver.Equation(eq)
			self.assertEqual(None, check.input)

		eq = "5 * X^ + "
		with self.assertRaises(ArithmeticError):
			check = solver.Equation(eq)
			self.assertEqual(None, check.input)

		eq = "5 * X^0 = 5 * X^0 toto"
		with self.assertRaises(ArithmeticError):
			check = solver.Equation(eq)
			self.assertEqual(None, check.input)

		eq = "5 * X^0 + toto - 1 * X^1 = 5 * X^0"
		with self.assertRaises(ArithmeticError):
			check = solver.Equation(eq)
			self.assertEqual(None, check.input)

		eq = "5 * X^0.1 - 1 * X^1 = 5 * X^0"
		with self.assertRaises(ArithmeticError):
			check = solver.Equation(eq)
			self.assertEqual(None, check.input)

		eq = ".0 * X^0 + 1 * X^1 = 5 * X^0"
		with self.assertRaises(ArithmeticError):
			check = solver.Equation(eq)
			self.assertEqual(None, check.input)

		eq = "5 + X^0 = 5 * X^0"
		with self.assertRaises(ArithmeticError):
			check = solver.Equation(eq)
			self.assertEqual(None, check.input)

	def test__get_reduced_form(self):
		check = solver.Equation(self.pos_eq)
		self.assertEqual({'X^1': 4.0, 'X^0': 4.0, 'X^2': -9.3}, check._process_reduced_form())

		check = solver.Equation(self.neg_eq)
		self.assertEqual({'X^1': 5.0, 'X^0': 7.0, 'X^2': 3.0}, check._process_reduced_form())

	def test_get_degree(self):
		check = solver.Equation(self.pos_eq)
		self.assertEqual(2, check._process_degree())

		check = solver.Equation(self.neg_eq)
		self.assertEqual(2, check._process_degree())

		check = solver.Equation("5 * X^0 = 5 * X^0")
		self.assertEqual(0, check._process_degree())

		check = solver.Equation("6 * X^0 = 5 * X^0")
		self.assertEqual(0, check._process_degree())

		check = solver.Equation("6 * X^1 = 5 * X^0")
		self.assertEqual(1, check._process_degree())

		check = solver.Equation("5 * X^1 = 5 * X^1")
		self.assertEqual(0, check._process_degree())

		check = solver.Equation("5 * X^2 = 5 * X^2")
		self.assertEqual(0, check._process_degree())

		check = solver.Equation("5 * X^2 + 7 * X^1 = 5 * X^2")
		self.assertEqual(1, check._process_degree())

	def test_solve_two(self):
		check = solver.Equation(self.pos_eq)
		check.solve()
		self.assertEqual(164.8, check.discriminant)
		self.assertEqual((-0.47513146390886934, 0.9052389907905898), check.solution)

		check = solver.Equation(self.neg_eq)
		check.solve()
		self.assertEqual(-59., check.discriminant)
		self.assertEqual(('-0.833333333333 + i1.28019095798',
		                  '-0.833333333333 - i1.28019095798'), check.solution)

	def test_solve_one(self):
		check = solver.Equation("6 * X^1 = 5 * X^0")
		check.solve()
		self.assertIsNone(check.discriminant)
		self.assertEqual((0.8333333333333334,), check.solution)

	def test_solve_zero(self):
		check = solver.Equation("5 * X^0 = 5 * X^0")
		check.solve()
		self.assertIsNone(check.discriminant)
		self.assertEqual((True,), check.solution)

		check = solver.Equation("6 * X^0 = 5 * X^0")
		check.solve()
		self.assertIsNone(check.discriminant)
		self.assertEqual((False,), check.solution)

	def test_solve_three(self):
		check = solver.Equation("6 * X^3 = 5 * X^0")
		check.solve()
		self.assertIsNone(check.discriminant)
		self.assertEqual((False,), check.solution)

	def test_display_solution_d2(self):
		# d2 > 0
		expect = ['Reduced form: 4 * X^0 + 4 * X^1 - 9.3 * X^2 = 0',
		          'Polynomial degree: 2',
		          'Discriminant is strictly positive, the two solutions are:',
		          '-0.475131463909',
		          '0.905238990791']
		check = solver.Equation(self.pos_eq)
		message = check._build_display_message()
		self.assertEqual(expect, message)

		expect = ['Reduced form: 7 * X^0 + 5 * X^1 + 3 * X^2 = 0',
		          'Polynomial degree: 2',
		          'Discriminant is strictly negative, the two solutions are:',
		          '-0.833333333333 + i1.28019095798',
		          '-0.833333333333 - i1.28019095798']
		check = solver.Equation(self.neg_eq)
		message = check._build_display_message()
		self.assertEqual(expect, message)

		expect = ['Reduced form: -3 * X^2 = 0',
		          'Polynomial degree: 2',
		          'Discriminant is null, the solution is:',
		          '0']
		check = solver.Equation("       0=0*X^0+0*X^1+3*X^2")
		message = check._build_display_message()
		self.assertEqual(expect, message)

	def test_display_solution_d1(self):
		# Degree 1
		expect = ['Reduced form: -5 * X^0 + 6 * X^1 = 0',
		          'Polynomial degree: 1',
		          'The solution is:',
		          '0.833333333333']
		check = solver.Equation("6*X^1 = 5 * X^0")
		message = check._build_display_message()
		self.assertEqual(expect, message)

		expect = ['Reduced form: 6 * X^1 = 0',
		          'Polynomial degree: 1',
		          'The solution is:', '0']
		check = solver.Equation("6 * X^1 = 0")
		message = check._build_display_message()
		self.assertEqual(expect, message)

	def test_display_solution_d0(self):
		# Degree 0 All solutions
		expect = ['No reduced form', 'Polynomial degree: 0', 'Every complex number is solution']
		check = solver.Equation("5 * X^0 = 5 * X^0")
		message = check._build_display_message()
		self.assertEqual(expect, message)

		# Degree 0 No solution
		expect = ['Reduced form: 1 * X^0 = 0', 'Polynomial degree: 0', 'There is no solution']
		check = solver.Equation("6 * X^0 = 5 * X^0")
		message = check._build_display_message()
		self.assertEqual(expect, message)

	def test_display_solution_d3(self):
		expect = ['Reduced form: -5 * X^0 + 5 * X^3 = 0',
		          'Polynomial degree: 3',
		          "The polynomial degree is strictly greater than 2, I can't solve"]
		check = solver.Equation("5 * X^3 = 5 * X^0")
		message = check._build_display_message()
		self.assertEqual(expect, message)

	def test_display_solution(self):
		check = solver.Equation(self.neg_eq)
		null = os.open("/dev/null", 777)
		check.display_solution(null)

	def test_sqrt(self):
		for i in range(0, 50):
			self.assertEqual(sqrt(i), solver.my_sqrt(i))
			self.assertEqual(sqrt(float(i) / 2), solver.my_sqrt(float(i) / 2))
		with self.assertRaises(ValueError):
			solver.my_sqrt(-5)
		with self.assertRaises(TypeError):
			solver.my_sqrt("5")