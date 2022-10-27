"""
Created on Wed Oct 26 15:29:06 2022

@author: eschares
"""
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.express as px
# import os
# import re
# from datetime import datetime

st.set_page_config(page_title='OSTP Impact ISU', page_icon="", layout='wide') #, initial_sidebar_state="expanded")


st.markdown('# Impact of the 2022 OSTP Memo on Iowa State')

with st.expander("About:"):
    st.write("""
        On August 25, 2022, the White House Office of Science and Technology Policy (OSTP) released a [memo](https://www.whitehouse.gov/ostp/news-updates/2022/08/25/ostp-issues-guidance-to-make-federally-funded-research-freely-available-without-delay/) regarding public access to scientific research.
        This updated guidance eliminated the 12-month embargo on publications arising from U.S. federal funding that had been in effect from a previous 2013 OSTP memo.
        
        The OSTP released a companion report with the memo, but it only provided a broad estimate of total numbers affected per year.

        **Therefore, this study seeks to more deeply investigate the characteristics of U.S. federally funded research** over a 5-year period from 2017-2021 to better understand the impact of the updated guidance. It uses a manually created custom filter in the Dimensions database to return only publications that arise from U.S. federal funding.
        
        Each section shows interactive charts and graphs both by absolute number and by percentage of total.

        Additionally, you may search for a particular publisher or journal title to label and color it red to make it easier to distinguish on the graphs.
    """)


st.markdown("""---""")
st.header('Number')
st.write('The number of ISU U.S. federally funded publications per year in Dimensions are:')

d = {'Year': [2021, 2020, 2019, 2018, 2017],
    'Number': ['1,772', '1,747', '1,756', '1,764', '1,677']
    }
summary_df = pd.DataFrame(data=d)
summary_df



# Initialize session_state versions of to_true list
if 'publishers_to_change' not in st.session_state:
    st.session_state.publishers_to_change = []
if 'jnls_to_change' not in st.session_state:
    st.session_state.jnls_to_change = []



st.markdown("""---""")
st.header('Publishers')
publishers_df = pd.read_csv('ISU_by_publisher.csv', header=1)
if st.checkbox('Show raw publisher data'):
    st.subheader('Raw data')
    st.write(publishers_df)


st.write('Label a Publisher and turn it red on the charts:')
selected_publishers = st.multiselect('Publisher Name:', pd.Series(publishers_df['Name'].reset_index(drop=True)), help='Displayed in order provided by the underlying datafile')

if st.button('Find that Publisher'):
    for publisher_name in selected_publishers:
        st.session_state.publishers_to_change.append(publisher_name)
        
# Actually do the changes in df; this runs every time the script runs but session_state lets me save the previous changes
#st.write('changing', st.session_state.publishers_to_change)
for name in st.session_state.publishers_to_change:
    title_filter = (publishers_df['Name'] == name)
    publishers_df.loc[title_filter, 'color'] = 'red'




########### Publishers ############
st.subheader('By absolute number')
fig = px.scatter(publishers_df, x='All Publications', y='FF Publications',  color='color',
                 color_discrete_sequence=['blue', 'red'],
                 log_x='True',
                 hover_name='Name',
                 hover_data={'color': False},
                 trendline='ols',
                 trendline_scope='overall',
                 trendline_color_override='blue',
                 #text='Name'
                 )

fig.update_traces(textposition='top center')

fig.update_layout(
    height=700, width=1200,
    title_text='Publishers: ISU Total vs. U.S. Federally Funded Publications, 2017-2021',
    xaxis_title='Total number of ISU publications 2017-2021 [log]',
    yaxis_title='ISU number of U.S. Federally Funded publications 2017-2021',
    showlegend=False
)


publishers_df2 = publishers_df[(publishers_df['FF Publications'] > 550) | (publishers_df['All Publications'] > 880) | (
    publishers_df['Name'].str.contains('Lawrence Berk|Ridge National|Argonne|Iowa State') | publishers_df['Name'].isin(selected_publishers))]
num_rows = publishers_df2.shape[0]
for i in range(num_rows):
    fig.add_annotation(x=np.log10(publishers_df2['All Publications']).iloc[i],
                       y=publishers_df2["FF Publications"].iloc[i],
                       text=publishers_df2["Name"].iloc[i],
                       # showarrow = True,
                       ax=0,
                       ay=-10
                       )


st.plotly_chart(fig, use_container_width=True)
st.write('R^2 is',px.get_trendline_results(fig).px_fit_results.iloc[0].rsquared)




st.subheader('By percentage')
fig = px.scatter(publishers_df, x='All Publications', y='Percentage', color='color',
                 color_discrete_sequence=['blue', 'red'],
                 log_x='True',
                 hover_name='Name',
                 hover_data={'color': False},
                 )

fig.update_traces(textposition='top center')

fig.update_layout(
    height=700, width=1200,
    title_text='Publishers: ISU Total vs. % FF Publications, 2017-2021',
    xaxis_title='Total number of ISU publications 2017-2021 [log]',
    yaxis_title='ISU % of U.S. Federally Funded publications 2017-2021',
    showlegend=False
)


publishers_df2 = publishers_df[(publishers_df['All Publications'] > 500) | ((publishers_df['Percentage'] > 80) & (publishers_df['Percentage'] < 92)) | (
    publishers_df['Name'].str.contains('Lawrence Berk|Ridge National|Argonne|Iowa State') | publishers_df['Name'].isin(selected_publishers))]
num_rows = publishers_df2.shape[0]
for i in range(num_rows):
    fig.add_annotation(x=np.log10(publishers_df2['All Publications']).iloc[i],
                       y=publishers_df2["Percentage"].iloc[i],
                       text=publishers_df2["Name"].iloc[i],
                       # showarrow = True,
                       ax=0,
                       ay=-10
                       )



st.plotly_chart(fig, use_container_width=True)



############ Publishers OA ##########
st.subheader('Open Access by percentage')

sortby = st.radio(
    'The following charts will show the highest 16 publishers. How do you want to sort?', ('Total Number of Federally Funded pubs', '% of Closed', '% of Green', '% of Gold', '% of Bronze', '% of Hybrid'))

if sortby == 'Total Number of Federally Funded pubs':
    publishers_df = publishers_df.sort_values(by='FF Publications', ascending=False)
elif sortby == '% of Closed':
    publishers_df = publishers_df.sort_values(
        by='% OSTP Closed', ascending=False)
elif sortby == '% of Green':
    publishers_df = publishers_df.sort_values(
        by='% OSTP Green', ascending=False)
elif sortby == '% of Gold':
    publishers_df = publishers_df.sort_values(
        by='% OSTP Gold', ascending=False)
elif sortby == '% of Bronze':
    publishers_df = publishers_df.sort_values(
        by='% OSTP Bronze', ascending=False)
elif sortby == '% of Hybrid':
    publishers_df = publishers_df.sort_values(
        by='% OSTP Hybrid', ascending=False)


fig = px.histogram(publishers_df.iloc[:16], x='Name', y=['% OSTP Closed', '% OSTP Green', '% OSTP Gold', '% OSTP Bronze', '% OSTP Hybrid'],  # color='Mode',
                   barnorm='percent', text_auto='.2f',
                   color_discrete_sequence=[
                       "gray", "green", "gold", "darkgoldenrod", "red"],
                   title='Open Access status of FF publications')  # , facet_col='facet')

fig.update_layout(
    height=700, width=1200,
    title_text='ISU % Open Access Status of U.S. Federally Funded Publications, by Publisher 2017-2021 <br> Numbers 1-16 based on condition selected',
    xaxis_title='Publisher',
    yaxis_title='ISU Percentage FF Publications by OA Mode',
    legend_traceorder="reversed",
    legend_title_text='OA Type'
)

st.plotly_chart(fig, use_container_width=True)


st.subheader('Open Access by absolute number, selections controlled above')

fig = px.histogram(publishers_df.iloc[:16], x='Name', y=['Closed', 'Green', 'Gold', 'Bronze', 'Hybrid'],
                   text_auto='f',
                   color_discrete_sequence=[
                       "gray", "green", "gold", "darkgoldenrod", "red"],
                   title='Open Access status of FF publications')  # , facet_col='facet')

fig.update_layout(
    height=700, width=1200,
    title_text='ISU Open Access Status of U.S. Federally Funded Publications, by Publisher 2017-2021',
    xaxis_title='Publisher',
    yaxis_title='ISU Number FF Publications by OA Mode',
    legend_traceorder="reversed",
    legend_title_text='OA Type'
)

st.plotly_chart(fig, use_container_width=True)









st.markdown("""---""")
######## Journals #########
st.header('Journal Titles')

jnl_df = pd.read_csv('ISU_by_journal.csv', header=1)
if st.checkbox('Show raw journal data'):
    st.subheader('Raw data')
    st.write(jnl_df)



st.write('Label a Journal and turn it red on the charts:')
selected_journals = st.multiselect('Journal Name:', pd.Series(jnl_df['Name'].reset_index(drop=True)), help='Displayed in order provided by the underlying datafile')

if st.button('Find that Journal'):
    for journal_name in selected_journals:
        #st.write(f"changed name, {journal_name}")
        #clear_name_from_list(publisher_name)

        st.session_state.jnls_to_change.append(journal_name)

# Actually do the changes in df; this runs every time the script runs but session_state lets me save the previous changes
#st.write('changing', st.session_state.jnls_to_change)
for name in st.session_state.jnls_to_change:
    title_filter = (jnl_df['Name'] == name)
    jnl_df.loc[title_filter, 'color'] = 'red'



st.subheader('Absolute Number')
fig = px.scatter(jnl_df, x='All Publications', y='FF Publications', color='color',
                 color_discrete_sequence=['blue', 'red'],
                 log_x='True',
                 hover_name='Name',
                 hover_data={'color': False},
                 trendline='ols',
                 trendline_scope='overall',
                 trendline_color_override='blue',
                 #text='Name'
                 )

fig.update_traces(textposition='top center')

fig.update_layout(
    height=700, width=1200,
    title_text='Journals: ISU Total vs. U.S. Federally Funded Publications, 2017-2021',
    xaxis_title='Total number of ISU publications 2017-2021 [log]',
    yaxis_title='ISU number of U.S. Federally Funded publications 2017-2021',
    showlegend=False
)

jnl_df2 = jnl_df[(jnl_df['FF Publications'] > 550) | (jnl_df['All Publications'] > 100) | (
    jnl_df['Name'].str.contains('Lawrence Berk|Ridge National|Argonne|Iowa State') | jnl_df['Name'].isin(selected_journals))]
num_rows = jnl_df2.shape[0]
for i in range(num_rows):
    fig.add_annotation(x=np.log10(jnl_df2['All Publications']).iloc[i],
                       y=jnl_df2["FF Publications"].iloc[i],
                       text=jnl_df2["Name"].iloc[i],
                       # showarrow = True,
                       ax=0,
                       ay=-10
                       )


st.plotly_chart(fig, use_container_width=True)
st.write('R^2 is',px.get_trendline_results(fig).px_fit_results.iloc[0].rsquared)



st.subheader('Percentage')
fig = px.scatter(jnl_df, x='All Publications', y='Percentage', color='color',
                 color_discrete_sequence=['blue', 'red'],
                 log_x='True',
                 hover_name='Name',
                 hover_data={'color': False},
                 )

fig.update_traces(textposition='top center')

fig.update_layout(
    height=700, width=1200,
    title_text='Journals: ISU Total vs. % FF Publications, 2017-2021',
    xaxis_title='Total number of ISU publications 2017-2021 [log]',
    yaxis_title='ISU % of U.S. Federally Funded publications 2017-2021',
    showlegend=False
)


jnl_df2 = jnl_df[(jnl_df['All Publications'] > 100) | ((jnl_df['Percentage'] > 800) & (jnl_df['Percentage'] < 902)) | (
    jnl_df['Name'].str.contains('Lawrence Berk|Ridge National|Argonne|Iowa State') | jnl_df['Name'].isin(selected_journals))]
num_rows = jnl_df2.shape[0]
for i in range(num_rows):
    fig.add_annotation(x=np.log10(jnl_df2['All Publications']).iloc[i],
                       y=jnl_df2["Percentage"].iloc[i],
                       text=jnl_df2["Name"].iloc[i],
                       # showarrow = True,
                       ax=0,
                       ay=-10
                       )


st.plotly_chart(fig, use_container_width=True)



####### By Journal OA #################
st.subheader('Open Access by percentage')

sortby = st.radio(
    'The following charts will show the highest 16 journals. How do you want to sort?', ('Total Number of Federally Funded pubs', '% of Closed', '% of Green', '% of Gold', '% of Bronze', '% of Hybrid'))

if sortby == 'Total Number of Federally Funded pubs':
    jnl_df = jnl_df.sort_values(
        by='FF Publications', ascending=False)
elif sortby == '% of Closed':
    jnl_df = jnl_df.sort_values(
        by='% OSTP Closed', ascending=False)
elif sortby == '% of Green':
    jnl_df = jnl_df.sort_values(
        by='% OSTP Green', ascending=False)
elif sortby == '% of Gold':
    jnl_df = jnl_df.sort_values(
        by='% OSTP Gold', ascending=False)
elif sortby == '% of Bronze':
    jnl_df = jnl_df.sort_values(
        by='% OSTP Bronze', ascending=False)
elif sortby == '% of Hybrid':
    jnl_df = jnl_df.sort_values(
        by='% OSTP Hybrid', ascending=False)


fig = px.histogram(jnl_df.iloc[:16], x='Name', y=['% OSTP Closed', '% OSTP Green', '% OSTP Gold', '% OSTP Bronze', '% OSTP Hybrid'],  # color='Mode',
                   barnorm='percent', text_auto='.2f',
                   color_discrete_sequence=[
                       "gray", "green", "gold", "darkgoldenrod", "red"],
                   title='Open Access status of FF publications')  # , facet_col='facet')

fig.update_layout(
    height=700, width=1200,
    title_text='ISU: % Open Access Status of U.S. Federally Funded Publications, by Journal Title 2017-2021',
    xaxis_title='Journal Title',
    yaxis_title='ISU Percentage FF Publications by OA Mode',
    legend_traceorder="reversed",
    legend_title_text='OA Type'
)

st.plotly_chart(fig, use_container_width=True)


st.subheader('Open Access by absolute number, selections controlled above')
fig = px.histogram(jnl_df.iloc[:16], x='Name', y=['Closed', 'Green', 'Gold', 'Bronze', 'Hybrid'],
                   #barnorm='percent', 
                   text_auto='f',
                   color_discrete_sequence=[
                       "gray", "green", "gold", "darkgoldenrod", "red"],
                   title='Open Access status of FF publications')  # , facet_col='facet')

fig.update_layout(
    height=700, width=1200,
    title_text='ISU: Open Access Status of U.S. Federally Funded Publications, by Journal Title 2017-2021',
    xaxis_title='Journal Title',
    yaxis_title='ISU PercNumberentage FF Publications by OA Mode',
    legend_traceorder="reversed",
    legend_title_text='OA Type'
)

st.plotly_chart(fig, use_container_width=True)




##### Footer in sidebar #####
#st.subheader("About")
github = "[![GitHub repo stars](https://img.shields.io/github/stars/eschares/ostp_impact_isu?logo=github&style=social)](<https://github.com/eschares/ostp_impact_isu>)"


st.write(github)

html_string = "<p style=font-size:13px>v1.0, last modified 10/25/22 <br />Created by Eric Schares, Iowa State University <br /> <b>eschares@iastate.edu</b></p>"
st.markdown(html_string, unsafe_allow_html=True)
