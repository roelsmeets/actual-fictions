# #!/usr/bin/env python

# # -*- coding: utf-8 -*-


# Most code is based on https://melaniewalsh.github.io/Intro-Cultural-Analytics/features/Text-Analysis/Named-Entity-Recognition.html

import math
import spacy
from spacy import displacy
from collections import Counter
import pandas as pd
pd.options.display.max_rows = 600
pd.options.display.max_colwidth = 400
pd.set_option("display.max_rows", None, "display.max_columns", None)

import nl_core_news_lg
nlp = nl_core_news_lg.load()

filepath = '/Users/roelsmeets/desktop/af_corpora/af_corpus_1stpers_clean/AaVander_DeLichtekooiVanLoven_clean.txt'
text = open(filepath, encoding='utf-8').read()
document = nlp(text)
show_results = displacy.render(document, style="ent")
# print (show_results)
# print (document.ents)

# for named_entity in document.ents:
# 	print(named_entity, named_entity.label_)

# for named_entity in document.ents:
# 	if named_entity.label_ == "PERSON":
# 		print(named_entity)


# GET PEOPLE

people = []

for named_entity in document.ents:
	if named_entity.label_ == "PERSON":
		people.append(named_entity.text)

people_tally = Counter(people)

df = pd.DataFrame(people_tally.most_common(), columns=['character', 'count'])
print ('people:', df)



# GET PLACES

# places = []

# for named_entity in document.ents:
# 	if named_entity.label_ == "GPE" or named_entity.label_ == "LOC":
# 		places.append(named_entity.text)

# places_tally = Counter(places)

# df = pd.DataFrame(places_tally.most_common(), columns=['place', 'count'])
# print ('places:', df)



# GET STREETS, PARKS, ET CETERA

# streets = []

# for named_entity in document.ents:
# 	if named_entity.label_ == "FAC":
# 		streets.append(named_entity.text)

# streets_tally = Counter(streets)

# df = pd.DataFrame(streets_tally.most_common(), columns = ['street', 'count'])
# print ('streets, parks, etc:', df)



# # GET WORKS OF ART 

# works_of_art = []

# for named_entity in document.ents:
# 	if named_entity.label_ == "WORK_OF_ART":
# 		works_of_art.append(named_entity.text)

# art_tally = Counter(works_of_art)

# df = pd.DataFrame(art_tally.most_common(), columns = ['work_of_art', 'count'])
# print ('works of art:', df)


# GET NAMED ENTIITIES IN THEIR CONTEXT

# context_named_entity = get_ner_in_context('Alexander', document)
# print (context_named_entity)

