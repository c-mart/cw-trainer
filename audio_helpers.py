#!/usr/bin/python

import numpy
import math

def sine(freq, duration, rate):
    array_len = int(duration * rate)
    factor = float(freq) * (math.pi * 2) / rate
    return numpy.sin(numpy.arange(array_len) * factor)