# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

# 1. IMPORTS

import argparse
from collections import Counter 
from itertools import islice
import networkx as nx
import matplotlib.pyplot as plt
import re
import nltk
import pandas as pd
import os
import glob
import sys
import errno
import csv
from characternetworks_af import Book, Character, Network

from variables_af import *

argparser = argparse.ArgumentParser(description='computes character network of (subset of) novels')
argparser.add_argument('--task', default=1, type=int, help='number of task when parallelising')
argparser.add_argument('--total', default=1, type=int, help='total number of tasks when parallelising')
args = argparser.parse_args()
parameters=vars(args)
task = parameters['task']
total = parameters['total']
if task > total:
    sys.exit('task can not be higher than total!')
    

# 2. INPUT

with open(csvfiles['books'], 'rt') as csvfile1, \
     open(csvfiles['nodes'], 'rt') as csvfile2, \
     open(csvfiles['names'], 'rt') as csvfile4:
    # Csv-file with information on each novel, columns: Book_ID, Title, Author, Publisher, Gender_author, Birthtyear_author Perspective (1stpers, 3rdpers, multi, other)
    BOOKS_AF = csv.reader(csvfile1, delimiter=',')
    # Csv-file with information on characters, columns: Book-ID, Character-ID, Name, Gender, Descent, Age, Education, Profession
    NODES_AF = csv.reader(csvfile2, delimiter=',')
    # Csv-file with information on name variances, columns: Book-ID, Character-ID, Name-ID, Name-variances
    NAMES_AF = csv.reader(csvfile4, delimiter=',')

    
# 3. CREATE BOOK OBJECTS, CHARACTER OBJECTS, ADD NAME VARIANTS TO CHARACTER OBJECTS IN BOOKS OBJECTS, ADD EDGES TO NETWORK OBJECTS IN BOOK OBJECTS

    allbooks = {}

    for line in BOOKS_AF: 
        """ Creates instances of Book for every novel in the corpus

        """
        book_id = line[0]

        if book_id.isdigit(): # Check if book_id a digit

            title = line[1]
            name_author = line[2]
            gender_author = line[3]
            nationality_author = line[4]
            publisher = line[5]
            perspective = line[6]
            filename = line[7]

            allbooks[book_id] = Book(book_id, title, name_author, gender_author, nationality_author, publisher, perspective, filename)

    for line in NODES_AF:
        """ Creates instances of Character for every character in the corpus and adds them to instances of Book

        """
        book_id = line[0]


        if book_id.isdigit(): # Check if book_id is a digit

            character_id = line[1]
            name = line[2]
            gender = line[3]
            #descent = line[4]
            #age = line[5]
            #education = line[6]
            #profession = line[7]

            allbooks[book_id].addcharacter(book_id, character_id, name, gender)


    for line in NAMES_AF:
        """ Adds name variants to instances of Character in instances of Book 

        """
        book_id = line[0]

        if book_id.isdigit(): # Check if book_id is a digit

            character_id = line[1]
            name = line[2]
            name_variant = line[3]

            if allbooks[book_id].allcharacters[character_id].name != name:
                print ('NAMES_AF DOES NOT CORRESPOND WELL WITH NODES_AF IN BOOK', book_id) # Raise error if there are mistakes or typo's in the two corresponding csv-files
                print (allbooks[book_id].allcharacters[character_id].name, name) # Print instance to which the error is due
                exit(1)


            allbooks[book_id].allcharacters[character_id].addnamevariant(name_variant)


    # for line in EDGES_AF_test:
    #     """ Add edges to instances of Network in instances of Book 

    #     """
    #     book_id = line[0]

    #     if book_id.isdigit(): # Check if book_id is a digit

    #         source = line[1]
    #         target = line[2]
    #         relation_type = line[3]


    #         allbooks[book_id].network.add_edge(source, target, relation_type)


    # 4. OUTPUT

    bookids = sorted(allbooks.keys(),key=int)
    tasksize = len(bookids) / total
    startnr = int((task-1) * tasksize)
    endnr = int((task) * tasksize)

    taskbookids = bookids[startnr:endnr]

    csvfile = 'character_rankings.csv'
    if total > 1:
        csvfile = 'character_rankings_task_'+str(task)+'.csv'

    # csvfile2 = 'networkstats.csv'
    # if total > 1:
    #     csvfile2 = 'networkstats_task_'+str(task)+'.csv'

    # csvfile3 = 'communities_frequency_distributions.csv'
    # if total > 1:
    #     csvfile3 = 'communities_frequency_distributions_task_'+str(task)+'.csv'

    # gephi_file = 'networkx_graph.gexf'
    # if total > 1:
    #     gephi_file = 'networkx_graph_task_'+str(task)+'.gexf'



    for book_id in taskbookids: 
        """ Computes all necessary steps for the construction of character networks and outputs centrality values per character to new csv file


        """

        print('computing network of book '+str(book_id))
        #allbooks[book_id].readfile(bookpath[allbooks[book_id].perspective]) # Call method readfile on Book objects with perspective (1, 2, 3)

        allbooks[book_id].readfile(bookpath) # Call method readfile on Book objects with perspective (1, 2, 3)

        allbooks[book_id].novel_word_count() # Call method novel_word_count on each Book object

        allbooks[book_id].compute_network() # Computes weight of relations between Characters objects in Book objects
        
        allbooks[book_id].write_to_csv(csvfile) # Writes to a csv file all character info + their scores for the 5 centrality measures


        #allbooks[book_id].network.compute_networkstats(csvfile2)

        #allbooks[book_id].network.detect_communities(csvfile3)

        # allbooks[book_id].network.draw_network(gephi_file)
















