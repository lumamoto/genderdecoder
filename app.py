import pandas as pd
import streamlit as st
import numpy as np
import genderdecoder.gd as gd
from collections import Counter


def create_df():
    # Read CSV
    df = pd.read_csv("data/google/all.csv")
    # Drop unneeded columns
    df.drop(['Unnamed: 0.1', 'Unnamed: 0', 'extensions', 'detected_extensions',
             'job_id', 'thumbnail', 'via'], axis=1, inplace=True)
    # Drop rows with same descriptions
    df.drop_duplicates(subset=['description'], inplace=True)
    # Drop rows w/o coded words lists
    df = df[df.masculine_coded_words != 'masculine_coded_words']
    # Get number of masculine/feminine words
    df["num_masculine_words"] = df['masculine_coded_words'].apply(
        lambda x: is_list(x))
    df["num_feminine_words"] = df['feminine_coded_words'].apply(
        lambda x: is_list(x))
    # Drop rows with nan values
    df.dropna()

    return df


def is_list(x):
    if type(x) == list:
        return len(x)
    else:
        return np.nan


def display_analysis(df):
    # Create separate dfs for sci and eng queries
    df_sci = df[(df['query'] == 'scientist') |
                (df['query'] == 'data scientist')]
    df_eng = df[(df['query'] == 'engineer') | (
        df['query'] == 'software engineer')]

    # Get number of jobs
    num_total_jobs = df.shape[0]
    num_sci_jobs = len(df_sci[df_sci == True].index)
    num_eng_jobs = len(df_eng[df_eng == True].index)

    # Get average number of masc/fem words
    avg_masc_total = df.describe()['num_masculine_words']
    print(avg_masc_total)
    avg_fem_total = df.describe()['num_feminine_words']['mean']
    avg_masc_sci = df_sci.describe()['num_masculine_words']['mean']
    avg_fem_sci = df_sci.describe()['num_feminine_words']['mean']
    avg_masc_eng = df_eng.describe()['num_masculine_words']['mean']
    avg_fem_eng = df_eng.describe()['num_feminine_words']['mean']

    # Get number of masc/fem results
    df_total_res = df.groupby('result').size()
    df_sci_res = df_sci.groupby('result').size()
    df_eng_res = df_eng.groupby('result').size()
    df_total_res.columns = ['count']
    df_sci_res.columns = ['count']
    df_eng_res.columns = ['count']

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Overall")
        st.write(f"Number of ads: {num_total_jobs}")

        # st.write(f"Avg # of masculine words: {avg_masc_total}")
        # st.write(f"Avg # of feminine words: {avg_fem_total}")

        st.write("Coding counts:")
        st.write(df_total_res)

        # ls = df["masculine_coded_words"].tolist()
        # flat_ls = [item for sublist in ls for item in sublist]
        # c = Counter(flat_ls)
        # sorted(c.elements())
        # st.write(c)

    with col2:
        st.subheader("Scientist")
        st.write(f"Number of ads: {num_sci_jobs}")

        # st.write(f"Avg # of masculine words: {avg_masc_sci}")
        # st.write(f"Avg # of feminine words: {avg_fem_sci}")

        st.write("Coding counts:")
        st.write(df_sci_res)

        # ls = df_sci["masculine_coded_words"].tolist()
        # print(ls)
        # flat_ls = []
        # for subls in ls:
        #     try:
        #         for item in subls:
        #             flat_ls.append(item)
        #     except Exception:
        #         continue
        # c = Counter(flat_ls)
        # sorted(c.elements())
        # st.write(c)

    with col3:
        st.subheader("Engineer")
        st.write(f"Number of ads: {num_eng_jobs}")

        # st.write(f"Avg # of masculine words: {avg_masc_eng}")
        # st.write(f"Avg # of feminine words: {avg_fem_eng}")

        st.write("Coding counts:")
        st.write(df_eng_res)

    # Get average number of masc/fem words

    # Get most seen masc/fem words

    return {

    }


def main():
    st.title('Job Ad Gender Decoder')
    st.write("This is a tool that determines gender bias in job advertisements.")
    st.write(f"This application uses the Python package, [genderdecoder](https://github.com/Doteveryone/genderdecoder), by Richard Pope,"
             "which uses the analysis code from [gender-decoder.katmatfield.com](http://gender-decoder.katmatfield.com) by Kat Mayfield,"
             "which is based on the paper, [Evidence That Gendered Wording in Job Advertisements Exists and Sustains Gender Inequality](http://gender-decoder.katmatfield.com/static/Gaucher-Friesen-Kay-JPSP-Gendered-Wording-in-Job-ads.pdf), by Danielle Gaucher, Justin Friesen, and Aaron C. Kay.)")
    st.header("Tool")
    txt = st.text_area('Job listing text')
    st.write('Result:', gd.assess(txt))

    st.header("Data Analysis")
    df = create_df()
    display_analysis(df)

    st.header("Raw Data")
    st.write(df)


main()
