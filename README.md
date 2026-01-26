# 🔍 Hidden Transaction Dashboard

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://rahulx2001-hidden-transactions-a-data-driven-invest-main-kjsxqd.streamlit.app)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/rahulx2001)
[![Portfolio](https://img.shields.io/badge/Portfolio-a855f7?style=for-the-badge&logo=google-chrome&logoColor=white)](https://rahulkumarsingh-portfolio.vercel.app/)

**🚀 [View Live Dashboard](https://rahulx2001-hidden-transactions-a-data-driven-invest-main-kjsxqd.streamlit.app)**

A modern Streamlit-based fraud detection and financial crime analysis dashboard.

## Features

- **📊 Interactive KPI Cards**: Real-time metrics for transactions, fraud cases, and amounts
- **📈 Daily Transaction Trends**: Visualize transaction volume over time
- **🔴 Fraud Analysis**: Pie charts and bar charts for fraud detection insights
- **💳 Transaction Type Distribution**: Analyze different types of transactions
- **🔥 Crime Level Heatmap**: Identify patterns in criminal activity
- **🎛️ Advanced Filtering**: Filter by month, transaction type, fraud status, and crime type
- **📥 Data Export**: Download filtered data as CSV

## Installation

```bash
# Navigate to the dashboard directory
cd hiddentranscation-dashboard

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

## Data Structure

The dashboard expects a CSV file with the following columns:
- `typeofaction`: Type of transaction (cash-in, cash-out, transfer, etc.)
- `sourceid`: Source account ID
- `destinationid`: Destination account ID
- `amountofmoney`: Transaction amount
- `date`: Transaction date
- `isfraud`: Fraud indicator (0 = legitimate, 1 = fraud)
- `typeoffraud`: Type of fraud detected
- `levelofcrime`: Severity level (head, member, etc.)
- `typeofcrime`: Crime classification
- `month`: Month extracted from date

## Screenshots

The dashboard features a modern dark theme with gradient accents and interactive Plotly charts.

## Author

**Rahul Kumar Singh**  
[LinkedIn](https://www.linkedin.com/in/rahulx2001)

## License

© 2024 Hidden Transaction Detection System | All Rights Reserved
