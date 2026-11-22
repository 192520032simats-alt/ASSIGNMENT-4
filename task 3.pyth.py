
import os
import tempfile


# Custom exception
class InvalidRecord(Exception):
    """Raised when an attendance line is invalid."""


# Function to check each attendance line
def parse_line(line):

    parts = [part.strip() for part in line.strip().split(",")]

    if len(parts) != 3:
        raise InvalidRecord(
            f"expected 3 fields, found {len(parts)}"
        )

    register_no, date, status = parts

    if status not in ("P", "A"):
        raise InvalidRecord(f"invalid status '{status}'")

    return register_no, date, status


# Function to process attendance file
def summarise(path):

    present = 0
    absent = 0
    errors = []

    try:
        with open(path, "r", encoding="utf-8") as file:

            for line_number, line in enumerate(file, start=1):

                if not line.strip():
                    continue

                try:
                    register_no, date, status = parse_line(line)

                    if status == "P":
                        present += 1
                    else:
                        absent += 1

                except InvalidRecord as error:
                    errors.append((line_number, str(error)))

    except FileNotFoundError as error:
        raise FileNotFoundError(
            f"Attendance file not found: {path}"
        ) from error

    except PermissionError as error:
        raise PermissionError(
            f"Permission denied: {path}"
        ) from error

    except UnicodeDecodeError as error:
        raise UnicodeError(
            f"Invalid text encoding: {path}"
        ) from error

    else:
        print("File processing completed successfully.")

    finally:
        print("Processing attempt finished.")

    return present, absent, errors


# Create sample attendance data
data = (
    "192311001,2026-10-08,P\n"
    "192311002,2026-10-08,A\n"
    "192311003,2026-10-08\n"
    "192311004,2026-10-08,L\n"
)

# Create a temporary file
with tempfile.NamedTemporaryFile(
    "w",
    suffix=".csv",
    delete=False,
    encoding="utf-8"
) as tmp:

    tmp.write(data)
    file_name = tmp.name


# Process the attendance file
try:
    print("\nAttendance Result:")
    print(summarise(file_name))

except (FileNotFoundError, PermissionError, UnicodeError) as error:
    print("File error:", error)

finally:
    if os.path.exists(file_name):
        os.remove(file_name)


# Test missing file handling
print("\nMissing File Test:")

try:
    summarise("missing_attendance.csv")

except FileNotFoundError as error:
    print("Handled error:", error)
