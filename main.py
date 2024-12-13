import pandas as pd
import streamlit as st
import Streamlit_Dashboard.Preprocessor as Preprocessor 
 
df = pd.read_csv("data.csv")

# Creating time feature 
df = Preprocessor.fetch_time_feature(df)

# Title for Dshbord
st.title("Sales Analytics Dashboard")

#  Side bar for filter
st.sidebar.title('Filters')

# Filters
selected_year =  Preprocessor.multiselect("Select Year" , df['Financial_Year'].unique())
selected_retailer = Preprocessor.multiselect("Select Ratailer",df['Retailer'].unique())
selected_company = Preprocessor.multiselect("Select Coampany",df['Company'].unique())
selected_month = Preprocessor.multiselect("Select Financial Month",df['Financial_Month'].unique())

filtered_df = df[(df['Financial_Year'].isin(selected_year)) &
                 (df['Retailer'].isin(selected_retailer)) &
                 (df['Company'].isin(selected_company)) &
                 (df['Financial_Month'].isin(selected_month))]



# KPI - Key Performance Indicater
# Create column for displaying KPIs
col1, col2, col3, col4 = st.columns(4)

# Total Sales
with col1:
    st.metric(label = 'Total Sales' , value = f" ₹ {int(filtered_df['Amount'].sum())}")

# Total Margin
with col2:
    st.metric(label = 'Total Margin' , value = f" ₹ {int(filtered_df['Margin'].sum())}")

#Total Transaction
with col3:
    st.metric(label = 'Total Transaction' , value = len(filtered_df))

# Percentage Margin
with col4:
    st.metric(label = 'Total Sales' , value = f"{int(filtered_df['Margin'].sum() * 100 / (filtered_df['Amount'].sum()))} %")

# Visualization to analyze month -on - month sales trends
yearly_sales = (filtered_df[['Financial_Year','Financial_Month','Amount']]
                .groupby(['Financial_Year','Financial_Month'])
                .sum()
                .reset_index()
                .pivot(index = "Financial_Month",columns = 'Financial_Year', values='Amount'))

st.line_chart(yearly_sales , x_label = 'Financial_Month',y_label = 'Total_Sales')

# Visualize Retailer count by Revenue %
col5, col6 = st.columns(2)

with col5:
    st.title("Retailer count by Revenue %")
    retailer_count = Preprocessor.fetch_top_revenue_retailers(filtered_df)
    retailer_count.set_index('percentage revenue',inplace= True)
    st.bar_chart(retailer_count , x_label = 'percentage revenue' ,y_label = 'retailer_count')

with col6:
    st.title("Company count by Revenue %")
    company_count = Preprocessor.fetch_top_revenue_compaines(filtered_df)
    company_count .set_index('percentage revenue',inplace= True)
    st.bar_chart(retailer_count , x_label = 'percentage revenue' ,y_label = 'company_count')
