#!/usr/bin/env python

import csv
import random
import sys

def readprefs(prefsfn):
    """
    read the preferences from "prefs.csv"
    """
    inner = csv.reader(open(prefsfn))

    prefs = {}


    for line in inner:
        if len(line) == 0: continue
        line = [s.strip() for s in line]
        prefs[line[0]] = line[1:]

    return prefs

def fillin(prefs):
    """
    some choices may not include everyone.

    fill in the rest by rearranging the others available at random.
    """

    names = set(prefs.keys())

    for name, choices in prefs.iteritems():

        left = set(names).difference([name]).difference(choices)


        if len(left) > 0:
            left = list(left)
            random.shuffle(left)
            choices.extend(left)

def checkprefs(prefs):
    """
    - `prefs`: preferences dict, name key, list of names as choices in order
    """

    names = set(prefs.keys())

    for name, choices in prefs.iteritems():
        try:
            assert len(names.difference(choices)) == 1
        except AssertionError, e:
            print
            print "len(names.difference(choices)) = {0} != 0".format(
                len(names.difference(choices)))
            print name, choices
            print names.difference(choices)

            raise AssertionError(e)


        try:
            assert len(choices) == len(names) - 1
        except AssertionError, e:
            print
            print "len(choices) != len(names) - 1"
            print "{0} != {1}".format(len(choices), len(names)-1)
            print name, choices
            raise AssertionError(e)


def checkranks(ranks, prefs):
    """
    check that ranks and prefs correspond

    Arguments:
    - `ranks`: dict mapping name to rank index
    - `prefs`: preferences dict, name key, list of names as choices in order
    """

    for n in ranks:
        for m in ranks[n]:
            idx = ranks[n][m]
            try:
                assert m == prefs[n][idx]
            except AssertionError(e):
                print "m != prefs[n][idx]"
                print "{0} != {1}".format(m, prefx[n][idx])


def reject(prefs, ranks, holds):

    for y in holds:
        # n holds holds[n]
        i = 0
        x = holds[y]
        while i < len(prefs[y]):
            yi = prefs[y][i]
            # print y, x, yi, ranks[yi][holds[yi]], ranks[yi][y]
            if yi == x:
                prefs[y] = prefs[y][:i+1]
            # lower rank is better
            elif ranks[yi][holds[yi]] < ranks[yi][y]:
                prefs[y].pop(i)
                continue
            i += 1



def find_all_or_nothing(prefs, ranks, holds):
    """

    Arguments:
    - `prefs`:
    - `ranks`:
    - `holds`:
    """
    p = []
    q = []

    for x in sorted(prefs):
        if len(prefs[x]) > 1:
            cur = x
            break
    else:
        return None


    while cur not in p:
        # q_i = second person in p_i's list
        q.append( prefs[cur][1] )

        # p_{i+1} = q_i' last person
        p.append(cur)
        cur = prefs[q[-1]][-1]

    a = p[p.index(cur):]
    b = [prefs[n][0] for n in a]


    # print a
    # print b
    return a





def phase1(prefs, ranks, curpref=None):
    """
    perform phase 1 of the stable roomates problem.

    Arguments:
    - `prefs`: preferences dict, name key, list of names as choices in order
    - `ranks`: dict mapping name to rank index
    """

    # holds
    holds = dict( (name,None) for name in prefs.keys() )

    if curpref is None:
        curpref = dict( (name, 0) for name in prefs.keys() )

    people = prefs.keys()
    random.shuffle(people)


    proposed_to = set()


    print "-- phase 1 -----------"
    print people


    for person in people:
        # # randomly pick someone
        # cur = random.choice(list(unpicked))
        # unpicked.remove(cur)

        poser = person

        while (1):


            # find poser someone
            while curpref[poser] < len(prefs[poser]):
                # person poser is proposing to
                nchoice = prefs[poser][curpref[poser]]
                curpref[poser] += 1

                # person poser is holding
                cchoice = holds[nchoice]
                print "{0} proposes to {1};\t".format(poser,nchoice),
                # if cchoice is not None:
                #     print ranks[nchoice][poser],
                #     ranks[nchoice][cchoice]


                # lower ranking is better
                if cchoice is None or \
                        ranks[nchoice][poser] < ranks[nchoice][cchoice]:
                    break
                print "{0} rejects {1};".format(nchoice, poser)


            print "{0} holds {1}".format(nchoice, poser),
            holds[nchoice] = poser

            if nchoice not in proposed_to:
                print ";"
                assert cchoice is None
                break

            print "and rejects {0}".format(cchoice)
            poser = cchoice

        # print "Solution Possible: {0}".format(poser == nchoice)
        proposed_to.add(nchoice)


    print

    return holds



def stableroomate():
    """
    find a stable roomate matching
    """

    # random.seed(100)
    random.seed(1000)

    if len(sys.argv) < 2:
        print "requires a filename argument"
        return

    prefsfn = sys.argv[1]

    # read prefs from file
    prefs = readprefs(prefsfn)

    # make sure everyone has the same number of choices
    fillin(prefs)

    # validate that names are correct
    checkprefs(prefs)

    # generate a dictionary of rank values for each name
    ranks = dict( (idx, dict(zip(val,range(len(val)) )))
                 for idx,val in prefs.iteritems() )

    # validate the ranks correspond to the proper indices
    checkranks(ranks, prefs)

    # phase1
    holds = phase1(prefs, ranks)

    print_holds(holds)

    reject(prefs, ranks, holds)

    cycle = find_all_or_nothing(prefs, ranks, holds)

    if cycle is not None and  len(cycle) == 3:
        print "no solution exists"
        return

    while cycle is not None:
        print "-- cycle detected -----------"
        print cycle
        print

        curpref = {}
        for x in prefs:
            if x in cycle:
                curpref[x] = 1
            else:
                curpref[x] = 0

        holds = phase1(prefs, ranks, curpref)
        print_holds(holds)

        reject(prefs, ranks, holds)

        cycle = find_all_or_nothing(prefs, ranks, holds)
        print "cycle:", cycle



    # print prefs
    # print ranks

def print_holds(holds):
    """

    Arguments:
    - `holds`:
    """

    print "-- holds -----------"
    for h in holds:
        print h, holds[h]

    print


def print_prefs(prefs):
    """

    Arguments:
    - `prefs`:
    """

    print "-- prefs -----------"
    for x in sorted(prefs):
        print "{0}\t".format(x),
        for y in prefs[x]:
            print y,
        print

    print

if __name__ == '__main__':
    stableroomate()
