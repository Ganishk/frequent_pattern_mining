#!/usr/bin/env python3

"""Importing built-in libraries"""
import math
import sys



class Apriori:
    '''
        The class for perform apriori algorithm related functions
    '''


    frequent_items = [] #This will store all the k-length frequent itemsets
    length_of_frequent_items = [0]
    #value at index `i` - `i-1` gives the total number of i-length frequent itemsets


    def __init__(self,values=[[]],relative_minimum_support=1):
        """
            Constructor for Apriori class.
            Here, the minimum support count will be calculated
            and 2D array of input values will be taken and stored
            in the class variable ds efficiently.
        """
        self.total_transactions = len(values)
        self.minsup = len(values)*relative_minimum_support
        self.ds = Apriori.generate_dataset_efficiently(values)
        self.items = list(self.ds.keys())
        self.__candidate_set = self.items # This stores the latest candidate itemsets


    @staticmethod
    def generate_dataset_efficiently(transactions):
        """
            Will return the transactions in an hashmap with keys
            as items and values as the set of transaction numbers.
        """
        hmp = dict();
        for transaction_number in range(len(transactions)):
            for item in transactions[transaction_number]:
                if item not in hmp: hmp[item]=set()
                hmp[item].add(transaction_number)
        return hmp

    def sort_items(self):
        '''
            This function will sorts the class variable which is the
            list of all items based on it's support.


            Time Complexity: O(nlog(n))
        '''
        self.__candidate_set.sort(key=(lambda item: len(self.ds[item])),reverse=True)

    def base_itemsets(self):
        '''
            Perform binary search to take the frequent itemsets of length=1,
            which are sorted at the front of the items array.

            Time Complexity: O(nlog(n) + log(n)) = O(nlog(n))
        '''
        self.sort_items();

        start = 0; end = len(self.items);

        while(start<=end):
            """ Find the upper bound of the supports """
            mid = start + (end - start)//2

            if (len(self.ds[self.items[mid]]) >= self.minsup):
                start = mid + 1;
            else: end = mid - 1;

        """
            At the end of this search, items from 0 to index `end`(inclusive) are frequent,
            whereas items from index `start`(inclusive) to the end of the list are not frequent.
        """

        self.frequent_items += self.items[0:start]
        self.length_of_frequent_items.append(start)

        return start

    def generate_candidates(self,klength=2):
        for i in range(self.length_of_frequent_items[-2],self.length_of_frequent_items[-1]):
            for j in range(i,self.length_of_frequent_items[-1]):
                self.__candidate_set



def main(dataset=None,relminsup=1):
    if dataset==None: return

    with open(dataset,'rt') as file:
        """
            Seek the beginning position of the dataset
            file, read each lines and split them based on
            the delimitter `;`

            values will be a 2D array
        """
        values = [line.split(';') for line in file.read().split('\n') if file.seek(0)==0]


    apriori = Apriori(values,rel_minsup)

    end_index = apriori.base_itemsets()

################################### TASK 1a ####################################
    with open('patterns_1.txt','wt') as file:
        '''
            Write the 1 length frequent itemsets to the patterns_1.txt file'
        '''
        file.write(str(end_index)+"\n")
        for i in range(end_index):
            file.write(f"{apriori.items[i]}: {len(apriori.ds[apriori.items[i]])}\n")

    k = 2
    while apriori.length_of_frequent_items[-1] - apriori.length_of_frequent_items[-2] > 0:
        apriori.generate_candidates(2)
        break




if __name__=="__main__":
    """Entry point, if this file is run as a script"""
    filename = sys.argv[1]
    rel_minsup = 0.01
    main(filename)
