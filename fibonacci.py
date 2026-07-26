import math
import time


def generate_fibonacci(n):
    fibonacci = []
    a, b = 0, 1

    for _ in range(n):
        fibonacci.append(a)
        a, b = b, a + b

    return fibonacci


def fibonacci_upto_limit(limit):
    fibonacci = []
    a, b = 0, 1

    while a <= limit:
        fibonacci.append(a)
        a, b = b, a + b

    return fibonacci


def is_perfect_square(num):
    root = int(math.sqrt(num))
    return root * root == num


def is_fibonacci(num):
    return (
        is_perfect_square(5 * num * num + 4)
        or is_perfect_square(5 * num * num - 4)
    )


def display_result(result):
    print("\nGenerated Fibonacci Series:\n")

    for i, number in enumerate(result, start=1):
        print(f"{i:2}. {number}")

    print("\n----------- Statistics -----------")
    print(f"Total Numbers : {len(result)}")
    print(f"First Number  : {result[0]}")
    print(f"Last Number   : {result[-1]}")


def save_to_file(result):
    choice = input("\nDo you want to save the result to a text file? (y/n): ")

    if choice.lower() == "y":
        with open("fibonacci_output.txt", "w") as file:
            file.write("Fibonacci Generator Output\n")
            file.write("=" * 35 + "\n\n")

            for i, number in enumerate(result, start=1):
                file.write(f"{i}. {number}\n")

            file.write("\n")
            file.write(f"Total Numbers: {len(result)}\n")
            file.write(f"First Number : {result[0]}\n")
            file.write(f"Last Number  : {result[-1]}\n")

        print("\n✅ Result saved successfully as 'fibonacci_output.txt'.")


def main():
    print("=" * 55)
    print("         FIBONACCI GENERATOR")
    print("               Version 1.0")
    print("         Developed by Muneeb Khan Dawar")
    print("=" * 55)

    while True:

        print("\nChoose an option:")
        print("1. Generate first N Fibonacci numbers")
        print("2. Generate Fibonacci numbers up to a limit")
        print("3. Check if a number is Fibonacci")
        print("4. Exit")

        choice = input("\nEnter your choice (1-4): ")

        if choice == "1":
            try:
                n = int(input("\nEnter how many Fibonacci numbers you want: "))

                if n <= 0:
                    print("Please enter a positive number.")
                    continue

                start = time.time()

                result = generate_fibonacci(n)

                end = time.time()

                display_result(result)

                print(f"\nExecution Time: {end-start:.6f} seconds")

                save_to_file(result)

            except ValueError:
                print("Invalid input! Please enter a valid integer.")

        elif choice == "2":
            try:
                limit = int(input("\nGenerate Fibonacci numbers up to: "))

                if limit < 0:
                    print("Please enter a non-negative number.")
                    continue

                start = time.time()

                result = fibonacci_upto_limit(limit)

                end = time.time()

                display_result(result)

                print(f"\nExecution Time: {end-start:.6f} seconds")

                save_to_file(result)

            except ValueError:
                print("Invalid input! Please enter a valid integer.")

        elif choice == "3":
            try:
                number = int(input("\nEnter a number: "))

                if number < 0:
                    print("Please enter a non-negative number.")
                    continue

                if is_fibonacci(number):
                    print(f"\n✅ {number} is a Fibonacci number.")
                else:
                    print(f"\n❌ {number} is NOT a Fibonacci number.")

            except ValueError:
                print("Invalid input! Please enter a valid integer.")

        elif choice == "4":
            print("\nThank you for using Fibonacci Generator!")
            print("Project developed by Muneeb Dawar")
            print("Goodbye!")
            break

        else:
            print("Invalid choice! Please select 1, 2, 3 or 4.")


if __name__ == "__main__":
    main()