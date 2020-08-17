import numpy
import string
import random



#Zeroth order model. Generates words uniformly randomly
class zero_model:
    def gen(self, n = 20):
        newtext = []

        for i in range(n):
            newtext.append(random.choice(self.cleaned))
        return " ".join(newtext)
    
    def __init__(self, corpus):
        self.cleaned = corpus
        
    
   
#One word Markov model. 
class one_word_model:   
   
    def gen(self, n = 20):
    
        #set up generation with empty list and random seed word.
        newtext = []
        current = random.choice(self.cleaned)
        newtext.append(current)

        for i in range(n-1):
            #grab dist for current word
            dist = self.P[self.unique.index(current), :]
            
            #random number between 0 and 1
            chooser = random.uniform(0,1)
            
            #placeholder. will later be column id of next chosen word
            choice = 0
            
            #subtract from chooser.
            #column that exhausts the chooser is our next choice
            #only words that followed current word in text will have >0 prob
            while chooser > 0:
                chooser = chooser - dist[choice]
                choice = choice + 1
                
            #adjusting for choice increase at end of loop
            choice = choice - 1
            
            #add chosen word. current word is now chosen word
            newtext.append(self.unique[choice])
            current = self.unique[choice]
            
        #return text as string instead of list
        return " ".join(newtext) 


    def __init__(self, corpus):
        #taking out punctuation
        nopunc = []

        table = str.maketrans({key: None for key in string.punctuation})
        
        for w in corpus:
            nopunc.append(w.translate(table))

        self.cleaned = [word.lower() for word in nopunc]
        
        
        self.unique = []
        self.cleanlen = len(self.cleaned)
        
        #list of all unique words
        for i in self.cleaned:
            if i not in self.unique:
                self.unique.append(i)
        
        #number of unique words
        self.nuniq = len(self.unique)
        
        #placeholder square matrix
        self.P = numpy.zeros((self.nuniq,self.nuniq))
        
        #scanning next recording order of words
        for i in range(self.cleanlen-1):
            self.P[self.unique.index(self.cleaned[i]), 
            self.unique.index(self.cleaned[i+1])] = self.P[self.unique.index(self.cleaned[i]), 
            self.unique.index(self.cleaned[i+1])] + 1
        
        #adjusting matrix to have probabilities instead of counts
        for t in range(numpy.shape(self.P)[0]):
            self.P[t,:] = self.P[t,:] / self.cleaned.count(self.unique[t])        

    
class two_word_model:

    def gen(self, n = 20):
        
        #Set up generation with empty list. Randomly generate starting pair of words.
        newtext = []
        
        randomint = random.randint(0,self.cleanlen)
        current = [self.cleaned[randomint], self.cleaned[randomint + 1]]
        
        newtext.append(current[0])
        newtext.append(current[1])

        
        for i in range(n-1):
            #grab distribution (row) for current pair
            dist = self.P2[self.unique.index(current), :]
            
            #random number between 0, and 1
            chooser = random.uniform(0,1)
            choice = 0
            
            #subtract each column from chooser.
            #column that fully depletes is choice
            while chooser > 0:
                chooser = chooser - dist[choice]
                choice = choice + 1
            
            #adjusting for iteration style
            choice = choice - 1
            
            #adding new word to list, make new current pair 
            newtext.append(self.uniqueone[choice])
            current = [current[1], self.uniqueone[choice]]
        
        #joining list of new words
        return(" ".join(newtext))
        
        
    def __init__(self, corpus):
        
        #set up
        self.cleaned = [word.lower() for word in corpus] #list of text
        self.unique = [] #list of unique pairs
        self.cleanlen = len(self.cleaned) #number of words in text
        counts = numpy.zeros((self.cleanlen,1)) #count of each unique pair of words
        self.uniqueone = [] #list of unique words
        
        #getting all unique individual words
        for i in self.cleaned:
            if i not in self.uniqueone:
                self.uniqueone.append(i)
        
        #getting all unique pairs of words
        for i in range(self.cleanlen-1):
            if [self.cleaned[i], self.cleaned[i+1]] not in self.unique:
                self.unique.append([self.cleaned[i],self.cleaned[i+1]])
                
            #recording counts to later scale by
            counts[list(self.unique).index([self.cleaned[i],self.cleaned[i+1]])] = counts[list(self.unique).index([self.cleaned[i],self.cleaned[i+1]])] + 1
        
        # number of unique words
        self.nuniq = len(self.uniqueone)
        
        #empty P matrix of shape (# of unique pairs) x (# of unique words)
        self.P2 = numpy.zeros((numpy.shape(self.unique)[0],self.nuniq))

        #model building
        #shifting reading frame, based on current two, add one to the column of next word in their distribution
        for i in range(self.cleanlen-2):
            self.P2[list(self.unique).index([self.cleaned[i], self.cleaned[i+1]]), self.uniqueone.index(self.cleaned[i+2])] = self.P2[list(self.unique).index([self.cleaned[i], self.cleaned[i+1]]), self.uniqueone.index(self.cleaned[i+2])] + 1
        
        #scaling by row sum to have matrix of probabilities instead of counts
        for t in range(numpy.shape(self.P2)[0]):
            self.P2[t,:] = self.P2[t,:] / counts[t]
        


 
 