
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import pandas as pd
import numpy as np

st.title("데이터 시각화📊")
dataset_name = st.text_input('데이터 예시: titanic, tips, taxis, penguins, iris...:')

try:
    df = sns.load_dataset(dataset_name)
    st.write(df.head(5))

except ValueError:
    st.write("올바른 데이터 이름을 써주세요!")
    st.stop()

# 라디오 버튼 생성
variable_type = st.radio("변량 유형 선택", ("수치형", "범주형"))


def get_slider_step(min_value, max_value):
    value_range = max_value - min_value
    bins_size_min = float((min_value // 5) * 5)
    bins_size_max = float((value_range) / 5) if value_range != 0 else 1.0

    if value_range < 1:
        step = 0.1
    elif value_range < 10:
        step = 0.5
    else:
        step = 1
        bins_size_min = int(bins_size_min)
        bins_size_max = int(bins_size_max)

    return bins_size_min+step, bins_size_max, step

# 라디오 버튼의 선택에 따라 실행되는 코드 블록
if variable_type == "수치형":
    # 변량이 수치형인 경우 실행되는 코드
    st.write("수치형 데이터를 히스토그램과 상자그림으로 표현합니다. ")


    try:
        colname = st.text_input("시각화하고 싶은 열 이름을 써주세요!")
        if colname != "":

            data = df[colname]
            # 데이터의 요약 통계량 계산
            summary_stats = pd.DataFrame({
                '평균': np.mean(data),
                '표준편차': np.std(data),
                '최솟값': np.min(data),
                '중앙값': np.median(data),
                '최댓값': np.max(data)
            }, index=['통계량'])

            st.write(summary_stats)
            minvalue = min(df[colname])
            maxvalue = max(df[colname])
            st.write(colname, '의 최솟값:', minvalue, '의 최댓값:',maxvalue)
            bins_size_min, bins_size_max, step = get_slider_step(minvalue, maxvalue)
            st.write(step)
            bins_size = st.slider("계급의 크기를 설정해주세요.",
                                min_value=bins_size_min, 
                                max_value=bins_size_max, 
                                step=step)

            # Create a figure and adjust the histogram parameters
            fig = plt.figure(figsize=(5, 3))

            # bins_size = st.slider("계급의 크기를 설정해주세요.", 
            #                       min_value= 0.5,#+ int((minvalue // 5) * 5), 
            #                       max_value= 1.0+ int((max(df[colname]-min(df[colname])))/5),
            #                       step= 0.5)



            st.write("히스토그램의 계급의 크기:",bins_size)
            # Plot the histogram with adjusted parameters
            sns.set_style("darkgrid")
            plt.title('Histogram of {}'.format(colname))
            sns.histplot(x=df[colname], binwidth=bins_size, binrange = [min(df[colname]), max(df[colname])], kde=False)
            plt.xlabel("")
            st.pyplot(fig)

            # 이상치 숨기기 체크박스
            hide_outliers = st.checkbox("이상치 숨기기")

            # 이상치를 숨기는 옵션 설정
            showfliers = not hide_outliers
            fig2 = plt.figure(figsize=(5, 1))
            plt.title('Boxplot of {}'.format(colname))
            sns.set_style("darkgrid")
            # 박스 플롯 그리기
            sns.boxplot(x=df[colname], palette="Set2", showfliers=showfliers)
            plt.xlabel("")
            st.pyplot(fig2)

    except ValueError:
        st.write("올바른 열 이름을 써주세요!")
        st.stop()


else:
    # 변량이 범주형인 경우 실행되는 코드
    st.write("범주형 데이터를 막대그래프로 표현합니다.")

    try:
        colname = st.text_input("시각화하고 싶은 열 이름을 입력해주세요!")
        if colname != "":
            # Create a figure and adjust the bar plot parameters
            fig = plt.figure(figsize=(5,3))
            ax = sns.countplot(x=df[colname], palette="Blues")

            # Add frequency labels on top of each bar with white outline
            for p in ax.patches:
                height = p.get_height()
                ax.annotate(format(height, ','),
                            (p.get_x() + p.get_width() / 2, height),
                            ha='center', va='center',
                            xytext=(0, -10), textcoords='offset points',
                            fontsize=10, color='black',
                            path_effects=[path_effects.Stroke(linewidth=3, foreground='white'),
                                          path_effects.Normal()])

            plt.title('Barplot of {}'.format(colname))
            sns.set_style("darkgrid")
            plt.xlabel("")
            st.pyplot(fig)

    except ValueError:
        st.write("올바른 열 이름을 입력해주세요!")
        st.stop()
