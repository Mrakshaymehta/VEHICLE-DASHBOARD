# 🚗 Vehicle Registration Dashboard

[![Streamlit App](https://img.shields.io/badge/Streamlit-Deployed-brightgreen?logo=streamlit)](https://vehicledashboard.streamlit.app/)  
[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)  
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repo-black?logo=github)](https://github.com/Mrakshaymehta/VEHICLE-DASHBOARD)

An interactive Streamlit dashboard providing a detailed analysis of vehicle registrations in India for 2024 and 2025. This project combines category-wise vehicle data and monthly registration trends to enable in-depth exploration of the automotive market segmented by vehicle type and class.

## Features

- **Comprehensive Category Group Analysis (2025 data)**
  - Breakdown of registrations by vehicle type: Two Wheeler (2W), Three Wheeler (3W), and Four Wheeler (4W).
  - Detailed insight by vehicle class and category group.
  - Powerful filters to explore registrations by vehicle type, class, and category group.
  - Visualizations including bar charts and data tables to support quick insights.

- **Time-Series Analysis of Registrations (2024 & 2025)**
  - Month-wise registration trends for each vehicle class.
  - Interactive line charts with monthly data points.
  - Calculations of quarterly growth metrics including Quarter-over-Quarter (QoQ) and Year-over-Year (YoY) changes.
  - User controls for viewing specific quarters and filtering vehicle classes.

- **User-Friendly Interface**
  - Sidebar filters for dynamic data exploration.
  - Real-time metrics giving quick access to key performance indicators.
  - Responsive layout suitable for quick business analysis or presentation.

---

🌐 **Live Demo**: [Vehicle Dashboard](https://vehicledashboard.streamlit.app/)  
📂 **Repository**: [GitHub Repo](https://github.com/Mrakshaymehta/VEHICLE-DASHBOARD)

## 📊 Features
- Upload and analyze **2W, 3W, and 4W vehicle registration datasets**
- Interactive filters by **State, Year, and Vehicle Category**
- Visualizations: registration trends, market share, comparative insights
- Built-in data cleaning for raw CSVs
- Simple, fast, and interactive dashboard UI

## 🛠 Tech Stack
- Python 3.12
- Streamlit
- Pandas
- Plotly Express

## 🚀 Getting Started
```bash
git clone https://github.com/Mrakshaymehta/VEHICLE-DASHBOARD.git
cd VEHICLE-DASHBOARD

python3 -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows

pip install -r requirements.txt
# Or install manually
pip install streamlit pandas plotly

streamlit run app.py

📂 Project Structure
VEHICLE-DASHBOARD/
│── app.py               # Main Streamlit dashboard
│── requirements.txt     # Project dependencies
│── 2W.csv               # 2-Wheeler dataset
│── 3W.csv               # 3-Wheeler dataset
│── 4W.csv               # 4-Wheeler dataset
│── README.md            # Documentation

📈 Deployment

The app is deployed on Streamlit Cloud: Vehicle Dashboard Live

👨‍💻 Author

Akshay Mehta
📌 GitHub
