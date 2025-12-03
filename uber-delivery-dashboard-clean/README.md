# Uber – Delivery Time & ATD Dashboard

This project is a full Streamlit dashboard built to analyze Actual Time of Delivery (ATD), operational performance, and delivery patterns using weekly Uber delivery data.  
It's developed as part of a technical  assessment that includes the next things:

- Data preparation  
- Feature engineering  
- Exploratory visualization  
- KPI design  
- Predictive modeling (Random Forest)  
- Dashboard 
- Clean code practices 



 Project Overview

The purpose of this dashboard is to give stakeholders a clear way to:

- Monitor delivery performance  
- Understand the drivers behind ATD  
- Compare courier flows, territories, and restaurant surfaces  
- Identify opportunities for operational improvement  
- Explore a predictive model that explains and predict ATD   

The dashboard is fully interactive and allows filtering by:

- Territory
- Courier flow**
- Merchant surface
- On-time threshold

Dataset Description

The dashboard it's build to consume the weekly dataset produced by the workflow designes in the first deliverable. Each row represents a completed delivery trip and includes:

| Column | Description |
|-------|-------------|
| `workflow_uuid` | Unique workflow/order ID |
| `delivery_trip_uuid` | Unique trip ID |
| `driver_uuid` | Courier ID |
| `territory` | Operational region grouping |
| `courier_flow` | Mode of transportation (Motorbike, Bicycle, Car, etc.) |
| `merchant_surface` | Restaurant device type (Tablet, POS, Other) |
| `pickup_distance` | Distance courier → restaurant (km) |
| `dropoff_distance` | Distance restaurant → customer (km) |
| `ATD` | Actual Time of Delivery (minutes) |
| `order_final_state_timestamp_local` | Local delivery timestamp |

Derived features:

- `total_distance_km`
- `hour_of_day`
- `day_of_week`
- `is_weekend`


Dashboard Features

1. High-level KPIs
- Avg ATD  
- P95 ATD  
- On-time rate  
- Avg pickup distance  
- Avg dropoff distance  

2. Visual Analytics
-ATD distribution (histogram)
- ATD by courier flow (boxplot)
- ATD by territory (bar chart)
- ATD vs total distance (scatterplot)

All charts use an Uber-style theme:
- Dark background (`#000000`)
- White typography  
- Uber green accents  


Predictive Modeling (Random Forest)

The dashboard includes an optional machine learning module using:

- `RandomForestRegressor`
- `ColumnTransformer`
- `OneHotEncoder`
- `SimpleImputer`  
- `StandardScaler`

odel output includes:**
Performance:
- MAE (mean absolute error)
- R² (variance explained)

Feature Importance:
Top drivers of ATD:

- Dropoff distance  
- Total distance  
- Merchant surface  
- Hour of day  
- Courier flow  
- Territory  

Partial Dependence Plots (PDPs)
Explain how changes in each key feature impact ATD.

---

Stakeholder Insights 

This dashboard helps teams answer:

- *Which territories experience the highest ATD?*  
- *Which courier flows are the slowest?*  
- *Are some restaurant device types introducing friction?*  
- *How strongly do long-distance deliveries affect ATD?*  
- *At what hours does ATD spike?*  

This can guide actions such as:

- Increasing courier supply in peak hours  
- Optimizing assignment logic for long-distance trips  
- Supporting merchants with poor device performance  
- Adjusting ETA and pricing strategies  
- Prioritizing operational interventions by territory  

Setup Instructions

Follow these steps to install dependencies and launch the dashboard.

1. Clone the repository
git clone https://github.com/<your-username>/uber-delivery-dashboard.git
cd uber-delivery-dashboard

2. Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate   # macOS
# or
venv\Scripts\activate      # Windows

3. Install dependencies
pip install -r requirements.txt

4. Ensure the dataset is in the correct path

Your project must contain:

data/delivery_weekly.csv


This file is required for the dashboard to run.

5. Run the Streamlit app
streamlit run app.py


The dashboard will open automatically in your browser at:

http://localhost:8501

Reproducibility Notes

This project is designed to be fully reproducible by any reviewer:

All code is modular and organized into the modules/ folder.

The entire environment is specified in requirements.txt.

No external APIs or credentials are required.

All preprocessing is done inside the dashboard (no external ETL needed to run it).

The dashboard uses only the  CSV file (data/delivery_weekly.csv), this file is not in the repo, so It has to be add manually.

If reviewers want to test their own data, they simply need to replace the CSV file with one following the same schema.

📂 Repository Structure
uber-delivery-dashboard/
│
├── app.py                     # Main Streamlit app
├── README.md                  # Project documentation
├── requirements.txt           # Python dependencies
│
│
└── modules/
    ├── data_loader.py         # Loading functions
    ├── preprocessing.py       # Cleaning / feature engineering
    ├── metrics.py             # KPI calculations
    ├── charts.py              # Visualization logic
    └── model.py               # ML model (Random Forest + PDPs)



