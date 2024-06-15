import pandas as pd
# import string
import streamlit as st
from sklearn.cluster import KMeans
import plotly.express as px

def load_data_yearly():
    penguin_file = st.file_uploader("Select Your Local CSV file",accept_multiple_files=True)
    if penguin_file is None:
        st.stop()
    else:
        tr_pi_bf_ff_data = pd.read_csv(penguin_file[1])
        grouped_by_data = pd.read_csv(penguin_file[0])
    return tr_pi_bf_ff_data, grouped_by_data

tr_pi_bf_ff_data,grouped_by_data = load_data_yearly()
# print(tr_pi_bf_ff_data.columns.tolist())
index_df = tr_pi_bf_ff_data.set_index("Location")

k_n = st.slider("How many clusters?", 2, 10, 2)

# if st.button("Submit"):
# K-means++ with sklearn
kmeans = KMeans(n_clusters=k_n, init='k-means++', random_state=42)  # Set random state for reproducibility
kmeans.fit(index_df)
# Get cluster labels and predicted centroids
cluster_labels = kmeans.labels_
print(cluster_labels)
cluster_df = pd.DataFrame({"Location":index_df.index,"K_Means_labels":cluster_labels})
# Assuming x_col in x has unique values that match column names in y
merged_df = grouped_by_data.merge(cluster_df, left_on='Location', right_on='Location')

merged_df_col_names = merged_df.columns.tolist()
option = st.selectbox("select the cluster number?",tuple(range(k_n)))
if option in tuple(range(k_n)):
    merged_df = merged_df[merged_df[merged_df_col_names[-1]] == option]
    fig = px.line(merged_df, x=merged_df_col_names[1], y=merged_df_col_names[2], color=merged_df_col_names[0], title='Daily Average Demand by Location')
    fig.update_layout(xaxis_title='Date', yaxis_title='Average Demand')
    st.plotly_chart(fig)
# else:
#     st.write("please press submit!")
