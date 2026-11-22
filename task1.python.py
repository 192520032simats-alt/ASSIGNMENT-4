
from decimal import Decimal, InvalidOperation

# Function to calculate the total mess bill
def total_mess_bills(filename):

    total = Decimal("0.00")
    report = []
    rejected = []

    try:
        with open(filename, "r", encoding="utf-8") as file:

            for line_number, line in enumerate(file, start=1):

                line = line.strip()

                if not line:
                    continue

                parts = line.split(",")

                if len(parts) != 3:
                    rejected.append(
                        (line_number, line, "Expected 3 fields")
                    )
                    continue

                register_no, name, amount_text = parts

                try:
                    amount = Decimal(amount_text.strip())

                    if amount < 0:
                        raise ValueError("Negative amount")

                except (InvalidOperation, ValueError):
                    rejected.append(
                        (line_number, line, "Invalid amount")
                    )
                    continue

                total += amount
                report.append(
                    f"{name.strip()} - Rs. {amount:.2f}"
                )

    except FileNotFoundError:
        print("Error: File not found:", filename)
        return

    print("MESS BILL REPORT")
    print("-------------------------")

    for record in report:
        print(record)

    print("-------------------------")
    print(f"Total Mess Bill: Rs. {total:.2f}")

    if rejected:
        print("\nREJECTED RECORDS")

        for item in rejected:
            print(item)


# Create sample input file automatically
input_file = "mess_oct.txt"

with open(input_file, "w", encoding="utf-8") as file:
    file.write(
        "192311001,Arun,1250.50\n"
        "192311002,Divya,1400.00\n"
        "192311003,Kavin,1150.75\n"
        "192311004,Meena,1300.00\n"
        "192311005,Ravi,invalid\n"
    )

# Run the program
total_mess_bills(input_file)
