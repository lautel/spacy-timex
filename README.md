# spacy-timex
Detect temporal expressions in the input text and return it with TIMEX3 tags 

## Usage

First, you can check whether language models that you have downloaded are compatible with the currently installed version of spaCy by running the following command:
````python
python3 -m spacy validate
````

Then, run the main script providing an input sentence 
````python
python main.py -i "Let's have a meeting on Friday at 11:30"
>> Let's have a meeting on <TIMEX3 tid=t0 type=DATE value=2021-01-01>Friday</TIMEX3> at <TIMEX3 tid=t1 type=TIME value=T11:30>11:30</TIMEX3>

we had a meeting yesterday at 5pm
>> we had a meeting <TIMEX3 tid=t0 type=DATE value=2020-12-29>yesterday</TIMEX3> at <TIMEX3 tid=t1 type=TIME value=T17:00>5pm</TIMEX3>

````
## Limitations
* Still a lot to do on converting date strings to proper TIMEX3 values.
* DURATION and some SET values aren't properly defined yet following timeML annotation.
* Also note that the output strongly depends on entities detected by spaCy, which varies according to the model used. 