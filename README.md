Insurance Data Analysis

Overview:
This repository contains a data analytics pipeline for analyzing insurance-related data. It uses synthetic datasets to explore insurance claims, customer demographics, and policy details. The project leverages Python, dbt, and Power BI for analysis and visualization.

Project Structure:

insurance_dbt/: dbt models for transforming and structuring data.

scripts/: Python scripts for data generation and analysis.

data/: Raw and processed datasets.

logs/: Log files generated during processing.

dashboard.pbix: Power BI dashboard for visualization.

Getting Started:

Clone the repository:
git clone https://github.com/vmaz193/insurance_data.git

cd insurance_data

Install dependencies using uv:
uv install

Set up dbt and run models:
uv run -m dbt run

Open the Power BI dashboard: Launch Power BI Desktop and open dashboard.pbix.

Usage:

Analyze claims, customer demographics, and policies.

Explore dashboards in Power BI.

Use Python scripts for additional data analysis or modeling.

Contributing:
Contributions are welcome. Fork the repository, make changes, and submit a pull request.

License:
This project is licensed under the MIT License. See LICENSE for details.
