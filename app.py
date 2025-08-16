import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np

# --- Helper Functions ---

def clean_quantity_column(s):
    if pd.isna(s): 
        return 0
    s = str(s).replace(',', '').strip()
    try:
        return int(s)
    except:
        return 0

def find_header_row(path, target_columns=['2WIC', '3WN', '4WIC', 'JAN']):
    with open(path, encoding='utf-8') as f:
        for i, line in enumerate(f):
            if any(col in line for col in target_columns):
                return i
    return 6

def load_category_group_data(files):
    df_list = []
    for category, path in files.items():
        header_row = find_header_row(path)
        df_raw = pd.read_csv(path, skiprows=header_row)
        df_raw.dropna(how='all', axis=0, inplace=True)
        df_raw.dropna(how='all', axis=1, inplace=True)
        if category == '2W':
            df_raw.columns = ['S No', 'Vehicle Class', '2WIC', '2WN', '2WT', 'TOTAL']
            melt_vars = ['2WIC', '2WN', '2WT', 'TOTAL']
        elif category == '3W':
            df_raw.columns = ['S No', 'Vehicle Class', '3WN', '3WT', 'TOTAL']
            melt_vars = ['3WN', '3WT', 'TOTAL']
        elif category == '4W':
            df_raw.columns = ['S No', 'Vehicle Class', '4WIC', 'LMV', 'MMV', 'HMV', 'TOTAL']
            melt_vars = ['4WIC', 'LMV', 'MMV', 'HMV', 'TOTAL']
        else:
            continue
        df = df_raw.drop(columns=['S No'], errors='ignore')
        df_long = df.melt(id_vars=['Vehicle Class'], value_vars=melt_vars,
                          var_name='Category Group', value_name='Registrations')
        df_long['Registrations'] = df_long['Registrations'].apply(clean_quantity_column)
        df_long['Vehicle Type'] = category
        df_list.append(df_long)
    return pd.concat(df_list, ignore_index=True)

def load_monthwise_data(path, year):
    header_row = find_header_row(path, target_columns=['JAN'])
    df = pd.read_csv(path, skiprows=header_row)
    df.dropna(how='all', axis=0, inplace=True)
    df.dropna(how='all', axis=1, inplace=True)
    month_names = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
    month_cols = [col for col in df.columns if str(col).upper().strip()[:3] in month_names]
    vehicle_class_candidates = [col for col in df.columns if "vehicle" in str(col).lower() and "class" in str(col).lower()]
    if not vehicle_class_candidates:
        st.error(f"Could not find 'Vehicle Class' column. Found columns: {df.columns.tolist()}")
        st.stop()
    vehicle_class_col = vehicle_class_candidates[0]
    for m in month_cols:
        df[m] = df[m].apply(clean_quantity_column)
    df['Year'] = year
    df = df[[vehicle_class_col] + month_cols + ['Year']]
    df = df.rename(columns={vehicle_class_col: 'Vehicle Class'})
    df['Vehicle Class'] = df['Vehicle Class'].astype(str).str.strip()
    return df

def prepare_time_series(df_2024, df_2025):
    month_map = {'JAN':1,'FEB':2,'MAR':3,'APR':4,'MAY':5,'JUN':6,'JUL':7,'AUG':8,
                 'SEP':9,'OCT':10,'NOV':11,'DEC':12}
    ts = []
    for df in [df_2024, df_2025]:
        year = int(df['Year'].iloc[0])
        for _, row in df.iterrows():
            vclass = row['Vehicle Class']
            for m in month_map.keys():
                if m in df.columns:
                    val = row[m]
                    date = pd.to_datetime(f"{year}-{month_map[m]}-01")
                    ts.append({'Vehicle Class': vclass, 'date': date, 'registrations': val})
    return pd.DataFrame(ts)

def calculate_yoy_qoq(df_time_series, class_filter=None, quarter=None):
    df = df_time_series.copy()
    if class_filter and class_filter != 'All':
        df = df[df['Vehicle Class'] == class_filter]
    df = df.sort_values('date')
    df['quarter'] = df['date'].dt.to_period('Q')
    quarter_sum = df.groupby('quarter')['registrations'].sum().reset_index()
    quarter_sum['quarter_start'] = quarter_sum['quarter'].dt.start_time
    if quarter:
        quarter_sum = quarter_sum[quarter_sum['quarter'].astype(str) == quarter]
    quarter_sum['prev_registrations'] = quarter_sum['registrations'].shift(1)
    quarter_sum['QoQ Growth %'] = np.where(
        quarter_sum['prev_registrations'] == 0, np.nan,
        ((quarter_sum['registrations'] - quarter_sum['prev_registrations']) / quarter_sum['prev_registrations']) * 100
    )
    quarter_sum['prev_year_quarter'] = quarter_sum['quarter'] - 4
    prev_year = quarter_sum[['quarter', 'registrations']].rename(
        columns={'quarter':'prev_year_quarter','registrations':'prev_year_registrations'})
    quarter_sum = quarter_sum.merge(prev_year, on='prev_year_quarter', how='left')
    quarter_sum['YoY Growth %'] = np.where(
        quarter_sum['prev_year_registrations'] == 0, np.nan,
        ((quarter_sum['registrations'] - quarter_sum['prev_year_registrations']) / quarter_sum['prev_year_registrations']) * 100
    )
    return quarter_sum

# ----------- Streamlit App -----------

st.set_page_config(page_title="Vehicle Registration Dashboard", page_icon="🚗", layout="wide")
st.title("🇮🇳 Vehicle Registration Dashboard")

# Load category group data
group_files = {
    '2W': 'data/2W.csv',
    '3W': 'data/3W.csv',
    '4W': 'data/4W.csv'
}
category_df = load_category_group_data(group_files)

# Sidebar filters for category group data
st.sidebar.header("Category Group Filters")
vehicle_types = ['All'] + sorted(category_df['Vehicle Type'].unique())
selected_vehicle_type = st.sidebar.selectbox("Select Vehicle Type", vehicle_types)
filtered_category_df = category_df
if selected_vehicle_type != 'All':
    filtered_category_df = filtered_category_df[filtered_category_df['Vehicle Type'] == selected_vehicle_type]
vehicle_classes = ['All'] + sorted(filtered_category_df['Vehicle Class'].unique())
selected_vehicle_class = st.sidebar.selectbox("Select Vehicle Class", vehicle_classes)
if selected_vehicle_class != 'All':
    filtered_category_df = filtered_category_df[filtered_category_df['Vehicle Class'] == selected_vehicle_class]
category_groups = ['All'] + sorted(filtered_category_df['Category Group'].unique())
selected_category_group = st.sidebar.selectbox("Select Category Group", category_groups)
if selected_category_group != 'All':
    filtered_category_df = filtered_category_df[filtered_category_df['Category Group'] == selected_category_group]

# Show category group data summary and charts
st.header("Vehicle Category Group Data (2025)")
total_units = filtered_category_df['Registrations'].sum()
st.metric("Total Vehicle Units", f"{total_units:,}")
st.dataframe(filtered_category_df.sort_values('Registrations', ascending=False), use_container_width=True)
st.header("Registrations by Vehicle Class")
class_df = filtered_category_df.groupby('Vehicle Class', as_index=False)['Registrations'].sum()
fig_cls = px.bar(class_df.sort_values('Registrations', ascending=False),
                 x='Vehicle Class', y='Registrations', title='Registrations by Vehicle Class')
st.plotly_chart(fig_cls, use_container_width=True)
st.header("Registrations by Category Group")
grp_df = filtered_category_df.groupby('Category Group', as_index=False)['Registrations'].sum()
fig_grp = px.bar(grp_df.sort_values('Registrations', ascending=False),
                 x='Category Group', y='Registrations', title='Registrations by Category Group')
st.plotly_chart(fig_grp, use_container_width=True)

# Load and analyze month-wise data if available
import os
if os.path.exists('data/last-year-data.csv') and os.path.exists('data/month-wise-data.csv'):
    with st.spinner("Loading month-wise data for 2024 and 2025..."):
        df_2024 = load_monthwise_data('data/last-year-data.csv', 2024)
        df_2025 = load_monthwise_data('data/month-wise-data.csv', 2025)
    df_time_series = prepare_time_series(df_2024, df_2025)

    st.sidebar.markdown("---")
    st.sidebar.header("Time Series Filters")
    ts_vehicle_classes = ['All'] + sorted(df_time_series['Vehicle Class'].unique())
    ts_selected_class = st.sidebar.selectbox("Select Vehicle Class (Time Series)", ts_vehicle_classes)

    all_quarters = df_time_series['date'].dt.to_period('Q').drop_duplicates().astype(str).tolist()
    ts_selected_quarter = st.sidebar.selectbox("Select Quarter (Growth Metrics)", ["Show latest"] + all_quarters)

    filtered_ts = df_time_series
    if ts_selected_class != 'All':
        filtered_ts = filtered_ts[filtered_ts['Vehicle Class'] == ts_selected_class]
    monthly_sum = filtered_ts.groupby('date')['registrations'].sum().reset_index()

    st.header(f"Monthly Registrations Trend - {ts_selected_class}")
    fig_ts = px.line(monthly_sum, x='date', y='registrations',
                     labels={'date': 'Date', 'registrations': 'Registrations'},
                     markers=True)
    fig_ts.update_layout(title_x=0.5)
    st.plotly_chart(fig_ts, use_container_width=True)

    growth_df = calculate_yoy_qoq(df_time_series, class_filter=ts_selected_class,
                                  quarter=None if ts_selected_quarter == "Show latest" else ts_selected_quarter)

    if ts_selected_quarter == "Show latest":
        latest_growth = growth_df.iloc[-1] if not growth_df.empty else None
    else:
        latest_growth = growth_df[growth_df['quarter'].astype(str) == ts_selected_quarter]
        latest_growth = latest_growth.iloc[0] if not latest_growth.empty else None

    st.header("Quarterly Growth Metrics (Time Series)")
    if latest_growth is not None:
        st.metric("Quarter", str(latest_growth['quarter']))
        st.metric("Registrations", f"{latest_growth['registrations']:,}")
        st.metric("QoQ Growth (%)", f"{latest_growth['QoQ Growth %']:.2f}" if pd.notna(latest_growth['QoQ Growth %']) else "N/A")
        st.metric("YoY Growth (%)", f"{latest_growth['YoY Growth %']:.2f}" if pd.notna(latest_growth['YoY Growth %']) else "N/A")
    else:
        st.warning("No data available for the selected criteria/quarter.")

    st.header("All Quarters Growth Table (Time Series)")
    st.dataframe(growth_df)
else:
    st.info("Month-wise data files not found. Place 'last-year-data.csv' and 'month-wise-data.csv' in the data/ folder to enable time series analysis.")

