# Subscription Increase Calculator

A simple desktop application to calculate subscription cost increases over multiple years.

## Features

- **Automatic Calculation:** Generates a table with subscription cost increases based on a range of percentage increases.
- **Manual Entry:** Allows you to manually enter subscription values for each year.
- **CSV Export:** Download the results as a CSV file.

## How to Use

1. **Run the Application:**
   - Open the app by double-clicking the `SubscriptionCalculator.app` (macOS).

2. **Settings:**
   - Enter the subscription amount from the last period.
   - Set the starting, ending, and step percentage for the increase.
   - Enter the number of years.

3. **Generate Tables:**
   - Click **Generate Automatic Table** to create a table with calculated values.
   - Click **Generate Manual Table** to enter your own values per year.

4. **Download CSV:**
   - Click **Download CSV** to save both tables to a CSV file.

5. **Cancel:**
   - Click **Cancel** to exit the application.

## Running in Development

1. **Activate your virtual environment** (if using one):
   ```bash
   source venv/bin/activate  # macOS/Linux

2. **Run the application**
   ```bash
   python SubscriptionCalculator.py

## Building the Application (macOS using PyInstaller)

1. **Install PyInstaller** (if not installed):
   ```bash
   pip install pyinstaller

2. **Clean previous builds** (optional):
  ```bash
  rm -rf build dist __pycache__
  ```
3. **Build the app as a standalone executable:**
   ```bash
   pyinstaller --onefile --windowed SubscriptionCalculator.py
   ```
4. **Find the executable:**
    - After the build completes, the executable will be located in the dist/ folder.
  
## Creating a DMG Installer (macOS)

1.	Install create-dmg (requires Node.js):
2.	Run the create-dmg command (adjust paths as needed):
Replace /path/to/dist/SubscriptionCalculator with the full path to your built executable (from PyInstaller) and /path/to/background.png with the path to your background image. The DMG file will be created in the output folder.

## Troubleshooting
  -	**Tcl/Tk Issues:**
    If you experience Tcl/Tk problems, ensure the TCL_LIBRARY and TK_LIBRARY environment variables are set correctly in your code (see the top of SubscriptionCalculator.py).
  -	**Missing Modules:**
Verify that your virtual environment has all required modules installed.

## License
This project is licensed under the MIT License.
