import streamlit as st
import plotly.express as px
import pandas as pd
import os

st.set_page_config(page_title="Superstore", page_icon=":chart_with_upwards_trend:",layout="wide")

st.title(" :chart_with_upwards_trend: Dashboard for Superstore")
st.markdown('<style>div.block-container{padding-top:15px;}</style>',unsafe_allow_html=True)

os.chdir(r"C:\Users\Asus\OneDrive\Documents\7th sem\Data Mining\StreamlitPractice")
df = pd.read_csv("Sample-Superstore.csv", encoding = "ISO-8859-1")

col1, col2 = st.columns((2)) #two columns for start date and end date
df["Order Date"] = pd.to_datetime(df["Order Date"])

# Getting the min and max date 
startDate = pd.to_datetime(df["Order Date"]).min()
endDate = pd.to_datetime(df["Order Date"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()

st.sidebar.header("Choose your filter: ")
# For Region
region = st.sidebar.multiselect("Pick the Country", df["Region"].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df["Region"].isin(region)]

# For State
state = st.sidebar.multiselect("Pick the State", df2["State"].unique())
if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2["State"].isin(state)]

# For City
city = st.sidebar.multiselect("Pick the City",df3["City"].unique())

# Filter the data based on Region, State and City

if not region and not state and not city:
    filtered_df = df
elif not state and not city:
    filtered_df = df[df["Region"].isin(region)]
elif not region and not city:
    filtered_df = df[df["State"].isin(state)]
elif state and city:
    filtered_df = df3[df["State"].isin(state) & df3["City"].isin(city)]
elif region and city:
    filtered_df = df3[df["Region"].isin(region) & df3["City"].isin(city)]
elif region and state:
    filtered_df = df3[df["Region"].isin(region) & df3["State"].isin(state)]
elif city:
    filtered_df = df3[df3["City"].isin(city)]
else:
    filtered_df = df3[df3["Region"].isin(region) & df3["State"].isin(state) & df3["City"].isin(city)]


category_df = filtered_df.groupby(by = ["Category"], as_index = False)["Sales"].sum()
region_df = filtered_df.groupby(by = ["Region"], as_index = False)["Sales"].sum()

with col1:
    st.subheader("Sales by Category")
    fig = px.pie(filtered_df, values = "Sales", names = "Category",template = "plotly_dark", hole = 0.6)
    fig.update_traces(text = filtered_df["Category"], textposition = "inside")
    fig.update_layout(showlegend=True,legend=dict(title='Category', orientation='v', x=1.0, y=0))
    st.plotly_chart(fig,use_container_width=True)
    with st.expander("View Sales by Category Data"):
        st.write(category_df.style.background_gradient(cmap="Blues"))
        csv = category_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "Category.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')

with col2:
    st.subheader("Sales by Country")
    fig = px.pie(filtered_df, values = "Sales", names = "Region",template = "plotly_dark", hole = 0.6)
    fig.update_traces(text = filtered_df["Region"], textposition = "inside")
    fig.update_layout(showlegend=True,legend=dict(title='Country', orientation='v', x=1.1, y=0))
    st.plotly_chart(fig,use_container_width=True)
    with st.expander("View Sales by Country Data"):
        st.write(region_df.style.background_gradient(cmap="Blues"))
        csv = region_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "Country.csv", mime = "text/csv",
                        help = 'Click here to download the data as a CSV file')


category_pf = filtered_df.groupby(by = ["Category"], as_index = False)["Profit"].sum()
region_pf = filtered_df.groupby(by = "Region", as_index = False)["Profit"].sum()


with col1:
    st.subheader("Profit by Category")
    fig2 = px.pie(filtered_df, values = "Profit", names = "Category",template = "plotly_dark", hole = 0.6)
    fig2.update_traces(text = filtered_df["Category"], textposition = "inside")
    fig2.update_layout(showlegend=True,legend=dict(title='Category', orientation='v', x=1.0, y=0))
    st.plotly_chart(fig2,use_container_width=True)

with col2:
    st.subheader("Profit by Country")
    fig2 = px.pie(filtered_df, values = "Profit", names = "Region",template = "plotly_dark", hole = 0.6)
    fig2.update_traces(text = filtered_df["Region"], textposition = "inside")
    fig2.update_layout(showlegend=True,legend=dict(title='Country', orientation='v', x=1.1, y=0))
    st.plotly_chart(fig2,use_container_width=True)

c1, c2 = st.columns(2)
with c1:
    with st.expander("View Profit by Category Data"):
        st.write(category_pf.style.background_gradient(cmap="Blues"))
        csv = category_pf.to_csv(index = False).encode('utf-8')
        st.download_button("Download", data = csv, file_name = "Category.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')

with c2:
    with st.expander("View Profit by Country Data"):
        st.write(region_pf.style.background_gradient(cmap="Blues"))
        csv = region_pf.to_csv(index = False).encode('utf-8')
        st.download_button("Download", data = csv, file_name = "Country.csv", mime = "text/csv",
                        help = 'Click here to download the data as a CSV file')



Subcategory_df = filtered_df.groupby(by = ["Sub-Category"], as_index = False)["Sales"].sum()
st.subheader("Sales by Sub-Category") 
fig = px.bar(Subcategory_df, x = "Sub-Category", y = "Sales", text = ['${:,.2f}'.format(x) for x in Subcategory_df["Sales"]], 
                 template = "seaborn") 
fig.update_traces(marker_color='#74BBFB')
st.plotly_chart(fig,use_container_width=True, height = 200)

with st.expander("View Sales by Sub-Category Data"):
    st.write(Subcategory_df.style.background_gradient(cmap="Blues"))
    csv = Subcategory_df.to_csv(index = False).encode('utf-8')
    st.download_button("Download Data", data = csv, file_name = "Sub-Category.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')

Subcategory_df = filtered_df.groupby(by = ["Sub-Category"], as_index = False)["Profit"].sum()
st.subheader("Profit by Sub-Category") 
fig = px.bar(Subcategory_df, x = "Sub-Category", y = "Profit", text = ['${:,.2f}'.format(x) for x in Subcategory_df["Profit"]], 
                 template = "seaborn") 
fig.update_traces(marker_color='#74BBFB')
st.plotly_chart(fig,use_container_width=True, height = 200)

with st.expander("View Profit by Sub-Category Data"):
    st.write(Subcategory_df.style.background_gradient(cmap="Blues"))
    csv = Subcategory_df.to_csv(index = False).encode('utf-8')
    st.download_button("Download", data = csv, file_name = "Sub-Category.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')

# Create a tree based on Region, category, sub-Category
st.subheader("Hierarchical view of Sales")
fig3 = px.treemap(filtered_df, path = ["Region","Category","Sub-Category"], values = "Sales",hover_data = ["Sales"],
                  color = "Sub-Category")
fig3.update_layout( height = 700)
st.plotly_chart(fig3, use_container_width=True)

# Time series
filtered_df["month_year"] = filtered_df["Order Date"].dt.to_period("M")
st.subheader('Time Series Analysis [Sales]')

linechart = pd.DataFrame(filtered_df.groupby(filtered_df["month_year"].dt.strftime(" %Y %b"))["Sales"].sum()).reset_index()
linechart['month_year'] = pd.to_datetime(linechart['month_year'])
linechart = linechart.sort_values('month_year')
fig2 = px.line(linechart, x = "month_year", y="Sales", labels = {"Sales": "Sales", "month_year":"Time"},height=500, width = 1000,template="gridon")
st.plotly_chart(fig2,use_container_width=True)

with st.expander("View Data of TimeSeries:"):
    st.write(linechart.style.background_gradient(cmap="Blues"))
    csv = linechart.to_csv(index=False).encode("utf-8")
    st.download_button('Download Data', data = csv, file_name = "TimeSeries.csv", mime ='text/csv', 
                       help = 'Click here to download the data as a CSV file')

filtered_df["month_year"] = filtered_df["Order Date"].dt.to_period("M")
st.subheader('Time Series Analysis [Profit]')

linechart = pd.DataFrame(filtered_df.groupby(filtered_df["month_year"].dt.strftime(" %Y %b"))["Profit"].sum()).reset_index()
linechart['month_year'] = pd.to_datetime(linechart['month_year'])
linechart = linechart.sort_values('month_year')
fig2 = px.line(linechart, x = "month_year", y="Profit", labels = {"Sales": "Profit", "month_year":"Time"},height=500, width = 1000,template="gridon")
st.plotly_chart(fig2,use_container_width=True)

chart1, chart2 = st.columns((2))

with chart1:
    st.subheader('Sales by Segment')
    fig = px.pie(filtered_df, values = "Sales", names = "Segment", template = "plotly_dark", hole=0.6)
    fig.update_traces(text = filtered_df["Segment"], textposition = "inside")
    st.plotly_chart(fig,use_container_width=True)

with chart2:
    st.subheader('Profit by Segment')
    fig = px.pie(filtered_df, values = "Profit", names = "Segment", template = "plotly_dark", hole=0.6)
    fig.update_traces(text = filtered_df["Segment"], textposition = "inside")
    st.plotly_chart(fig,use_container_width=True)

# Create a scatter plot
st.subheader('Relationship between Sales and Profit')
data1 = px.scatter(filtered_df, x = "Sales", y = "Profit", size = "Quantity",trendline='ols')
data1['layout'].update(xaxis = dict(title="Sales",titlefont=dict(size=19)),
                       yaxis = dict(title = "Profit", titlefont = dict(size=19)))
st.plotly_chart(data1,use_container_width=True)

st.subheader('Relationship between Quantity and Discount')
data1 = px.scatter(filtered_df, x = "Quantity", y = "Discount",trendline='ols')
data1['layout'].update(xaxis = dict(title="Quantity",titlefont=dict(size=19)),
                       yaxis = dict(title = "Discount", titlefont = dict(size=19)))
st.plotly_chart(data1,use_container_width=True)

# Download orginal DataSet
col1, col2 = st.columns([1,3])
with col1:
    st.markdown("##### Download Original Dataset")
with col2:
    csv = df.to_csv(index = False).encode('utf-8')
    st.download_button('Download', data = csv, file_name = "Data.csv",mime = "text/csv")
