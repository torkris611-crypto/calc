class LogicCalculator:
    def __init__(self):
        self.history = []

    def evaluate(self, expr):
        try:
            expr_proc = expr.replace('1', 'True').replace('0', 'False')

            result = eval(expr_proc)

            if isinstance(result, bool):
                self.history.append((expr, result))
                return result, None
            else:
                return None, "Не логическое значение"
        except SyntaxError as e:
            return None, f"Синтаксическая ошибка"
        except Exception as e:
            return None, str(e)

    def check_syntax(self, expr):
        words = expr.split()

        for i, word in enumerate(words):
            if word == 'not':
                if i + 1 >= len(words):
                    return False, "not в конце выражения"
                if words[i + 1] in ['and', 'or', 'xor', '==', '!=']:
                    return False, "после not должен быть операнд (True/False или выражение)"
            elif word in ['and', 'or', 'xor']:
                if i == 0 or i == len(words) - 1:
                    return False, f"{word} не может быть в начале или конце"

        for i in range(len(words) - 1):
            if words[i] in ['True', 'False'] and words[i + 1] == 'not':
                return False, "not должен быть ПЕРЕД True/False, а не после"

        return True, "OK"

    def run(self):
        print("ЛОГИЧЕСКИЙ КАЛЬКУЛЯТОР")
        print("=" * 50)
        print("ПРАВИЛЬНЫЕ ЗАПИСИ:")
        print("   not True")
        print("   not False")
        print("   True and not False")
        print("   not (True and False)")
        print("-" * 50)
        print("НЕПРАВИЛЬНЫЕ ЗАПИСИ:")
        print("   True not False  (not после True)")
        print("   True and False not  (not в конце)")
        print("   and True  (and в начале)")
        print("-" * 50)
        print("Вводите выражения через ;")
        print("Команда: exit - выход")
        print("=" * 50)

        while True:
            text = input("\n> ").strip()

            if text.lower() == 'exit':
                print("До свидания!")
                break
            elif not text:
                continue

            expressions = [e.strip() for e in text.split(';') if e.strip()]

            print("\n" + "-" * 40)

            for i, expr in enumerate(expressions, 1):
                print(f"\n{i}. Выражение: {expr}")


                is_valid, error_msg = self.check_syntax(expr)

                if not is_valid:
                    print(f"   Ошибка: {error_msg}")
                    if 'True not' in expr:
                        print(f"   Правильно: not {expr.replace('True not', '').strip()}")
                    elif 'False not' in expr:
                        print(f"   Правильно: not {expr.replace('False not', '').strip()}")
                    continue


                result, error = self.evaluate(expr)

                if error:
                    print(f"Ошибка: {error}")
                else:
                    if result:
                        print(f"ИСТИНА (True)")
                    else:
                        print(f"ЛОЖЬ (False)")

            print("\n" + "-" * 40)



if __name__ == "__main__":
    calc = LogicCalculator()
    calc.run()