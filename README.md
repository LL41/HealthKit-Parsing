# HealthKit-Parsing

This program takes an Apple HealthKit XML file and formats it into usable CSV files.

## Downloading your Apple Health Data

1. Open the **Health app** on your iPhone.
2. Tap your **profile picture** or **initials** in the top right corner.
   - If you don't see them, tap **Summary** or **Browse** at the bottom, then scroll to the top.
3. Tap **Export All Health Data**.
4. Choose a method to share the data (e.g., email, cloud storage).

## Using HealthKit-Parsing

1. **Clone the repository:**
2. **Move your XML file:** Place the export.xml file into the HealthKit-Parsing directory.
3. **Run the script:** python parse.py export.xml
4. **Choose output format:**
- **unprocessed:** All data in a single CSV file.
- **grouped:** Data organized into separate CSV files by record type (see recordTypes.py for groupings).
Your formatted data will be saved in the same directory.
