# #!/usr/bin/env python

# # -*- coding: utf-8 -*-


# Most code is based on https://melaniewalsh.github.io/Intro-Cultural-Analytics/features/Text-Analysis/Named-Entity-Recognition.html


import math
import re
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

#print (people)

people_tally = Counter(people)
df = pd.DataFrame(people_tally.most_common(), columns=['character', 'count'])
# print (df)



# ESTIMATE GENDER OF PERSON

filepath1 = '/Users/roelsmeets/Desktop/actual_fictions/actual-fictions/male_names_dutch.csv'
filepath2 = '/Users/roelsmeets/Desktop/actual_fictions/actual-fictions/female_names_dutch.csv'

column_names1 = ['Name_male', 'Occurrences']
male_names_csv = pd.read_csv(filepath1, sep=";", names=column_names1)

column_names2 = ['Name_female', 'Occurrences']
female_names_csv = pd.read_csv(filepath2, sep=";", names=column_names2)

male_names = male_names_csv.Name_male.to_list()
female_names = female_names_csv.Name_female.to_list()

# print (male_names)
# print (female_names)

people_list = df.character.to_list()




with open ('characternames.csv', 'a', newline='') as f:
	csvwriter = csv.writer(f)
	"""

	Columns: book_id, character_id, ner_rank, character_name, estimated_gender

	In for-if loop below, define the values of the rows that have to be created by csvwriter.writerow 

	"""



	for person in people_list[:30]:
		if person in male_names and person in female_names:
			print ('RANK:', people_list.index(person), 'CHARACTER:', person, 'NAME', '= gender neutral name')
			# csvwriter.writerow(book_id, character_id, ner_rank, character_name, estimated_gender )
		elif person in male_names and person not in female_names:
			print ('RANK:', people_list.index(person), 'CHARACTER:', person, 'NAME',  '= probably male')
		elif person in female_names and person not in male_names:
			print ('RANK:', people_list.index(person), 'CHARACTER:', person, 'NAME', '= probably female')
		else:
			print ('RANK:', people_list.index(person), 'CHARACTER:', person, 'NAME', '= strange name OR entity is not a person')


	



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




# FUNCTION FOR GETTING NER IN CONTEXT OF TEXT


def get_ner_in_context(keyword, document, desired_ner_labels= 'PERSON'):
	if desired_ner_labels != False:
		desired_ner_labels = desired_ner_labels
	else:
		desired_ner_labels = ['PERSON', 'NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT', 'WORK_OF_ART', 'LAW', 'LANGUAGE', 'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL']  

	#Iterate through all the sentences in the document and pull out the text of each sentence
	for sentence in document.sents:
	    #process each sentence
	    sentence_doc = nlp(sentence.text)

	    for named_entity in sentence_doc.ents:
	        #Check to see if the keyword is in the sentence (and ignore capitalization by making both lowercase)
	        if keyword.lower() in named_entity.text.lower()  and named_entity.label_ in desired_ner_labels:
	            #Use the regex library to replace linebreaks and to make the keyword bolded, again ignoring capitalization
	            #sentence_text = sentence.text

	            sentence_text = re.sub('\n', ' ', sentence.text)
	            sentence_text = re.sub(f"{named_entity.text}", f"**{named_entity.text}**", sentence_text, flags=re.IGNORECASE)

	            print('---')
	            print(f"**{named_entity.label_}**")
	            print(sentence_text)
       

#context_named_entity = get_ner_in_context('Alexander', document)




