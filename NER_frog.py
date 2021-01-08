# #!/usr/bin/env python

# # -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals #to make this work on Python 2 as well as Python 3
import frog

filepath = '/Users/roelsmeets/desktop/af_corpora/af_corpus_1stpers_clean/AaVander_DeLichtekooiVanLoven_clean.txt'
text = open(filepath, encoding='utf-8').read()

frog = frog.Frog(frog.FrogOptions(parser=False))

raw_output = frog.process_raw(text)
# print ('**********************************************************')
# print("RAW OUTPUT=",raw_output)
# print ('**********************************************************')

parsed_output = frog.process(text)
# print ('**********************************************************')
# print("PARSED OUTPUT=",parsed_output)
# print ('**********************************************************')

named_entities = []

# for element in parsed_output:
# 	if parsed_output[element]['ner'] == 'B-PER':
# 		named_entities.append(parsed_output[element]['text'])

# print (named_entities)