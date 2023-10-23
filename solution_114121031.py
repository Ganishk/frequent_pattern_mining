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
        self.__candidate_set = list(map(lambda item: set((item,)), self.items)) # This stores the latest candidate itemsets

    @staticmethod
    def generate_dataset_efficiently(transactions):
        """
            Will return the transactions in an hashmap with keys
            as items and values as the set of transaction numbers.

            Space Complexity: O(m*n) (with a small constant multiplier)
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


            Time Complexity: O(log2(n))
            Space Complexity: O(n)
        '''
        # Perform merge sort operation
        self.merge_sort(0, len(self.__candidate_set)-1)

    def merge_sort(self,start,end):
        if (start>=end): return 
        mid = start + (end-start)//2
        self.merge_sort(start,mid)
        self.merge_sort(mid+1,end)
        self.merge_sort_merger(start,mid,end)

    def merge_sort_merger(self,start,mid,end):
        left = start; right = mid + 1
        temp = []
        while left <= mid and right <= end:
            # Sort the array in descending order
            if self.get_support(self.__candidate_set[left]) > self.get_support(self.__candidate_set[right]):
                temp.append(self.__candidate_set[left])
                left += 1
            else:
                temp.append(self.__candidate_set[right])
                right += 1
        
        while left<=mid:
            temp.append(self.__candidate_set[left])
            left += 1
        
        while right<=end:
            temp.append(self.__candidate_set[right])
            right += 1
        
        for i in range(end-start + 1):
            self.__candidate_set[start + i] = temp[i]

    def generate_frequent_itemsets(self):
        '''
            Perform binary search to take the frequent itemsets of length=1,
            which are sorted at the front of the items array.

            Time Complexity: O(log(n) + log(n)) = O(log(n))
        '''
        self.sort_items();

        start = 0; end = len(self.__candidate_set)-1;

        while(start<=end):
            """ Find the upper bound of the supports """
            mid = start + (end - start)//2
            if (self.get_support(self.__candidate_set[mid]) >= self.minsup):
                start = mid + 1;
            else: end = mid - 1;

        """
            At the end of this search, items from 0 to index `end`(inclusive) are frequent,
            whereas items from index `start`(inclusive) to the end of the list are not frequent.
        """

        self.frequent_items += self.__candidate_set[:start]
        self.length_of_frequent_items.append(self.length_of_frequent_items[-1] + start)

        return start

    def get_support(self,itemset=set()):
        """
            This functions is used to get the support of the itemset from dataset. The input
            should be a non-empty itemset

            Time Complexity: O(m*min(ni)), where m is no. of attributes and ni is the no. of
            transactions of ith attribute
        """
        assert len(itemset) > 0
        temp = set()
        for x in itemset:
            # Since, set is a mutable type, don't pop it out to take the first value, but frozenset can be used
            if len(temp) == 0: temp = set(self.ds[x]) # do shallow copy to avoid mutation
            temp &= (self.ds[x])
            if len(temp) == 0: break
        return len(temp)

    def generate_candidates(self,klength=2):
        '''
            This method is used to generate the next set of candidate items

            Time Complexity: O(n*n)
        '''
        self.__candidate_set = list()

        # Merge phase is done below
        for i in range(self.length_of_frequent_items[-2],self.length_of_frequent_items[-1]):
            for j in range(i,self.length_of_frequent_items[-1]):
                new_itemset = self.frequent_items[i] | self.frequent_items[j]
                # Pruning will be done if the itemset is of length k
                if (len(new_itemset)  == klength and new_itemset not in self.__candidate_set and self.get_support(new_itemset)>=self.minsup): self.__candidate_set.append(new_itemset)
    
    def write_to_file(self,filename,start=0,end=None,*,closed=False):
        if end==None: end = len(self.__closed_patterns) if closed else self.length_of_frequent_items[-1]

        frequent_patterns_to_write = self.__closed_patterns if closed else self.frequent_items[start:end]
        frequent_patterns_to_write.sort(key=self.get_support,reverse=True)

        with open(filename,'w') as file:
            file.write(str(end-start)+'\n')
            for i in range(end):
                file.write(f"{','.join(frequent_patterns_to_write[i])}: {self.get_support(frequent_patterns_to_write[i])}\n")

    def filter_closed_frequent_itemsets(self):
        self.__closed_patterns = []
        for klength_index in range(len(self.length_of_frequent_items)-2):
            for pattern_number in range(self.length_of_frequent_items[klength_index],self.length_of_frequent_items[klength_index+1]):
                support_of_current_pattern = self.get_support(self.frequent_items[pattern_number])
                valid_closed_frequent_itemset = False

                for higher_index in range(self.length_of_frequent_items[klength_index+1],self.length_of_frequent_items[klength_index+2]):
                    if self.frequent_items[higher_index].issuperset(self.frequent_items[pattern_number]):
                        if self.get_support(self.frequent_items[higher_index]) != support_of_current_pattern:
                            valid_closed_frequent_itemset = True
                        else:
                            valid_closed_frequent_itemset = False
                            break
                    else: valid_closed_frequent_itemset = True
                    
                
                if valid_closed_frequent_itemset: self.__closed_patterns.append(self.frequent_items[pattern_number])

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

    end_index = apriori.generate_frequent_itemsets()

################################### TASK 1a ####################################
    apriori.write_to_file('patterns_1.txt') # Write the 1 length frequent itemsets to the patterns_1.txt file

    k = 2

    while apriori.length_of_frequent_items[-1] - apriori.length_of_frequent_items[-2] > 0:
        print(f"Generating candidate itemsets of length '{k}'")
        apriori.generate_candidates(k)
        print(f"Finding frequent patterns of length '{k}'")
        apriori.generate_frequent_itemsets()

        start_index = apriori.length_of_frequent_items[-2]
        end_index = apriori.length_of_frequent_items[-1]
        # apriori.write_to_file(f'items_{k}')

        k += 1
    else:
        print("\nLargest found length of itemset:",k-2)

################################### TASK 1b ####################################
    apriori.write_to_file('patterns_all.txt')

################################### TASK 1b ####################################
    apriori.filter_closed_frequent_itemsets()
    apriori.write_to_file("patterns_close.txt",closed=True)
    print("Closed itemsets are filtered successfully")



if __name__=="__main__":
    """Entry point, if this file is run as a script"""
    filename = 'categories.txt' if len(sys.argv) else sys.argv[1]
    rel_minsup = 0.01 if len(sys.argv) < 3 else sys.argv[2]
    main(filename,rel_minsup)
