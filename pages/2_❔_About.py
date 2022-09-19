import streamlit as st
from util import write_horizontally, get_ordered_list, init_page


def main():
    init_page("About")

    st.write('''
        This application helps users locate gender bias in a given job ad.
        It also analyzes the biases found in over 500 scientist and engineer job descriptions.

        ## Credits
        This application uses the Python package, [genderdecoder](https://github.com/Doteveryone/genderdecoder)
        by Richard Pope, which uses the analysis code from [Gender Decoder](http://gender-decoder.katmatfield.com) 
        by Kat Matfield, which is based on the paper, [Evidence That Gendered Wording in Job Advertisements 
        Exists and Sustains Gender Inequality](http://gender-decoder.katmatfield.com/static/documents/Gaucher-Friesen-Kay-JPSP-Gendered-Wording-in-Job-ads.pdf)
        by Danielle Gaucher, Justin Friesen, and Aaron C. Kay.

        ## How it Works
        From Kat Matfield's Gender Decoder [About](http://gender-decoder.katmatfield.com/about) page:
        > Below are the full lists of words that Danielle Gaucher's, Justin Friesen's, 
        > and Aaron C. Kay's research considered masculine- and feminine-coded. 
        > This tool checks job adverts for the appearance of any of these words, 
        > then calculates the relative proportion of masculine-coded and feminine-coded 
        > words to reach an overall verdict on the gender-coding of the advert. 
        > 
        > Some words have been reduced to a 'stem' to cover a range of
        > noun, verb and adjective variants; for instance, "compet" covers "compete", 
        > "competitive" and "competition".
    ''')
    write_key_words()


def write_key_words():
    masc_words = 'active-\nadventurous-\naggress-\nambitio-\nanaly-\nassert-\nathlet-\nautonom-\nbattle-\nboast-\nchalleng-\nchampion-\ncompet-\nconfident-\ncourag-\ndecid-\ndecision-\ndecisive-\ndefend-\ndetermin-\ndomina-\ndominant-\ndriven-\nfearless-\nfight-\nforce-\ngreedy-\nhead-strong-\nheadstrong-\nhierarch-\nhostil-\nimpulsive-\nindependen-\nindividual-\nintellect-\nlead-\nlogic-\nobjective-\nopinion-\noutspoken-\npersist-\nprinciple-\nreckless-\nself-confiden-\nself-relian-\nself-sufficien-\nselfconfiden-\nselfrelian-\nselfsufficien-\nstubborn-\nsuperior-\nunreasonab-'.split(
        '\n')
    fem_words = 'agree-\naffectionate-\nchild-\ncheer-\ncollab-\ncommit-\ncommunal-\ncompassion-\nconnect-\nconsiderate-\ncooperat-\nco-operat-\ndepend-\nemotiona-\nempath-\nfeel-\nflatterable-\ngentle-\nhonest-\ninterpersonal-\ninterdependen-\ninterpersona-\ninter-personal-\ninter-dependen-\ninter-persona-\nkind-\nkinship-\nloyal-\nmodesty-\nnag-\nnurtur-\npleasant-\npolite-\nquiet-\nrespon-\nsensitiv-\nsubmissive-\nsupport-\nsympath-\ntender-\ntogether-\ntrust-\nunderstand-\nwarm-\nwhin-\nenthusias-\ninclusive-\nyield-\nshare-\nsharin-'.split(
        '\n')
    write_horizontally("**Masculine-Coded Words**",
                       "**Feminine-Coded Words**")
    write_horizontally(get_ordered_list(masc_words),
                       get_ordered_list(fem_words))


main()
