# Business Auto Report 📊

## Introduction
**Business Auto Report** is a financial data analysis showcase app. It's designed to effortlessly generate comprehensive PDF reports for a specified month based on business data.

<br> <!-- Line break -->

![Chart example](/images/chart_example.jpg)
*Chart example of generated report.*

## Tools Used
- **Python** (For creating the app)
- **SQLite3** (For data manipulation & analysis and database management. Explore the [database tables design](/sql/tables_creation.sql))
- **Pandas** (For data analysis)
- **Matplotlib and Seaborn** (For creating charts)
- **ReportLab** (For generating the textual part of the PDF report)
- **PyMuPDF (Fitz)** (For appending charts to the PDF report)

## Examples
The generated reports include textual information and several charts for a specified "year-month". The database is populated with dummy data for demonstration purposes. Access some generated report examples in the [docs folder](/docs/).

## Usage
1. Clone this repository using `git clone https://github.com/teofiloxyz/business-auto-report`
2. Navigate to the cloned directory `cd business-auto-report/`
3. Install all dependencies using `pip install -r requirements.txt`
4. Run the app `chmod +x main.py && ./main.py`
5. Choose the desired "year-month" (e.g. "2024-04") to generate the respective report.
6. The PDF report will be generated in the docs folder.

## License
GNU General Public License v3.0.
