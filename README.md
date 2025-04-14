# Magpie Take Home Project

This project processes and visualizes JSON data containing scores associated with skills. It generates CSV files for time series data and a proficiency-by-skill report, as well as a visualization of proficiency trends.

## Prerequisites

- [Python 3](https://www.python.org/downloads/) (Ensure Python is added to your PATH or use the Python launcher `py`)
- Required Python packages:
  - `pandas`
  - `matplotlib`

You can install the required packages via pip:

````bash
pip install pandas matplotlib

File Structure

magpie-take_home/
├── magpie_th/
│   └── src/
│       ├── main.py
│       └── data_processor.py
├── data.json
├── skills.json
└── proficiency.json

data.json: Raw input data containing score records.
skills.json: JSON file listing valid skills.
proficiency.json: JSON file defining allowed proficiency values.
Running the Program
Ensure your JSON input files (data.json, skills.json, proficiency.json) are in the root directory (or update the file paths in main.py accordingly).

Open a terminal in the project directory. On Windows, you can use the VS Code integrated terminal or Command Prompt.

Run the program:

python main.py

Output

time_series.csv: CSV file with processed time series data.
proficiency_report.csv: CSV file containing aggregated proficiency data by skill.
proficiency_visualization.png: Visualization image (scatter plot) displaying proficiency by skill.