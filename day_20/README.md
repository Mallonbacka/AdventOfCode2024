# Day 20

`solve_part1_old.py` contains my first approach, which naively tries removing each wall and running a breadth-first search. This worked, but was painfully slow (total running time around 5 minutes). 

Eventually, I realized that I could, instead, operate on the distances list, and search for distances within a reachable Manhattan distance of one another. This was much faster and eventually worked well. 