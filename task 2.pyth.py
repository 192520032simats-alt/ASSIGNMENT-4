
from pathlib import Path
import csv

# Create input and output folders
data_folder = Path("attendance_data")
output_folder = Path("attendance_output")

data_folder.mkdir(exist_ok=True)
output_folder.mkdir(exist_ok=True)

# Create sample daily attendance files
(data_folder / "day1.txt").write_text(
    "192311001,2026-10-08,P\n"
    "192311002,2026-10-08,A\n"
    "192311003,2026-10-08\n",
    encoding="utf-8"
)

(data_folder / "day2.txt").write_text(
    "192311001,2026-10-09,P\n"
    "192311002,2026-10-09,P\n"
    "192311003,2026-10-09,L\n",
    encoding="utf-8"
)

# Dictionary to store attendance counts
attendance = {}

# List to store damaged records
damaged = []

# Read all daily attendance files
for file_path in sorted(data_folder.glob("*.txt")):

    with open(file_path, "r", encoding="utf-8") as file:

        for line_number, line in enumerate(file, start=1):

            if not line.strip():
                continue

            parts = [part.strip() for part in line.strip().split(",")]

            # Check number of fields
            if len(parts) != 3:
                damaged.append(
                    (file_path.name, line_number,
                     line.strip(), "Expected 3 fields")
                )
                continue

            register_no, date, status = parts

            # Validate attendance record
            if not register_no or not date or status not in ("P", "A"):
                damaged.append(
                    (file_path.name, line_number,
                     line.strip(), "Missing field or invalid status")
                )
                continue

            # Initialise student record
            if register_no not in attendance:
                attendance[register_no] = {
                    "present": 0,
                    "absent": 0
                }

            # Update attendance count
            if status == "P":
                attendance[register_no]["present"] += 1
            else:
                attendance[register_no]["absent"] += 1

# Create attendance report
with open(output_folder / "attendance_report.csv",
          "w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)

    writer.writerow([
        "Register Number", "Present", "Absent",
        "Total", "Percentage", "Below 75%"
    ])

    for reg_no, counts in sorted(attendance.items()):

        present = counts["present"]
        absent = counts["absent"]
        total = present + absent

        percentage = (present / total * 100) if total else 0
        below_limit = "Yes" if percentage < 75 else "No"

        writer.writerow([
            reg_no, present, absent, total,
            f"{percentage:.2f}", below_limit
        ])

# Create damaged-record log
with open(output_folder / "damaged_records.log",
          "w", encoding="utf-8") as file:

    for item in damaged:
        file.write(" | ".join(map(str, item)) + "\n")

# Display final results
print("Attendance processing completed.")
print("Valid students:", len(attendance))
print("Damaged records:", len(damaged))

print("\nStudents below 75% attendance:")

for reg_no, counts in sorted(attendance.items()):
    total = counts["present"] + counts["absent"]
    percentage = counts["present"] / total * 100

    if percentage < 75:
        print(reg_no, "-", f"{percentage:.2f}%")

print("\nReports saved in:", output_folder)
