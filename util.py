import streamlit as st
import numpy as np


def write_horizontally(a, b):
    col1, col2 = st.columns(2)
    # Left Column
    with col1:
        st.write(a)
    # Right Column
    with col2:
        st.write(b)


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


def get_ordered_list(l):
    if not l:
        return "None"

    list_str = ""
    for i in range(len(l)):
        list_str += f"{i+1}. {l[i]}\n"
    return list_str


def init_page(page):
    st.set_page_config(
        page_title=f"{page} | Gender Decoder",
    )

    with st.sidebar:
        st.title("Gender Decoder")
        st.write(
            "Original [Gender Decoder](http://gender-decoder.katmatfield.com) by Kat Matfield.")

    st.title(page)