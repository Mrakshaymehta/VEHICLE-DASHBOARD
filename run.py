import pandas as pd
import streamlit as st
import plotly.express as px

# Helper Functions
def clean_quantity_column(s):
    if pd.isna(s): return 0
    s = str(s).replace(',', '').strip()
    try:
        return int(s)
    except:
        return 0

def load_category_group_data(files):
    df_list = []
    for category, path in files.items():
        try:
            # Dynamic header row: look for '2WIC', etc. to skip metadata
            with open(path, encoding='utf-8') as f:
                for i, line in enumerate(f):
                    if any(x in line for x in ['2WIC','3WN','4WIC']):
                        header_row = i
                        break
                else:
                    header_row = 6  # fallback
            df_raw = pd.read_csv(path, skiprows=header_row)
            # Remove fully empty columns/rows
            df_raw.dropna(how='all', axis=0, inplace=True)
            df_raw.dropna(how='all', axis=1, inplace=True)
            # Set columns
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
            # Clean numbers
            df_long['Registrations'] = df_long['Registrations'].apply(clean_quantity_column)
            df_long['Vehicle Type'] = category
            df_list.append(df_long)
        except Exception as e:
            st.error(f"Error loading {path}: {e}")
            return pd.DataFrame()
    return pd.concat(df_list, ignore_index=True)

# Streamlit App
st.set_page_config(page_title="Vehicle Registration Dashboard", page_icon="🚗", layout="wide")
st.title("🇮🇳 Vehicle Registration Dashboard")

files = {
    '2W': 'data/2W.csv',
    '3W': 'data/3W.csv',
    '4W': 'data/4W.csv'
}
df = load_category_group_data(files)

if df.empty:
    st.warning("Data could not be loaded. Please check file paths and file formats.")
else:
    st.sidebar.header("Filters")
    vehicle_types = ['All'] + sorted(df['Vehicle Type'].unique())
    selected_vehicle_type = st.sidebar.selectbox("Select Vehicle Type", vehicle_types)
    filtered_df = df.copy()
    if selected_vehicle_type != 'All':
        filtered_df = filtered_df[filtered_df['Vehicle Type'] == selected_vehicle_type]
    vehicle_classes = ['All'] + sorted(filtered_df['Vehicle Class'].unique())
    selected_vehicle_class = st.sidebar.selectbox("Select Vehicle Class", vehicle_classes)
    if selected_vehicle_class != 'All':
        filtered_df = filtered_df[filtered_df['Vehicle Class'] == selected_vehicle_class]
    category_groups = ['All'] + sorted(filtered_df['Category Group'].unique())
    selected_cat_group = st.sidebar.selectbox("Select Category Group", category_groups)
    if selected_cat_group != 'All':
        filtered_df = filtered_df[filtered_df['Category Group'] == selected_cat_group]

    st.header("Summary Metrics")
    total_qty = filtered_df['Registrations'].sum()
    st.metric("Total Registration Units", f"{total_qty:,}")

    st.header("Details Table")
    st.dataframe(filtered_df.sort_values('Registrations', ascending=False), use_container_width=True)

    st.header("Distribution by Vehicle Class")
    class_df = filtered_df.groupby('Vehicle Class', as_index=False)['Registrations'].sum()
    fig = px.bar(class_df.sort_values('Registrations', ascending=False),
                 x='Vehicle Class', y='Registrations', title='Total Registration by Vehicle Class')
    st.plotly_chart(fig, use_container_width=True)
    
    st.header("Distribution by Category Group")
    group_df = filtered_df.groupby('Category Group', as_index=False)['Registrations'].sum()
    fig2 = px.bar(group_df.sort_values('Registrations', ascending=False),
                  x='Category Group', y='Registrations', title='Total Registration by Category Group')
    st.plotly_chart(fig2, use_container_width=True)
