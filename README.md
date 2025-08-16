# 🚗 Vehicle Registration Dashboard

[![Streamlit App](https://img.shields.io/badge/Streamlit-Deployed-brightgreen?logo=streamlit)](https://vehicledashboard.streamlit.app/)  
[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)  
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repo-black?logo=github)](https://github.com/Mrakshaymehta/VEHICLE-DASHBOARD)

An interactive **Streamlit dashboard** to analyze and visualize vehicle registration trends across different states in India. This project provides insights into the Indian automotive market from an **investor’s perspective**.

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
