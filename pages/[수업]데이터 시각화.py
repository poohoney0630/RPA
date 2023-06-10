
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

st.title("데이터 시각화📊")

titanic = sns.load_dataset("titanic")
st.write('타이타닉 데이터 미리보기')
st.write(titanic.head(5))


# Create a figure and adjust the histogram parameters
fig = plt.figure(figsize=(5, 3))
bins_size = st.slider("계급의 크기를 설정해주세요.", min_value=1, max_value=50, value=10)

# Plot the histogram with adjusted parameters
plt.title('histogram of Age')
sns.set_style("darkgrid")

sns.histplot(x=titanic['age'], binwidth=bins_size, binrange = [0, 100], kde=False)

# Display the histogram
st.pyplot(fig)