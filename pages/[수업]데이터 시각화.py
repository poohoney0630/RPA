
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

st.title("데이터 시각화📊")


dataset_name = st.text_input('데이터이름을 입력해주세요! titanic, iris...:')
if dataset_name == 'titanic':
    df = sns.load_dataset('titanic')
    colname = 'age'

elif dataset_name == 'iris':
    df = sns.load_dataset('iris')
    colname = 'sepal_length'

else:
    st.write("잘못된 데이터 이름입니다.")
    st.stop()

st.write(df.head(5))

st.write(colname, '의 최솟값:', min(df[colname]), '의 최댓값:',max(df[colname]))


# Create a figure and adjust the histogram parameters
fig = plt.figure(figsize=(5, 3))
bins_size = st.slider("계급의 크기를 설정해주세요.", min_value=1, max_value=50, value=10)

# Plot the histogram with adjusted parameters
plt.title('histogram of {}'.format(colname))
sns.set_style("darkgrid")
sns.histplot(x=df[colname], binwidth=bins_size, binrange = [min(df[colname]), max(df[colname])], kde=False)

# Display the histogram
st.pyplot(fig)