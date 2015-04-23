#!/bin/bash
python -ic "from simulator import *
def reload(): reload_sim(globals())"
