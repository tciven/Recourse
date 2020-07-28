import numpy
import string
import random

class zero_model:
    def gen(self,n):
        newtext = []
        

        for i in range(n):
            newtext.append(random.choice(self.cleaned))
        return " ".join(newtext)
    
    def __init__(self, corpus):
        self.cleaned = corpus
        
    
    

class one_word_model:   
   
    def gen(self, n = 20):
        newtext = []
        current = random.choice(self.cleaned)
        newtext.append(current)

        for i in range(n-1):
            dist = self.P[self.unique.index(current), :]
            
            chooser = random.uniform(0,1)
            choice = 0
            
            while chooser > 0:
                chooser = chooser - dist[choice-1]
                choice = choice + 1
            choice = choice
            newtext.append(self.unique[choice])
            current = self.unique[choice]
            
         
        return " ".join(newtext) 

    def __init__(self, corpus):
    
        nopunc = []

        table = str.maketrans({key: None for key in string.punctuation})
        
        for w in corpus:
            nopunc.append(w.translate(table))

        self.cleaned = [word.lower() for word in nopunc]
        
        
        self.unique = []
        self.cleanlen = len(self.cleaned)
        
        for i in self.cleaned:
            if i not in self.unique:
                self.unique.append(i)
        
        self.nuniq = len(self.unique)
        
        self.P = numpy.zeros((self.nuniq,self.nuniq))

        for i in range(self.cleanlen-1):
            self.P[self.unique.index(self.cleaned[i]), 
            self.unique.index(self.cleaned[i+1])] = self.P[self.unique.index(self.cleaned[i]), 
            self.unique.index(self.cleaned[i+1])] + 1
            
        for t in range(numpy.shape(self.P)[0]):
            self.P[t,:] = self.P[t,:] / self.cleaned.count(self.unique[t])        

    
class two_word_model:

    def gen(self, n = 20):
        
        newtext = []
        randomint = random.randint(0,self.cleanlen)
        current = [self.cleaned[randomint], self.cleaned[randomint + 1]]
        newtext.append(current[0])
        newtext.append(current[1])

        for i in range(n-1):
            dist = self.P2[self.unique.index(current), :]
            
            chooser = random.uniform(0,1)
            choice = 0
            
            while chooser > 0:
                chooser = chooser - dist[choice]
                choice = choice + 1
            choice = choice - 1
            newtext.append(self.uniqueone[choice])
            current = [current[1], self.uniqueone[choice]]
        
        return(" ".join(newtext))
        
        
    def __init__(self, corpus):
        nopunc = []
        
        """
        table = str.maketrans({key: None for key in string.punctuation})
        for w in corpus:
            nopunc.append(w.translate(table))

        self.cleaned = [word.lower() for word in nopunc]
        """
        
        self.cleaned = [word.lower() for word in corpus]
        self.unique = []
        self.cleanlen = len(self.cleaned)        
        
        counts = numpy.zeros((self.cleanlen,1))
        
        self.uniqueone = []
        
        for i in self.cleaned:
            if i not in self.uniqueone:
                self.uniqueone.append(i)
        
        
        for i in range(self.cleanlen-1):
            if [self.cleaned[i], self.cleaned[i+1]] not in self.unique:
                self.unique.append([self.cleaned[i],self.cleaned[i+1]])
                
            
            counts[list(self.unique).index([self.cleaned[i],self.cleaned[i+1]])] = counts[list(self.unique).index([self.cleaned[i],self.cleaned[i+1]])] + 1

        self.nuniq = len(self.uniqueone)
        
        


        self.P2 = numpy.zeros((numpy.shape(self.unique)[0],self.nuniq))

        
        for i in range(self.cleanlen-2):
            self.P2[list(self.unique).index([self.cleaned[i], self.cleaned[i+1]]), self.uniqueone.index(self.cleaned[i+2])] = self.P2[list(self.unique).index([self.cleaned[i], self.cleaned[i+1]]), self.uniqueone.index(self.cleaned[i+2])] + 1
            
        for t in range(numpy.shape(self.P2)[0]):
            self.P2[t,:] = self.P2[t,:] / counts[t]
        


 
 