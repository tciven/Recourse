
## Markov Text Generation

One interesting problem in artificial intelligence is the . It is one of the oldest questions in computer intelligence, posed formally in the [Turing Test](https://en.wikipedia.org/wiki/Turing_test), which tests whether not a computer can be nidistinguishable from a human in a text only chat. This model however stays far away from such a task, instead attempts to generate new recourse from a single speaker based on a corpus of recorded speech or writing.

We work here with deterministic, probability based models. Building from low to high complexity, we will create and evaluate several different types of models all based on [Markov Chains](https://en.wikipedia.org/wiki/Markov_chain).

Markov Chains describe a 
Here, we will define a state to be a word that we have just generated, and this state will have a transition proabbilities based on every word that came after it in the provided corpus.


```python
import recourse
import re
```

For this example I will be using speeches given by Dr. Martin Luther King Jr. I selected him not only for his imprtance but also his characteristic style of speeh, which I wanted to see how well this model could capture. The test is from Richten Park Public LIbrary, and the download for the original document can be found [here](wmasd.ss7.sharpschool.com/common/pages/UserFile.aspx?fileId=8373388).

A text file is in this repository of a cleaner version of this pdf, however it still contains a lot of puncuation and requires just a little more prep before it is ready to go into a model. We need an all lower case list of the words in order without puncuation (discussion of the impact of this on the model will be discussed later).


```python
corpus = open("king.txt","r")
text = corpus.read() 
corpus.close()
text = re.sub("[^A-Za-z0-9 ]+", "", text)
text = text.split()
text = [word.lower() for word in text]
```


```python
text[0:20]
```




    ['mr',
     'chairman',
     'distinguished',
     'platform',
     'associates',
     'fellow',
     'americans',
     'three',
     'years',
     'ago',
     'the',
     'supreme',
     'court',
     'of',
     'this',
     'nation',
     'rendered',
     'in',
     'simple',
     'eloquent']



To begin, let us take just about the simplest way to generate text based on a corpus we could think up, and have each generated word simply be randomly sampled from the corpus. This can be accomplished with the ```zero_model``` class within the recourse module. First we will build the model, and then use the function ```gen``` to create new sentences of arbitrary length.


```python
model_zero = recourse.zero_model(text)
```


```python
model_zero.gen(35)
```




    'universe the for best compassion out you in about give thousand built saying leaders and the get refuse i truth impractical of and by dignity course best of heritage independence richton the destroys by also'



This appraoch performs about as well as we could expect. While the vocabulary seems right, all together the language is unsurprisingly garbled.

To improve on this, let's build a model based on Markov Chains.

To build our model, we will record the order of the text, meaning counting how often words follow other words. What we will end up with is a list of distributions, one for each unique word in the text. The distributions will tell us what words tend to follow the current word. 

The function one_word_model takes a body of text (formatted in one string) and returns a model object.


```python
model_one = recourse.one_word_model(text)
```

Once we have these distributions encased in our model object, we are ready to generate! 

We can randomly choose a starting "seed" word, and then use its distribution in our matrix to generate the next word, use that next word's distribution to generate a third, and so on. The gen function in every model object will do just that. All it needs is the amount of words desired.


```python
print(model_one.gen(35))
```

    and that they had to ultimate reality is approaching spiritual yes maybe we do his policemen have a result of life is that enhance the light though i have been successful journey on ahead weve
    

Here the language becomes a little more free flowing, but is still nearly unintelligable. We can improve on this by building a new model that does not just consider what follows every unique word, but what follows every unique pair of words. This lets it have a little more context in generation.


```python
model_two = recourse.two_word_model(text)
```


```python
model_two.gen(35)
```




    'come treading our paths through the vista of eternity those stars that appear to be a great nation with all the other thing is that communism forgets that life as we kill a million acres of'



Now we can see even more nuanced characteristics of language appearing. This is as far as I have taken the module as of now, but there is still a lot of room for improvement.

## Notes on Potential Improvements
While these models have their moments, there is room for a lot of improvement. Chief amoung these is the lack of any way to define sentences, it just goes on until it reaches the spcified number of words. I think a more intuitive way to build speech would be instead of words, ask the model for a certain number of sentences and let it determine their length.

1. Determine the distribution of sentence lengths in the corpus and sample from that distribution to decide where to place commas
2. Keep the words that end sentences as denoted by ending in a "." distinct from the same words that does not. For example "things" would be a different word in the model, and have different movement probabilites than "things." 

The first option is computationally very cheapbut would add very little to the quality of the generator rhetoric. It does essentially the same operation and sprinkles in a couple of periods for flair. 

The second option, while requiring more thought in implementation, would guarantee that every first/last word in a generated sentence began/ended one sentence in the text. This would add coherence both within and between sentences. It is however exposed to more situations where the next geenrated word would be deterministic (only one time that word ended a sentence in the text). Also, there is the chance that some sentences can become very stuck in words that do not typically end sentences, and they can become unnaturally long. Additionally, because the size of the p matrices is the number of unique words (/word pairs) squared, significant increases beyond the number of unique words here (44448) (what a great number) can cause serious issues with storage of the matrix (10,000 unique words would be 100 million floating point numbers to store, and 800+ megabytes of RAM to store the model!!).

This brings us to the last thought, which is that this problem of model storage generalizes to all of these markov models no matter what type of system is used. One area to explore is the storeage of sparse matrices. Out of all the unique words, only very few ever appear next to each other, and there could be massive gains made by reducing the load of the build models by utilizing something like a dictionary of keys or a coordinate list.
