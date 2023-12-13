import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Super Market", page_icon=":chart_with_upwards_trend:",layout="wide")

st.title(" :chart_with_upwards_trend: Dashboard for Super Market")
st.markdown('<style>div.block-container{padding-top:15px;}</style>',unsafe_allow_html=True)

# fl = st.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))
# if fl is not None:
#     filename = fl.name
#     st.write(filename)
#     df = pd.read_csv(filename, encoding = "ISO-8859-1")
# else:
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
region = st.sidebar.multiselect("Pick your Region", df["Region"].unique())
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
region_df = filtered_df.groupby(by = "Region", as_index = False)["Sales"].sum()


with col1:
    st.subheader("Category wise Sales")
    fig = px.pie(filtered_df, values = "Sales", names = "Category", hole = 0.6)
    fig.update_traces(text = filtered_df["Category"], textposition = "inside",marker=dict(colors=['#EC6B56', '#FED60A', '#47B39C']))
    st.plotly_chart(fig,use_container_width=True)

with col2:
    st.subheader("Region wise Sales")
    fig = px.pie(filtered_df, values = "Sales", names = "Region", hole = 0.6)
    fig.update_traces(text = filtered_df["Region"], textposition = "inside",marker=dict(colors=['#EC6B56', '#FED60A', '#47B39C','#1F75FE']))
    st.plotly_chart(fig,use_container_width=True)

cl1, cl2 = st.columns((2))
with cl1:
    with st.expander("View Category Data"):
        st.write(category_df.style.background_gradient(cmap="Blues"))
        csv = category_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "Category.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')

with cl2:
    with st.expander("View Region Data"):
        st.write(region_df.style.background_gradient(cmap="Blues"))
        csv = region_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "Region.csv", mime = "text/csv",
                        help = 'Click here to download the data as a CSV file')

Subcategory_df = filtered_df.groupby(by = ["Sub-Category"], as_index = False)["Sales"].sum()
st.subheader("Sub-Category wise Sales") 
fig = px.bar(Subcategory_df, x = "Sub-Category", y = "Sales", text = ['${:,.2f}'.format(x) for x in Subcategory_df["Sales"]], 
                 template = "seaborn") 
fig.update_traces(marker_color='#74BBFB')
st.plotly_chart(fig,use_container_width=True, height = 200)

with st.expander("View Sub-Category Data"):
    st.write(Subcategory_df.style.background_gradient(cmap="Blues"))
    csv = Subcategory_df.to_csv(index = False).encode('utf-8')
    st.download_button("Download Data", data = csv, file_name = "Sub-Category.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')

filtered_df["month_year"] = filtered_df["Order Date"].dt.to_period("M")
st.subheader('Time Series Analysis')

linechart = pd.DataFrame(filtered_df.groupby(filtered_df["month_year"].dt.strftime(" %Y %b"))["Sales"].sum()).reset_index()
linechart['month_year'] = pd.to_datetime(linechart['month_year'])
linechart = linechart.sort_values('month_year')
fig2 = px.line(linechart, x = "month_year", y="Sales", labels = {"Sales": "Sales", "month_year":"Time"},height=500, width = 1000,template="gridon")
st.plotly_chart(fig2,use_container_width=True)

with st.expander("View Data of TimeSeries:"):
    st.write(linechart.style.background_gradient(cmap="Blues"))
    csv = linechart.to_csv(index=False).encode("utf-8")
    st.download_button('Download Data', data = csv, file_name = "TimeSeries.csv", mime ='text/csv')

# Create a tree based on Region, category, sub-Category
st.subheader("Hierarchical view of Sales using TreeMap")
fig3 = px.treemap(filtered_df, path = ["Region","Category","Sub-Category"], values = "Sales",hover_data = ["Sales"],
                  color = "Sub-Category")
fig3.update_layout(width = 800, height = 650)
st.plotly_chart(fig3, use_container_width=True)

chart1, chart2 = st.columns((2))
with chart1:
    st.subheader('Segment wise Sales')
    fig = px.pie(filtered_df, values = "Sales", names = "Segment", template = "plotly_dark")
    fig.update_traces(text = filtered_df["Segment"], textposition = "inside")
    st.plotly_chart(fig,use_container_width=True)

with chart2:
    st.subheader('Category wise Sales')
    fig = px.pie(filtered_df, values = "Sales", names = "Category", template = "gridon")
    fig.update_traces(text = filtered_df["Category"], textposition = "inside")
    st.plotly_chart(fig,use_container_width=True)

import plotly.figure_factory as ff
st.subheader(":point_right: Month wise Sub-Category Sales Summary")
with st.expander("Summary_Table"):
    df_sample = df[0:5][["Region","State","City","Category","Sales","Profit","Quantity"]]
    fig = ff.create_table(df_sample, colorscale = "Cividis")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("Month wise sub-Category Table")
    filtered_df["month"] = filtered_df["Order Date"].dt.month_name()
    sub_category_Year = pd.pivot_table(data = filtered_df, values = "Sales", index = ["Sub-Category"],columns = "month")
    st.write(sub_category_Year.style.background_gradient(cmap="Blues"))

# Create a scatter plot
data1 = px.scatter(filtered_df, x = "Sales", y = "Profit", size = "Quantity")
data1['layout'].update(title="Relationship between Sales and Profits using Scatter Plot.",
                       titlefont = dict(size=20),xaxis = dict(title="Sales",titlefont=dict(size=19)),
                       yaxis = dict(title = "Profit", titlefont = dict(size=19)))
st.plotly_chart(data1,use_container_width=True)

with st.expander("View Data"):
    st.write(filtered_df.iloc[:500,1:20:2].style.background_gradient(cmap="Blues"))

# Download orginal DataSet
csv = df.to_csv(index = False).encode('utf-8')
st.download_button('Download Data', data = csv, file_name = "Data.csv",mime = "text/csv")