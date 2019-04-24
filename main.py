#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 18:13:06 2019

@author: renatoguimaraes
"""
import scholar as sc
import numpy as np
import matplotlib.pyplot as plt
import os
import imp

imp.reload(sc)

def statistics(querier, regexp, opt):
    if opt is not None:
        
        # create an output dir if it doesnot exists
        output_dir = os.path.join(os.getcwd(), 'outputs')
        if os.path.isdir(output_dir) is False:
            os.mkdir(output_dir)
            
        file = open(os.path.join(output_dir, str(regexp.replace(' ','-') + '.opt' + str(opt))), 'w+')
        
        print('==============================================================')
        print(regexp + ' \t Option ' + str(opt))
        print('==============================================================')

        results = len(querier.articles)
        print('\t[=] Number of results: %s' % results)
        file.write('Number of results: %s\n\n' % (results))
        
        if results > 0:
            # variables
            years = list()
            citations = list()
    
            for article in querier.articles:
                # for statistics
                citations.append(article['num_citations'])
                if article['year'] is None:
                    continue
                else:
                    years.append(article['year'])

            years = np.asarray(years, dtype='float')
            citations = np.asarray(citations, dtype='float')
            
            print('\t[=] Year range: [%s, %s]' % (int(years.min()), int(years.max())))
            print('\t[=] Citations: %s +/- %s' % (round(citations.mean(),2), round(citations.std(),2)))
                
            # HAVE biotechnology and regexp
            
            # print results to screen and to file
            for article in querier.articles:
                
                # print to screen and write to file
                #print(article.as_txt() + '\n')
                file.write(article.as_txt() + '\n')
            file.close()
            print('==============================================================')
            return results, years, citations
        
        else:
            print('==============================================================')
            return 0, 0, 0

def main():

    # variables
    regexp = list()
    standard_handler = 'biotechnology'
    
    # Read the regexp from file
    file = open('regexp.in', 'r')
    
    for line in file.readlines():
       regexp.append(line)
    file.close()
    
    
    # Scholar Parser Variables
    querier = sc.ScholarQuerier()
    settings = sc.ScholarSettings()
    
    # Varibles for metric
    results_opt1 = list()
    results_opt2 = list()
    results_opt3 = list()
    
    # loop for each regexp in file
    for index, item in enumerate(regexp):
        query1 = sc.SearchScholarQuery()
        query2 = sc.SearchScholarQuery()
        query3 = sc.SearchScholarQuery()
    
        # Fixed 1000 because the specificity of query
        query1.set_num_page_results(1000)
        query2.set_num_page_results(1000)
        query3.set_num_page_results(1000)
        
        # remove new line
        item = item.rstrip()
        
        # I am using three types of searches because it is not clear how the search handles
        # more than 1 mandatory expression.
        
        # Search 1: 
        # words = ['ascidia curvata', 'biotechnology']
        # phrase = []
    
        query1.set_words(list([item, standard_handler]))
        querier.send_query(query1)
        result = statistics(querier, item, opt=1)
        
        results_opt1.append(result)
        
        # Search 2:
        # words = ['biotechnology']
        # phrase = ['ascidia curvata']
        
        query2.set_words(list([standard_handler]))
        query2.set_phrase(item)
        querier.send_query(query2)
        result = statistics(querier, item, opt=2)
        
        results_opt2.append(result)
        
        # Search 3:
        # words = ['ascidia', 'curvata', 'biotechnology']
        # phrase = []
        
        split_regexp = item.split()
        split_regexp.append(standard_handler)
        
        query3.set_words(split_regexp)
        querier.send_query(query3)
        result = statistics(querier, item, opt=3)
        
        results_opt3.append(result)
        
        
        # You may want to ajust the binning of the data
        # If you want to see citations check results_opt#[0][2]
        
        plt.hist(results_opt1[index][1], alpha=0.5, label='Option 1 (Number of results: %s)'%results_opt1[0][0])
        plt.hist(results_opt2[index][1], alpha=0.5, label='Option 2 (Number of results: %s)'%results_opt1[0][0])
        plt.hist(results_opt3[index][1], alpha=0.5, label='Option 3 (Number of results: %s)'%results_opt1[0][0])
        plt.legend()    
        plt.ylabel('Number of Articles')
        plt.xlabel('Year')
        plt.title(item.upper())
        plt.tight_layout()
        plt.savefig(item.replace(' ', '-') + 'histogram.png')
        plt.clf()
        
        del(query1)
        del(query2)
        del(query3)
    
    # each array is N dimensional, for N regexp specified in the input file
    return results_opt1, results_opt2, results_opt3
    

if __name__ == '__main__':
    main()