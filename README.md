# Business Auto Report 📊

## Introduction
**Business Auto Report** is a financial data analysis showcase app. It's designed to effortlessly generate comprehensive PDF reports for a specified month based on business data.

<br> <!-- Line break -->

![Chart example](/images/chart_example.jpg)
*Chart example of generated report.*


## Tools Used
- **Python**: For creating the app.
- **SQLite3**: For database management, data manipulation and data analysis. Explore the database design [here](/sql/tables_creation.sql).
- **Pandas**: For data analysis.
- **Matplotlib and Seaborn**: For creating charts.
- **ReportLab**: For generating the textual part of the PDF report.
- **PyMuPDF (Fitz)**: For appending charts to the PDF report.


## Examples
The generated reports include textual information and several charts for a specified "year-month". The database is populated with dummy data for demonstration purposes. Access some generated report examples in the [docs folder](/docs/).


## Usage
1. Clone this repository.
2. Install all requirements.
3. Run the app.
4. Choose the desired "year-month" (e.g. "2024-04") to generate the respective report.
5. The PDF report will be generated in the docs folder.

<details>
<summary>Click to reveal full command</summary>

```bash
git clone https://github.com/teofiloxyz/business-auto-report \
    && cd business-auto-report/ \
    && pip install -r requirements.txt \
    && chmod +x main.py \
    && ./main.py \
    || echo "An error occurred"
```
</details>


## License
GNU General Public License v3.0.
