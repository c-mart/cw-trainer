#!/usr/bin/python

"""
Definitions:
- CW signal stream: a string of '1's and '0's representing signal on/off respectively
- Clean text: a string containing only [A-Z0-9 ] (which we can encode as CW)
"""

import math
import random
import re
import time

import numpy
import pyaudio

import cw_helpers
import audio_helpers


def multi_line_input(num_lines, prompt=None):
    """
    Accepts multi-line text input
    """
    if prompt:
        print(prompt)
    i = input()
    for line_num in range(num_lines - 1):
        i += '\n' + input()
    return i


def clean_text_cw(text):
    """
    Cleans a string prior to conversion to digital signal (converts to uppercase and strips punctuation)
    Any unrecognized characters [^A-Z0-9 ] are replaced with spaces
    """
    upper_text = text.upper()
    clean_text = re.sub('[^A-Z0-9 ]',' ',upper_text)
    return clean_text


def text_is_clean(text):
    """
    Confirms that a string of text does not have any non-CW-able characters
    """
    dirty_match = re.match('[^A-Z0-9 ]', text)
    if dirty_match:
        raise Exception("Text contains non-encodable characters")
    return True


def text_to_cw_signal(text):
    """
    Converts a clean (see above) string of alphanumeric text to a digital CW signal
    """
    cw_signal = clean_text_cw(text).translate(str.maketrans(cw_helpers.text_signal_dict))

    return cw_signal


def play_signal(pyaudio_stream, cw_signal, freq=1800, wpm=20, volume=0.25):
    """
    Takes a pyaudio_stream and a cw_signal, plays audio. Allows override of:
    - tone frequency (freq)
    - speed (wpm)
    - volume between 0 and 1
    """

    dit_duration = 1.2 / wpm  # Per https://en.wikipedia.org/wiki/Morse_code#Speed_in_words_per_minute
    sample_rate = 44100

    audio_array = []
    for char in cw_signal:
        if char == '1':
            audio_array.append(audio_helpers.sine(freq, dit_duration, sample_rate))
        else:
            audio_array.append(numpy.zeros(int(dit_duration * sample_rate)))
            pass
    chunk = numpy.concatenate(audio_array) * volume
    pyaudio_stream.write(chunk.astype(numpy.float32).tostring())


def generate_challenge(letters_pool, word_length, num_words):
    """
    Given a letters_pool and a length, generates a list of random challenge words
    """
    # TODO refactor this
    challenge_words = []
    for word in range(num_words):
        challenge_word = ''
        for letter_pos in range(word_length):
            challenge_word += random.choice(letters_pool)
        challenge_words.append(challenge_word)
    return challenge_words


def match_score(str1, str2):
    """
    Calculates match score between two strings, returns a whole number percentage. Hamming distance?
    """
    dist_count = 0
    dist_count += abs(len(str1) - len(str2))
    for char_a, char_b in zip(str1, str2):
        if char_a != char_b:
            dist_count += 1
    max_len = max(len(str1), len(str2))
    score = (max_len - dist_count) / float(max_len) * 100
    return round(score)


def process_response(challenge_words):
    response_str = multi_line_input(len(challenge_words), "Please input copied characters, one word per line")
    response_words = response_str.splitlines()
    scores = list()
    for challenge_word, response_word in zip(challenge_words, response_words):
        response_word_clean = clean_text_cw(response_word)
        scores.append(match_score(challenge_word, response_word_clean))
    overall_score = sum(scores) / float(len(scores))
    print("""
Your answer:    {0}
Correct answer: {1}
Match score:    {2}%
    """.format(response_words, challenge_words, overall_score))
    return overall_score


def main_menu(state):
    choice = input("""
Choose a number:

1. Practice CW
2. Set number of characters in pool      currently {0} containing characters {1}
3. Set word length                       currently {2}
4. Set speed                             currently {3} WPM
5. Set number of words per exercise      currently {4}
6. Exit program
    """.format(state['num_chars_learn'],
               cw_helpers.learn_chars_no_punc[:state['num_chars_learn']],
               state['word_len'],
               state['speed'],
               state['words_per_xrcise']))
    if choice == "1":
        practice_cw(state)
    elif choice == "2":
        new_num_chars_learn = int(input("""
        Enter the number of characters to learn from the following set, starting from the left:
        {0}
            5   10   15   20   25   30   35
        """.format(cw_helpers.learn_chars_no_punc)))
        assert 0 < new_num_chars_learn <= 36
        state['num_chars_learn'] = new_num_chars_learn
    elif choice == "3":
        new_word_len = int(input("Enter the new desired word length."))
        assert 0 < new_word_len < 50
        state['word_len'] = new_word_len
    elif choice == "4":
        print("Warning, not Farnsworth spacing, speed under 18 WPM not recommended.")
        new_speed = int(input("Enter the new desired CW speed in words per minute."))
        assert 0 < new_speed
        state['speed'] = new_speed
    elif choice == "5":
        new_words_per_xrcise = int(input("Enter the new desired number of words per exercise."))
        assert 0 < new_words_per_xrcise
        state['words_per_xrcise'] = new_words_per_xrcise
    elif choice == "6":
        exit()


def practice_cw(state):
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=1)
    chars_pool = cw_helpers.learn_chars_no_punc[:state['num_chars_learn']]
    print("Testing with character pool: {0}".format(chars_pool))
    challenge_words = generate_challenge(chars_pool, state['word_len'], state['words_per_xrcise'])
    time.sleep(2)
    for word in challenge_words:
        play_signal(stream, text_to_cw_signal(word + ' '), wpm=state['speed'])
    score = process_response(challenge_words)
    if score >= 90:
        resp = input("Good score! Add another letter to the pool? (y/n)")
        if resp == "y":
            state['num_chars_learn'] += 1
    stream.close()
    pa.terminate()


if __name__ == "__main__":
    state = {'num_chars_learn': 2, 'word_len': 5, 'speed': 20, 'words_per_xrcise': 5}
    while True:
        main_menu(state)