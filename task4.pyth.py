
from pathlib import Path

# Create a folder for forensic analysis
folder = Path("forensics_data")
folder.mkdir(exist_ok=True)

# Create sample files
(folder / "attendance.txt").write_text(
    "192311001,Arun,P\n"
    "192311002,Divya,A\n",
    encoding="utf-8"
)

(folder / "damaged.txt").write_text(
    "192311003,Kavin\n"
    "192311004,Meena,L\n",
    encoding="utf-8"
)

# Create an error log
log_file = folder / "forensics_report.txt"

print("FILE AND EXCEPTION FORENSICS")
print("-----------------------------")

with open(log_file, "w", encoding="utf-8") as log:

    for file_path in sorted(folder.glob("*.txt")):

        if file_path.name == "forensics_report.txt":
            continue

        print("\nFile:", file_path.name)
        log.write(f"\nFile: {file_path.name}\n")

        try:
            with open(file_path, "r", encoding="utf-8") as file:

                for line_number, line in enumerate(file, start=1):

                    parts = line.strip().split(",")

                    if len(parts) != 3:
                        message = (
                            f"Line {line_number}: Invalid number of fields"
                        )
                        print(message)
                        log.write(message + "\n")

                    elif parts[2] not in ("P", "A"):
                        message = (
                            f"Line {line_number}: Invalid attendance status"
                        )
                        print(message)
                        log.write(message + "\n")

                    else:
                        print(f"Line {line_number}: Valid record")

        except FileNotFoundError:
            print("Error: File not found")

        except PermissionError:
            print("Error: Permission denied")

# Test missing file
print("\nMISSING FILE TEST")

try:
    with open(folder / "missing.txt", "r") as file:
        file.read()

except FileNotFoundError:
    print("Missing file detected successfully.")

print("\nForensic analysis completed.")
print("Report saved as:", log_file)
