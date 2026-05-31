# 🛒 E-Commerce Customer Analytics Dashboard

An interactive data analysis dashboard exploring customer behavior and sales performance using RFM (Recency, Frequency, Monetary) Analysis.

**Streamlit • Python • Pandas • Seaborn • Data Analysis**

---

## 📸 Preview

🔗 **Live Demo:** https://ecommerce-analysis-proyek-alviya.streamlit.app/

---

## 📋 Table of Contents

- Overview
- Business Questions
- Key Insights
- Dashboard Features
- Project Structure
- Setup & Run Locally
- Dataset
- Author

---

## 🔎 Overview

This project analyzes an e-commerce transaction dataset to understand business performance and customer purchasing behavior.

The analysis focuses on two main aspects:

- **Sales Trend Analysis** to evaluate transaction and revenue growth over time.
- **RFM Analysis (Recency, Frequency, Monetary)** to identify customer characteristics and purchasing patterns.

The project was developed as part of the **Fundamental Data Analysis** submission in the Coding Camp Program.

---

## ❓ Business Questions

| No | Question |
|----|----------|
| 1 | How have transaction volume and revenue evolved from 2016 to 2018? |
| 2 | What are the customer characteristics based on RFM (Recency, Frequency, Monetary) analysis? |

---

## 💡 Key Insights

### 📈 Business Growth

- Transaction volume and revenue generally increased throughout the observation period.
- Revenue reached its highest peak in **November 2017**.
- Monthly trends indicate potential seasonal effects and promotional periods influencing customer purchases.

### 👥 Customer Behavior

- Most customers are **one-time buyers**, indicated by low Frequency values.
- Many customers show high Recency values, suggesting they have not returned for a long period.
- Customer spending distribution is highly skewed, where a small portion of customers contributes significantly to total revenue.

### 🎯 RFM Segmentation

- The majority of customers belong to the **Hibernating** segment.
- A smaller group of **Champions** contributes substantial revenue and represents the most valuable customers.
- RFM analysis provides opportunities for retention campaigns and personalized marketing strategies.

---

## ✨ Dashboard Features

| Feature | Description |
|----------|------------|
| 🔍 Interactive Filters | Filter customers dynamically using RFM score selections |
| 📊 KPI Metrics | Customer count, average monetary value, and transaction volume |
| 🎨 Customer Visualization | Scatter plot of Frequency vs Monetary |
| 📈 Segment Distribution | Customer distribution across monetary score categories |
| 📌 Executive Summary | Automatically updates based on selected filters |
| ⚡ Real-Time Interaction | Dashboard updates instantly when filters change |

---

## 🗂️ Project Structure

```text
ecommerce-analysis-proyek/
│
├── dashboard/
│   ├── dashboard.py
│   ├── main_data.csv
│   └── monthly_trend.csv
│
├── notebook.ipynb
├── requirements.txt
└── README.md
```

> ⚠️ Important: Run the notebook first to generate `main_data.csv` and `monthly_trend.csv` before running the dashboard locally.

---

## ⚙️ Setup & Run Locally

### Prerequisites

- Python 3.10+
- pip

### 1. Clone Repository

```bash
git clone https://github.com/USERNAME/ecommerce-analysis-proyek.git
cd ecommerce-analysis-proyek
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Dashboard

```bash
streamlit run dashboard/dashboard.py
```

Open:

```text
http://localhost:8501
```

in your browser.

---

## 📦 Dependencies

| Package | Purpose |
|----------|---------|
| pandas | Data manipulation and aggregation |
| numpy | Numerical computation |
| matplotlib | Data visualization |
| seaborn | Statistical visualization |
| streamlit | Interactive dashboard |

---

## 📁 Dataset

| Attribute | Detail |
|------------|--------|
| Dataset | E-Commerce Public Dataset |
| Period | 2016 – 2018 |
| Main Tables | Orders, Order Items, Products, Customers |
| Analysis Dataset | main_data.csv |
| Dashboard Dataset | main_data.csv & monthly_trend.csv |

---

## 👤 Author

**Alviyatur Rahmaniyah**

- Dicoding ID: CDCC229D6X1609
- Email: alviyaturrahmaniyah@gmail.com

Fundamental Data Analysis — Coding Camp Program © 2026
