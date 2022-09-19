import pandas as pd
import streamlit as st
import numpy as np
import genderdecoder.gd as gd
from collections import Counter
import altair as alt

def create_df():
    # Read CSV
    df = pd.read_csv("data/google/all.csv")
    # Drop unneeded columns
    df.drop(["Unnamed: 0.1", "Unnamed: 0", "extensions", "detected_extensions",
             "job_id", "thumbnail", "via"], axis=1, inplace=True)
    # Drop rows with same descriptions
    df.drop_duplicates(subset=["description"], inplace=True)
    # Drop rows w/o coded words lists
    df = df[df.masculine_coded_words != "masculine_coded_words"]

    # Convert strings to lists
    df["masculine_coded_words"] = df.masculine_coded_words.apply(
        lambda s: str_to_list(s))
    df["feminine_coded_words"] = df.feminine_coded_words.apply(
        lambda s: str_to_list(s))

    # Get number of masculine/feminine words
    df["num_masculine_words"] = df["masculine_coded_words"].apply(
        lambda x: get_list_length(x))
    df["num_feminine_words"] = df["feminine_coded_words"].apply(
        lambda x: get_list_length(x))
    # Drop rows with nan values
    df.dropna()
    return df


def str_to_list(s):
    try:
        s = s.replace("'", "").strip()
        return s[1:-1].split(",")
    except Exception:
        return np.nan


def get_list_length(l):
    try:
        return int(len(l))
    except Exception:
        return np.nan


def get_most_common_df(df, coding):
    NUM_TOP_WORDS = 20

    # Determine column
    if coding == "masculine":
        column = "masculine_coded_words"
    elif coding == "feminine":
        column = "feminine_coded_words"
    else:
        raise Exception(
            "Invalid coding given! Valid codings: masculine, feminine")

    # Get list of word lists
    word_lists = df[column].tolist()
    # Flatten list
    flat_list = []
    for sublist in word_lists:
        try:
            for item in sublist:
                flat_list.append(item.strip())
        except Exception:
            continue

    # Get most common words...
    word_counter = Counter(flat_list)
    most_common_list = word_counter.most_common(NUM_TOP_WORDS)
    # And return it as a DataFrame
    most_common_df = pd.DataFrame(most_common_list, columns=["word", "count"])
    return most_common_df


def display_horiz(x, y):
    col1, col2 = st.columns(2)
    # Left Column
    with col1:
        st.write(x)
    # Right Column
    with col2:
        st.write(y)


def display_analysis(df, title):
    # Get number of jobs
    num_jobs = df.shape[0]

    # Get average number of masc/fem words
    avg_num_masc_words = int(df.describe()["num_masculine_words"]["mean"])
    avg_num_fem_words = int(df.describe()["num_feminine_words"]["mean"])

    # Get number of masc/fem results
    res_df = df.groupby("result").size(
    ).reset_index().reindex([4, 1, 2, 0, 3])
    res_df.columns = ["coding", "num_ads"]

    # Get most common word dfs
    masc_word_df = get_most_common_df(df, "masculine")
    fem_word_df = get_most_common_df(df, "feminine")

    st.title(title)

    st.write(f"Number of ads: **{num_jobs}**")

    res_graph = alt.Chart(res_df).mark_bar().encode(
        x=alt.X("num_ads"),
        y=alt.Y("coding", sort=None)).properties(
        width=350, height=230)

    masc_word_graph = alt.Chart(masc_word_df).mark_bar().encode(
        x=alt.X("count"),
        y=alt.Y("word", sort=None)).properties(
        width=200, height=400)

    fem_word_graph = alt.Chart(fem_word_df).mark_bar().encode(
        x=alt.X("count"),
        y=alt.Y("word", sort=None)).properties(
        width=200, height=400)

    st.subheader("Coding Counts")
    display_horiz(res_df, res_graph)

    st.subheader("20 Most Common Masculine Words")
    st.write(
        f"Average number of _masculine_ words per ad: **{avg_num_masc_words}**")
    display_horiz(masc_word_df, masc_word_graph)

    st.subheader("20 Most Common Feminine Words")
    st.write(
        f"Average number of _feminine_ words per ad: **{avg_num_fem_words}**")
    display_horiz(fem_word_df, fem_word_graph)


def main():
    st.title("Job Ad Gender Decoder")
    st.write("This is a tool that determines gender bias in job advertisements.")
    st.write(f"This application uses the Python package, [genderdecoder](https://github.com/Doteveryone/genderdecoder), by Richard Pope, "
             "which uses the analysis code from [gender-decoder.katmatfield.com](http://gender-decoder.katmatfield.com) by Kat Mayfield, "
             "which is based on the paper, [Evidence That Gendered Wording in Job Advertisements Exists and Sustains Gender Inequality]"
             "(http://gender-decoder.katmatfield.com/static/Gaucher-Friesen-Kay-JPSP-Gendered-Wording-in-Job-ads.pdf), "
             "by Danielle Gaucher, Justin Friesen, and Aaron C. Kay.")

    st.header("Tool")
    txt = st.text_area("Job Description", "Paste text here")
    st.write("Result:", gd.assess(txt))

    # st.header("Data Analysis")
    # df_def = pd.read_csv("data/def.csv")
    # st.write(df_def)

    df = create_df()
    # Create separate dfs for sci and eng queries
    df_sci = df[(df["query"] == "scientist") |
                (df["query"] == "data scientist")]
    df_eng = df[(df["query"] == "engineer") |
                (df["query"] == "software engineer")]

    option = st.selectbox(
        "Data to View", ("Overall", "Scientists", "Engineers"))

    if option == "Scientists":
        display_analysis(df_sci, "Scientists")
    elif option == "Engineers":
        display_analysis(df_eng, "Engineers")
    else:
        display_analysis(df, "Overall")

    st.header("Raw Data")
    st.write(df)


main()
