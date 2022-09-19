import pandas as pd
import streamlit as st
from collections import Counter
import altair as alt
from util import write_horizontally, str_to_list, get_list_length, init_page
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode


def main():
    init_page("Data")

    st.write('''
    The following data was collected using [SerpApi](https://serpapi.com/), 
    using the [Google Jobs API](https://serpapi.com/google-jobs-api).

    Using the **dropdown** below, you may view _Overall_, _Scientist_, and _Engineer_ data.
    - _Scientist_ data consists of job results from "scientist" and "data scientist" queries.
    - _Engineer_ data consists of job results from "engineer" and "software engineer" queries.
    - _Overall_ data consists of both _Scientist_ and _Engineer_ data.
    ''')

    df = create_df()
    df_sci = df[(df["query"] == "scientist") |
                (df["query"] == "data scientist")]
    df_eng = df[(df["query"] == "engineer") |
                (df["query"] == "software engineer")]

    option = st.selectbox(
        "Dataset to View", ("Overall", "Scientist", "Engineer"))

    if option == "Scientist":
        display_analysis(df_sci, "Scientist")
    elif option == "Engineer":
        display_analysis(df_eng, "Engineer")
    else:
        display_analysis(df, "Overall")


def aggrid_interactive_table(df):
    """Creates an st-aggrid interactive table based on a dataframe."""
    options = GridOptionsBuilder.from_dataframe(
        df, enableRowGroup=True, enableValue=True, enablePivot=True
    )
    options.configure_side_bar()
    options.configure_selection("single")
    AgGrid(
        df,
        enable_enterprise_modules=True,
        gridOptions=options.build(),
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
        height=500)

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
    df = df.dropna()

    # Move result column to right of company_name
    res_column = df.pop('result')
    df.insert(2, 'result', res_column)

    return df


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


def display_analysis(df, title):
    # Get number of jobs
    num_jobs = df.shape[0]

    # Get average number of masc/fem words
    avg_num_masc_words = int(df.describe()["num_masculine_words"]["mean"])
    avg_num_fem_words = int(df.describe()["num_feminine_words"]["mean"])

    # Get number of masc/fem results
    res_df = df.groupby("result").size().reset_index().reindex(
        [4, 1, 2, 0, 3])
    res_df.columns = ["coding", "num_ads"]

    # Get most common word dfs
    masc_word_df = get_most_common_df(df, "masculine")
    fem_word_df = get_most_common_df(df, "feminine")

    # Create graphs
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

    st.header(title)
    st.metric(label="Number of Ads", value=num_jobs)

    st.subheader("Coding Counts")
    write_horizontally(res_df, res_graph)

    st.subheader("20 Most Common Masculine Words")
    st.write(
        f"Average number of _masculine_ words per ad: **{avg_num_masc_words}**")
    write_horizontally(masc_word_df, masc_word_graph)

    st.subheader("20 Most Common Feminine Words")
    st.write(
        f"Average number of _feminine_ words per ad: **{avg_num_fem_words}**")
    write_horizontally(fem_word_df, fem_word_graph)

    st.subheader("Data Table")
    st.write('''
    Looking for results for a specific company or job title? Click on _Filters_.

    Too many columns? Hide a few by clicking on _Columns_.
    ''')
    aggrid_interactive_table(df)


main()
