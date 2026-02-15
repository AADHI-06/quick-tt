class InputService:
    @staticmethod
    def get_valid_int(prompt: str, min_val: int = None, max_val: int = None) -> int:
        while True:
            try:
                val = int(input(prompt))
                if min_val is not None and val < min_val:
                    print(f"Value must be at least {min_val}.")
                    continue
                if max_val is not None and val > max_val:
                    print(f"Value must be at most {max_val}.")
                    continue
                return val
            except ValueError:
                print("Invalid input. Please enter a number.")

    @staticmethod
    def get_valid_choice(prompt: str, choices: list) -> str:
        while True:
            val = input(prompt).strip().upper()
            if val in choices:
                return val
            print(f"Invalid choice. Must be one of: {', '.join(choices)}")
