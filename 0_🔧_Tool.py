import streamlit as st
import genderdecoder.gd as gd
from util import write_horizontally, get_ordered_list, init_page


def main():
    init_page("Tool")

    st.write("Find a job ad and paste its job description below to reveal any gender bias.")

    write_form()


def write_results(desc_input):
    res = gd.assess(desc_input)
    st.header("Results")
    st.subheader(str.title(res["result"]))
    st.write(res["explanation"])
    write_horizontally("**Masculine-Coded Words**",
                       "**Feminine-Coded Words**")
    write_horizontally(get_ordered_list(res["masculine_coded_words"]),
                       get_ordered_list(res["feminine_coded_words"]))


def write_form():
    with st.form("my_form"):
        desc_input = st.text_area("Job Description")
        submitted = st.form_submit_button("Decode ✨")
        if submitted:
            write_results(desc_input)


main()
