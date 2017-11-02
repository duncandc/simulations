#!/bin/bash

curl -u chinchilla:chirp --max-time 10800 "http://www.slac.stanford.edu/~beckermr/chinchilla/Lb250/hlists/hlist_1.00000.list" -o ./lb250_hlist_1.00000.list
curl -u chinchilla:chirp --max-time 10800 "http://www.slac.stanford.edu/~beckermr/chinchilla/Lb125/hlists/hlist_1.00000.list" -o ./lb125_hlist_1.00000.list

