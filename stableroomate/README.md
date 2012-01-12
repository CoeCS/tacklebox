# stableroomate python solution

`stableroomate.py` is an implementation Robert Irving's algorithm for
the
[stable roommates problem][wikipedia]
found in
[An efficient algorithm for the "stable roommates" problem][sciencedirect].  

## Input Format

Finding pairings is based off a preference list. Format of the
preference list is a CSV file where each row (line) is the preference
list for one person. The person is the first element in the row. The
following is example input found in the `solution_prefs.csv` file:

    1,4,6,2,5,3
    2,6,3,5,1,4
    3,4,5,1,6,2
    4,2,6,5,1,3
    5,4,2,3,6,1
    6,5,1,4,2,3
    
In this case the preference from highest to lowest for `1` is
`4,6,2,5,3`; `1` prefers `4` over all others.

*Note:* In the case where a row is missing entries, they are randomly
 generated and added to the end of the list.


## Test Input

The file `solution_prefs.csv` contains the example input, from the Irving
paper, which should generate a matching of

    1 6
    3 2
    2 3
    5 4
    4 5
    6 1

The file `nosolution_prefs.csv` contains an example of
data which doesn't have a solution.


## Execution

To run the `stableroomate.py` script pass it as an argument the
preferences file,

    ./stableroomate.py solution_prefs.csv
    

[sciencedirect]: http://www.sciencedirect.com/science/article/pii/0196677485900331
[wikipedia]: http://en.wikipedia.org/wiki/Stable_roommates_problem
