class LogicCalculator:
    def __init__(self):
        self.history = []
        self.variables = {}

    def evaluate(self, expr, var_values=None):
        try:
            expr_proc = expr

            if var_values:
                for var, val in var_values.items():
                    expr_proc = expr_proc.replace(var, str(val))

            expr_proc = expr_proc.replace('1', 'True').replace('0', 'False')

            result = eval(expr_proc)

            if isinstance(result, bool):
                return result, None
            else:
                return None, "Не логическое значение"
        except SyntaxError as e:
            return None, f"Синтаксическая ошибка: {e}"
        except Exception as e:
            return None, str(e)

    def extract_variables(self, expr):
        operators = ['and', 'or', 'not', 'xor', '==', '!=', '(', ')',
                     'True', 'False', '1', '0', 'true', 'false']

        for op in '()':
            expr = expr.replace(op, ' ')

        words = expr.split()

        variables = set()
        for word in words:
            word = word.strip()
            if word and word.lower() not in operators:
                if word not in ['True', 'False', 'true', 'false']:
                    variables.add(word)

        return sorted(list(variables))

    def validate_expression(self, expr):
        logical_ops = ['and', 'or', 'not', 'xor', '==', '!=']

        words = expr.replace('(', ' ').replace(')', ' ').split()

        has_operator = False
        for word in words:
            if word in logical_ops:
                has_operator = True
                break

        variables = self.extract_variables(expr)
        if len(variables) > 1 and not has_operator:
            return False, "Между переменными должны быть операторы"

        if ')' in expr and '(' in expr:
            for i in range(len(expr) - 1):
                if expr[i] == ')' and expr[i + 1].isalpha():
                    return False, "После закрывающей скобки должен быть оператор"
                if expr[i].isalpha() and expr[i + 1] == '(':
                    return False, "Перед открывающей скобкой должен быть оператор"

        return True, "OK"

    def generate_truth_table(self, expression):
        if not expression:
            print("Ошибка: не указано выражение!")
            print("Пример: /table (A and B) or C")
            return None

        is_valid, error_msg = self.validate_expression(expression)
        if not is_valid:
            print(f"Ошибка в выражении: {error_msg}")
            print("Правильные примеры:")
            print("• (A and B) or C")
            print("• A and B or not C")
            return None

        variables = self.extract_variables(expression)

        if not variables:
            print("В выражении нет переменных!")
            print("Пример: /table (A and B) or C")
            return None

        n = len(variables)

        print(f"\nТаблица истинности для: {expression}")
        print("=" * (n * 8 + 20))

        header = " | ".join(variables) + " | Result"
        print(header)
        print("-" * len(header))

        results = []
        has_errors = False

        for i in range(2 ** n):
            values = {}
            row_values = []

            for j in range(n):
                val = (i >> (n - 1 - j)) & 1
                var_name = variables[j]
                values[var_name] = bool(val)
                row_values.append(str(val))

            result, error = self.evaluate(expression, values)

            if error:
                print(f"Ошибка при вычислении: {error}")
                has_errors = True
                break
            else:
                result_str = str(int(result))
                result_val = result
                results.append(result_val)

                row = " | ".join(row_values) + f" | {result_str}"
                print(row)

        if not has_errors:
            print("=" * (n * 8 + 20))

            if results:
                true_count = sum(1 for r in results if r)
                false_count = len(results) - true_count
                print(f"\nРезультаты: ИСТИНА - {true_count}, ЛОЖЬ - {false_count}")

        return variables, results

    def check_syntax(self, expr):
        words = expr.split()

        for i, word in enumerate(words):
            if word == 'not':
                if i + 1 >= len(words):
                    return False, "not в конце выражения"
                if words[i + 1] in ['and', 'or', 'xor', '==', '!=']:
                    return False, "после not должен быть операнд"
            elif word in ['and', 'or', 'xor']:
                if i == 0 or i == len(words) - 1:
                    return False, f"{word} не может быть в начале или конце"

        for i in range(len(words) - 1):
            if words[i] in ['True', 'False'] and words[i + 1] == 'not':
                return False, "not должен быть ПЕРЕД True/False"

        return True, "OK"

    def show_help(self):
        print("\n" + "=" * 50)
        print("СПРАВКА ПО КОМАНДАМ")
        print("=" * 50)
        print("/table <выражение>   - построить таблицу истинности")
        print("<выражение>           - вычислить значение")
        print("/help                 - показать справку")
        print("/exit                 - выход")
        print("-" * 50)
        print("ПРИМЕРЫ ВЫРАЖЕНИЙ:")
        print("• (A and B) or C")
        print("• A and B or not C")
        print("• (A or B) and (C or D)")
        print("• not (A and B)")
        print("=" * 50)

    def run(self):
        print("=" * 50)
        print("ЛОГИЧЕСКИЙ КАЛЬКУЛЯТОР")
        print("=" * 50)
        print("Введите /help для списка команд")
        print("=" * 50)

        while True:
            text = input("\n> ").strip()

            if text.lower() == '/exit':
                print("До свидания!")
                break
            elif text.lower() == '/help':
                self.show_help()
                continue
            elif not text:
                continue

            if text.startswith('/table'):
                if text == '/table' or text == '/table ':
                    print("Ошибка: нужно указать выражение!")
                    print("Пример: /table (A and B) or C")
                else:
                    expr = text[7:].strip()
                    self.generate_truth_table(expr)

            elif text.startswith('/'):
                print(f"Неизвестная команда: {text}")
                print("Введите /help для списка команд")

            else:
                expressions = [e.strip() for e in text.split(';') if e.strip()]

                print("\n" + "-" * 40)

                for i, expr in enumerate(expressions, 1):
                    print(f"\n{i}. Выражение: {expr}")

                    is_valid, error_msg = self.check_syntax(expr)

                    if not is_valid:
                        print(f"Ошибка: {error_msg}")
                        continue

                    is_valid, error_msg = self.validate_expression(expr)
                    if not is_valid:
                        print(f"Ошибка: {error_msg}")
                        continue

                    variables = self.extract_variables(expr)

                    if variables:
                        print(f"Найдены переменные: {', '.join(variables)}")
                        print(f"Используйте /table для таблицы истинности")
                    else:
                        result, error = self.evaluate(expr)

                        if error:
                            print(f"Ошибка: {error}")
                        else:
                            if result:
                                print(f"= ИСТИНА (True)")
                            else:
                                print(f"= ЛОЖЬ (False)")

                print("\n" + "-" * 40)


if __name__ == "__main__":
    calc = LogicCalculator()
    calc.run()