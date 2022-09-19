# Gender Decoder

[Gender Decoder](https://lumamoto-genderdecoder-0--tool-5yx72t.streamlitapp.com/) 
is a web application that helps users locate gender bias in a given job ad and 
analyzes the biases found in over 500 scientist and engineer job descriptions.
## Credits
This application uses the Python package, [genderdecoder](https://github.com/Doteveryone/genderdecoder)
by Richard Pope, which uses the analysis code from [Gender Decoder](http://gender-decoder.katmatfield.com) 
by Kat Matfield, which is based on the paper, 
[Evidence That Gendered Wording in Job Advertisements Exists and Sustains Gender Inequality](http://gender-decoder.katmatfield.com/static/documents/Gaucher-Friesen-Kay-JPSP-Gendered-Wording-in-Job-ads.pdf)
by Danielle Gaucher, Justin Friesen, and Aaron C. Kay.

## How it Works
From Kat Matfield's Gender Decoder [About](http://gender-decoder.katmatfield.com/about):
> Below are the full lists of words that Danielle Gaucher's, Justin Friesen's, 
> and Aaron C. Kay's research considered masculine- and feminine-coded. 
> This tool checks job adverts for the appearance of any of these words, 
> then calculates the relative proportion of masculine-coded and feminine-coded 
> words to reach an overall verdict on the gender-coding of the advert. 
> 
> Some words have been reduced to a 'stem' to cover a range of
> noun, verb and adjective variants; for instance, "compet" covers "compete", 
> "competitive" and "competition".

## Built With
- [Streamlit](https://streamlit.io/)
- [genderdecoder](https://github.com/Doteveryone/genderdecoder)
- [SerpApi](https://serpapi.com/)