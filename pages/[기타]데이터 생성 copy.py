# Streamlit App
import streamlit as st
import pandas as pd

df = pd.DataFrame([['boy', 5,2,5], ['girl', 3,5,1]], columns = ['sex', 'a', 'b', 'c'])
st.write(df)
st.write(pd.melt(df, id_vars='sex', var_name='value2',value_name='id', args='count'))

# def main():
#     # Streamlit App Title
#     st.title("Data Melt with Streamlit")

#     # Upload CSV file using Streamlit
#     uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

#     if uploaded_file:
#         df = pd.read_csv(uploaded_file)
        
#         # Melt the dataframe
#         melted_df = pd.melt(df, id_vars=['성별'], var_name='학년', value_name='id').drop('id', axis=1)
#         melted_df['id'] = range(1, len(melted_df) + 1)
        
#         # Display melted dataframe
#         st.write(melted_df)
#     else:
#         st.write("Please upload a CSV file.")

# if __name__ == "__main__":
#     main()
