# Coe CS Toolbox

Repository of useful tools for CS at Coe.  Includes scripts
to help management of class repositories and templates for Makefiles.

## Makefile

This is a generic `Makefile` that can be used to easily compile a
single executable that depends only it's corresponding source file
(.c).  Using this file you can type `make fun` to compile `fun.c` and
output as `fun`.  


## blankbranch.sh

Shell script to create a new *blank* git branch in the current
directory.


## stableroomate

Contains the `stableroomate.py` script to calculate stable pairings
based off a preference list.  Format of the preference list is a CSV
file where each row (line) is the preference list for one person.  The
person is the first element in the list.  The following is example
input found in the `stableroomate/solution_prefs.csv` file:

    1,4,6,2,5,3
    2,6,3,5,1,4
    3,4,5,1,6,2
    4,2,6,5,1,3
    5,4,2,3,6,1
    6,5,1,4,2,3
    
In this case the preference from highest to lowest for `1` is
`4,6,2,5,3`; `1` prefers `4` over all others.

The file `stableroomate/nosolution_prefs.csv` contains an example of
data which doesn't have a solution.

### Execution

To run the `stableroomate.py` script pass it as an argument the
preferences file,

    ./stableroomate.py solution_prefs.csv
    

