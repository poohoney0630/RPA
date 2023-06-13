
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

st.title("데이터 시각화📊")


dataset_name = st.text_input('데이터 예시: titanic, tips, taxis, penguins, iris...:')
# if dataset_name == 'titanic':
#     df = sns.load_dataset('titanic')
#     colname = 'age'

# elif dataset_name == 'iris':
#     df = sns.load_dataset('iris')
#     colname = 'sepal_length'

# else:
#     st.write("올바른 데이터 이름을 써주세요!")
#     st.stop()

try:
    df = sns.load_dataset(dataset_name)
    st.write(df.head(5))

except ValueError:
    st.write("올바른 데이터 이름을 써주세요!")
    st.stop()


try:
    colname = st.text_input("수치형 열 이름을 써주세요!(범주형 데이터 시각화도 곧 추가될 예정입니다.)")
    if colname != "":

        st.write(colname, '의 최솟값:', min(df[colname]), '의 최댓값:',max(df[colname]))

        # Create a figure and adjust the histogram parameters
        fig = plt.figure(figsize=(5, 3))
        bins_size = st.slider("계급의 크기를 설정해주세요.", min_value=1, max_value=int(max(df[colname]-min(df[colname]))), value=10)

        # Plot the histogram with adjusted parameters
        plt.title('histogram of {}'.format(colname))
        sns.set_style("darkgrid")
        sns.histplot(x=df[colname], binwidth=bins_size, binrange = [min(df[colname]), max(df[colname])], kde=False)

        # Display the histogram
        st.pyplot(fig)

except ValueError:
    st.write("올바른 열 이름을 써주세요!")
    st.stop()
