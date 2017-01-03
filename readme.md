# Koch Method CW Trainer

- Command-line trainer program/game generates and plays CW using Koch method
- Copy down what you hear and receive a score
- Prompts you to add another letter when you achieve 90%+ comprehension
- Configurable pool of letters, speed, word length, etc.

## How to Use

numpy and pyaudio must be available, and pyaudio requires portaudio19-dev (Debian/Ubuntu package). The following commands should get you going on Debian/Ubuntu.

```
$ sudo apt-get install portaudio19-dev
$ virtualenv cw-venv
$ source cw-venv/bin/activate
$ pip install -r requirements.txt
$ python cw.py
```

## Example Session

```
$ python cw.py

Choose a number:

1. Practice CW
2. Set number of characters in pool      currently 2 containing characters KM
3. Set word length                       currently 5
4. Set speed                             currently 20 WPM
5. Set number of words per exercise      currently 5
6. Exit program
    1
Testing with character pool: KM
Please input copied characters, one word per line
kmmmm
mkkkk
mkmkk
kmkkk
kmkmk

Your answer:    ['kmmmm', 'mkkkk', 'mkmkk', 'kmkkk', 'kmkmk']
Correct answer: ['KMMMM', 'MKKKK', 'MKMKK', 'KMKKK', 'KMKMK']
Match score:    100.0%
    
Good score! Add another letter to the pool? (y/n)
```