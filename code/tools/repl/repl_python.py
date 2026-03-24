
def simple_repl() -> None:

    while True:
        try:
            user_input = input(">> ")
            try:
                # Try evaluating as an expression
                result = eval(user_input)
                if result is not None:
                    print(result)
            except:
                # If not an expression, execute as a statement
                exec(user_input)
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

simple_repl()
