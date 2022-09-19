import streamlit as st
from util import write_horizontally, get_ordered_list, init_page

def write_words():
    masc_words = '''active-
adventurous-
aggress-
ambitio-
analy-
assert-
athlet-
autonom-
battle-
boast-
challeng-
champion-
compet-
confident-
courag-
decid-
decision-
decisive-
defend-
determin-
domina-
dominant-
driven-
fearless-
fight-
force-
greedy-
head-strong-
headstrong-
hierarch-
hostil-
impulsive-
independen-
individual-
intellect-
lead-
logic-
objective-
opinion-
outspoken-
persist-
principle-
reckless-
self-confiden-
self-relian-
self-sufficien-
selfconfiden-
selfrelian-
selfsufficien-
stubborn-
superior-
unreasonab-'''.split('\n')

    fem_words = '''agree-
affectionate-
child-
cheer-
collab-
commit-
communal-
compassion-
connect-
considerate-
cooperat-
co-operat-
depend-
emotiona-
empath-
feel-
flatterable-
gentle-
honest-
interpersonal-
interdependen-
interpersona-
inter-personal-
inter-dependen-
inter-persona-
kind-
kinship-
loyal-
modesty-
nag-
nurtur-
pleasant-
polite-
quiet-
respon-
sensitiv-
submissive-
support-
sympath-
tender-
together-
trust-
understand-
warm-
whin-
enthusias-
inclusive-
yield-
share-
sharin-'''.split('\n')

    write_horizontally("**Masculine-Coded Words**",
                       "**Feminine-Coded Words**")
    write_horizontally(get_ordered_list(masc_words),
                       get_ordered_list(fem_words))


def main():
    init_page("About")

    st.write("This is a tool that determines gender bias in job advertisements.")
    st.write(f"This application uses the Python package, [genderdecoder](https://github.com/Doteveryone/genderdecoder), by Richard Pope, "
             "which uses the analysis code from [Gender Decoder](http://gender-decoder.katmatfield.com) by Kat Matfield, "
             "which is based on the paper, [Evidence That Gendered Wording in Job Advertisements Exists and Sustains Gender Inequality]"
             "(http://gender-decoder.katmatfield.com/static/documents/Gaucher-Friesen-Kay-JPSP-Gendered-Wording-in-Job-ads.pdf), "
             "by Danielle Gaucher, Justin Friesen, and Aaron C. Kay.")
    write_words()


main()
