import unittest
from main import LogicCalculator

class TestLogicCalculatorEvaluate(unittest.TestCase):
    def setUp(self):
        self.calc = LogicCalculator()

    def test_basic_operations(self):
        test_cases = [
            ("True and False", False),
            ("True or False", True),
            ("not True", False),
            ("True != False", True),
            ("True != True", False),
        ]
        for expr, expected in test_cases:
            result, error = self.calc.evaluate(expr)
            self.assertIsNone(error)
            self.assertEqual(result, expected)

    def test_variable_substitution(self):
        result, error = self.calc.evaluate("A and B", {"A": True, "B": False})
        self.assertIsNone(error)
        self.assertFalse(result)

    def test_numeric_substitution(self):
        result, error = self.calc.evaluate("1 and 0")
        self.assertIsNone(error)
        self.assertFalse(result)

    def test_errors(self):
        result, error = self.calc.evaluate("A and B")
        self.assertIsNotNone(error)

        result, error = self.calc.evaluate("True and")
        self.assertIsNotNone(error)
        self.assertIn("Синтаксическая ошибка", error)

        result, error = self.calc.evaluate("5 + 3")
        self.assertIsNotNone(error)
        self.assertEqual(error, "Не логическое значение")


class TestLogicCalculatorExtractVariables(unittest.TestCase):
    def setUp(self):
        self.calc = LogicCalculator()

    def test_variable_names(self):
        test_cases = [
            ("A and B", ["A", "B"]),
            ("(A or B) and not C", ["A", "B", "C"]),
            ("A1 and B_2", ["A1", "B_2"]),
            ("A and A", ["A"]),
        ]
        for expr, expected in test_cases:
            variables = self.calc.extract_variables(expr)
            self.assertEqual(sorted(variables), sorted(expected))

    def test_ignore_operators(self):
        test_cases = [
            ("True and False", []),
            ("1 and 0", []),
            ("A != B == C", ["A", "B", "C"]),
        ]
        for expr, expected in test_cases:
            variables = self.calc.extract_variables(expr)
            self.assertEqual(variables, expected)


class TestLogicCalculatorValidateExpression(unittest.TestCase):
    def setUp(self):
        self.calc = LogicCalculator()

    def test_validation(self):
        test_cases = [
            ("A and B", True),
            ("A B", False),
            ("(A and B)C", False),
            ("A(B and C)", False),
            ("A", True),
            ("(A and B)", True),
        ]
        for expr, expected in test_cases:
            is_valid, _ = self.calc.validate_expression(expr)
            self.assertEqual(is_valid, expected)


class TestLogicCalculatorCheckSyntax(unittest.TestCase):
    def setUp(self):
        self.calc = LogicCalculator()

    def test_operator_positions(self):
        test_cases = [
            ("A and B", True),
            ("not A", True),
            ("A not", False),
            ("not and B", False),
            ("and A", False),
            ("A and", False),
            ("True not", False),
            ("A != B", True),
        ]
        for expr, expected in test_cases:
            is_valid, _ = self.calc.check_syntax(expr)
            self.assertEqual(is_valid, expected)


class TestLogicCalculatorGenerateTruthTable(unittest.TestCase):
    def setUp(self):
        self.calc = LogicCalculator()

    def test_table_generation(self):
        test_cases = [
            ("A and B", ["A", "B"], 4, 1),
            ("A or B", ["A", "B"], 4, 3),
            ("not A", ["A"], 2, 1),
            ("A != B", ["A", "B"], 4, 2),
        ]
        for expr, expected_vars, expected_rows, expected_true in test_cases:
            result = self.calc.generate_truth_table(expr)
            self.assertIsNotNone(result)
            variables, results = result
            self.assertEqual(variables, expected_vars)
            self.assertEqual(len(results), expected_rows)
            self.assertEqual(sum(results), expected_true)

    def test_error_cases(self):
        test_cases = [
            ("", None),
            ("A B", None),
            ("True", None),
        ]
        for expr, expected in test_cases:
            result = self.calc.generate_truth_table(expr)
            self.assertEqual(result, expected)


class TestLogicCalculatorIntegration(unittest.TestCase):
    def setUp(self):
        self.calc = LogicCalculator()

    def test_workflow(self):
        expr = "A and B"

        is_valid, _ = self.calc.check_syntax(expr)
        self.assertTrue(is_valid)

        is_valid, _ = self.calc.validate_expression(expr)
        self.assertTrue(is_valid)

        variables = self.calc.extract_variables(expr)
        self.assertEqual(variables, ["A", "B"])

        result = self.calc.generate_truth_table(expr)
        self.assertIsNotNone(result)

        for a in [True, False]:
            for b in [True, False]:
                result, error = self.calc.evaluate(expr, {"A": a, "B": b})
                self.assertIsNone(error)
                self.assertEqual(result, a and b)


class TestLogicCalculatorBoundary(unittest.TestCase):
    def setUp(self):
        self.calc = LogicCalculator()

    def test_edge_cases(self):
        test_cases = [
            ("", []),
            ("   ", []),
            ("not not A", ["A"]),
            ("(A)", ["A"]),
            ("A == B", ["A", "B"]),
            ("A != B", ["A", "B"]),
        ]
        for expr, expected_vars in test_cases:
            variables = self.calc.extract_variables(expr)
            self.assertEqual(variables, expected_vars)


if __name__ == "__main__":
    unittest.main()