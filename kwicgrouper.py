"""
A module to look for patterns in concordances.
"""


import copy
import nltk
import pandas as pd
import re
from string import punctuation

def clean_text(text):
    text = text.lower()
    text = text.replace("\r\n", " ")
    wordlist = nltk.word_tokenize(text)   
    # wordlist = text.split()
    clean_text = " ".join(wordlist)
    return clean_text

def clean_punkt(text):
    """
    problem here: makes CAN'T into CA NT
    """
    
    for punkt in list(punctuation):
        text = text.replace(punkt, '')
    return text

def old_clean_punkt(text):
    """
    This ignores apostrophes and punctuation marks attached to the word
    * an alternative way would be to replace-delete the punctuation from the text
    """
    tokenized = nltk.word_tokenize(text)
    no_punkt = []
    for token in tokenized:
        if token in list(punctuation):
            pass
        else:
            # no_punkt.append(word.upper())
            no_punkt.append(token)
    return " ".join(no_punkt)


class Concordance(object):
    """
    This is a simple concordance for a text file. The input text
    should a string that is cleaned, for instance:
    
        text.replace("\n", " ").replace("  ", " ")
        
    This function has two argument: the search term and the 
    text to be searched.
    
    The length should be an integer
    """    
        
    def __init__(self, 
                 term, 
                 text, 
                 word_boundaries=True,
                 length=50,
                 keep_punctuation=True,
                 keep_line_breaks=False):

        self.term = term
        self.text = text
        self.word_boundaries = word_boundaries
        assert length < 250
        self.length = length
        self.keep_line_breaks = keep_line_breaks
        # keep_punctuation        
    
    def single_line_conc(self):
        if self.word_boundaries:
            hits = re.finditer(r"\b{}\b".format(self.term), self.text)
        else: 
            hits = re.finditer(r"{}".format(self.term), self.text)
        lines = []
        for hit in hits:
            start = hit.start()
            lines.append(self.text[start-self.length:start+len(self.term)+self.length])        
        return lines
   
    @classmethod
    def from_multiple_line_file(self, term, input_li):
        """
        Construct a concordance that respect line breaks (rather than one
        that treats the text as one large string)
        """
        return Concordance(term, input_li)
   
    def print_concordance(self):
        lines = self.single_line_conc()
        print "There are {} lines in the concordance for {}:".format(len(lines), self.term)
        print
        for line in lines:
            print line 
       
    def list_concordance(self): 
        if self.word_boundaries:
            hits = re.finditer(r"\b{}\b".format(self.term), self.text)
        else: 
            hits = re.finditer(r"{}".format(self.term), self.text)
        lines = []
        for hit in hits:
            start = hit.start()
            end = hit.end()
            left = self.text[start-self.length:start]
            term = self.text[start:end]
            right = self.text[start+len(self.term):start+len(self.term)+self.length]
            lines.append([left, term, right])
        return lines


def concordance_for_line_by_line_file(input_file, term):
    """
    Takes a file that has different line breaks that cannot be ignored 
    (for instance a file with a list of things) and makes it into a concordance
    """
    with open(input_file) as input_file:
        contents = input_file.readlines()
    
    concordance = []
    
    for line in contents:
        line = clean_punkt(clean_text(line))
        conc = Concordance(term, line, length=150).list_concordance()
        if conc: 
            concordance.append(conc)
    
    concordance = [itm for sublist in concordance for itm in sublist]
    return concordance


class KWICgrouper(object):
    """
    This starts from a concordance and transforms it into a pandas dataframe 
    (here called textframe) that has five words to the left and right of the
    search term in separate columns. These columns can then be searched for 
    and sorted. 
    
    Input: 
    A nested list of lists looking like:
     [
      ['sessed of that very useful appendage  a ', 
      'voice', 
      '  for a much longer space of time than t'
      ],
     ...
         
    """

    # constructor from CLIC
      # * include loc info 
    # constructor from text concordance

    def __init__(self, concordance):
        """
        Input:
         * a concordance with [left, term, right]
         * a pattern, for instance: L2 a, term=voice
         * or a number of patterns
        """
        self.concordance = concordance
        self.KWICSPOTS = ['L5', 
                          'L4', 
                          'L3', 
                          'L2', 
                          'L1', 
                          'R1', 
                          'R2', 
                          'R3', 
                          'R4', 
                          'R5']

    def split_nodes(self):

        lines = []        
        
        for line in self.concordance:
            
            output_dict = {}
            left, term, right = line
        
            left_words = left.split()[-5:]
            # handle cases where there are not five words
            while len(left_words) < 5:
                left_words.insert(0, "")
            assert len(left_words) == 5
            left_zipped = zip(range(1,6), list(reversed(left_words)))
            
            right_words = right.split()[:5]
            while len(right_words) < 5:
                right_words.append("")
            assert len(right_words) == 5
            right_zipped = zip(range(1,6), right_words)

            for word in left_zipped:
                position = "L" + str(word[0])
                output_dict[position] = word[1]       
        
            for word in right_zipped:
                position = "R" + str(word[0])
                output_dict[position] = word[1]
            
            output_dict["term"] = term
            lines.append(output_dict)
        
        return lines

    def conc_to_df(self):
        """
        Turns a list of dictionaries with L1-R5 values into a dataframe
        which can be used as a kwicgrouper.
        """
        conc = self.split_nodes()
        df = pd.DataFrame(conc)
        cols = ["L5", "L4", "L3", "L2", "L1", "term", "R1", "R2", "R3", "R4", "R5"]
        df = df[cols]
        self.textframe = df
        return df

    def filter_textframe(self, kwdict):
        """
        Construct a dataframe slice and selector on the fly.
        This is meta-programming.
        """
        self.conc_to_df()
        begin_string = 'self.textframe['
        individual_strings = []
        end_string = ']'
        
        for val in kwdict:
            print val
            if val in self.KWICSPOTS:
                a_string = """(self.textframe.{0}.isin({1}))""".format(val, kwdict[val])
                individual_strings.append(a_string)
                print a_string
            elif val == 'sort_by':
                end_string = """].sort({0})""".format(kwdict[val])
                
        query = begin_string + ' & '.join(individual_strings) + end_string
        return eval(query)

    def args_to_dict(self,
                 # term,
                 L5=None,
                 L4=None,
                 L3=None,
                 L2=None,
                 L1=None,
                 R1=None,
                 R2=None,
                 R3=None,
                 R4=None,
                 R5=None,):
    
        """
        Helper function to use 
        L1="a" type of functions
        """
        
        local_args = locals()
        del local_args["self"]
        if local_args.values().count(None) == 10:
            raise KeyError, "You should at least choose one pattern! "
        
        pattern = copy.deepcopy(local_args)
    
        for var in local_args:
            if local_args[var] is None:
                del pattern[var]
            elif not isinstance(pattern[var], list):
                try:
                    pattern[var] = pattern[var].split()
                except:
                    raise IOError
                
        return pattern
    

if __name__ == "__main__":
    
    # example, change dir to have it working 
    concordance = concordance_for_line_by_line_file("/Users/johan/projects/annotation/data/annotation/output/dickens/textract/long_suspensions/ot_long_suspensions.txt", "voice")
    kwicgrouper = KWICgrouper(concordance)
    print kwicgrouper.filter_textframe({'L3':['in']})
