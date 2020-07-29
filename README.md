
## Markov Text Generation

One interesting problem in artificial intelligence is the . It is one of the oldest questions in computer intelligence, posed formally in the [Turing Test](https://en.wikipedia.org/wiki/Turing_test), which tests whether not a computer can be nidistinguishable from a human in a text only chat. This model however stays far away from such a task, instead attempts to generate new recourse from a single speaker based on a corpus of recorded speech or writing.

We work here with deterministic, probability based models. Building from low to high complexity, we will build and evaluate several different types of models.
This model is based on [Markov Chains](https://en.wikipedia.org/wiki/Markov_chain), where we record for every unique word, what is the distribution of words that come after that word.

Let us consider a markov chain order zero, where we do not take any progresssion of words into account. Instead, each word is randomly selected from the corpus. T

We can accomplish this using the corpus module by calling model zero


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



To begin, let us take just about the simplest way to generate text based on a corpus we could think up, and have each generated word simply be randomly sampled from out list of words. This can be accomplished with the ```zero_model``` class within the recourse module. First we will build the model, and then use the function ```gen``` to create new sentences of arbitrary length.


```python
my_model = recourse.zero_model(text)
```


```python
my_model.gen(40)
```




    'a then a the laughing mercy vast hates must must love the a and to affirmation course ended the that thing georgia jerusalem sir on north is for able was been places the you in often light master dont they'




```python
my_model = recourse.one_word_model(text)
```


```python

```


```python

```
