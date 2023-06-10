
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

titanic = sns.load_dataset("titanic")
st.write(titanic.head(5))
fig = plt.figure(figsize=(10, 4))
sns.histplot(x=titanic['age'])
st.pyplot(fig)
