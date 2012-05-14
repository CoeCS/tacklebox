#!/usr/bin/env python

import csv
import random
import sys
import optparse
import logging

log = logging.getLogger("stableroommate")

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
            log.alert("len(names.difference(choices)) = {0} != 0".format(
                len(names.difference(choices))))
            log.alert(name, choices)
            log.alert(names.difference(choices))

            raise AssertionError(e)


        try:
            assert len(choices) == len(names) - 1
        except AssertionError, e:
            log.critical("len(choices) != len(names) - 1")
            log.critical("{0} != {1}".format(len(choices), len(names)-1))
            log.critical("{0} {1}".format(name, choices))
            raise AssertionError(e)


def verify_ranks(ranks, prefs):
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
                log.critical("m != prefs[n][idx]")
                log.critical("{0} != {1}".format(m, prefx[n][idx]))
                raise AssertionError(e)


def reject(prefs, ranks, holds):
    """
    This does a reduction of the ranks if either of the following conditions
    holds.

    (i)

    (ii)
    """

    for y in holds:

        # n holds holds[n]
        i = 0
        x = holds[y]
        while i < len(prefs[y]):
            yi = prefs[y][i]

            if yi == x:
                prefs[y] = prefs[y][:i+1]

            # lower rank is better
            elif ranks[yi][holds[yi]] < ranks[yi][y]:
                prefs[y].pop(i)
                continue
            i += 1



def find_all_or_nothing(prefs, ranks, holds):
    """
    Find an all or nothing cycle.

    Arguments:
    - `prefs`:
    - `ranks`:
    - `holds`:
    """
    p = []
    q = []

    # first find a key that has more than one pref left
    for x in sorted(prefs):
        if len(prefs[x]) > 1:
            cur = x
            break
    else:
        return None


    # trace through
    while cur not in p:
        # q_i = second person in p_i's list
        q.append( prefs[cur][1] )

        # p_{i+1} = q_i' last person
        p.append(cur)
        cur = prefs[q[-1]][-1]

    a = p[p.index(cur):]
    b = [prefs[n][0] for n in a]

    return a



def phase1(prefs, ranks, curpref=None, debug=False):
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

    log.info("-- phase 1 -----------")
    log.debug("{0}".format(people))


    for person in people:
        poser = person

        while (1):
            # find poser someone
            while curpref[poser] < len(prefs[poser]):
                # person poser is proposing to
                nchoice = prefs[poser][curpref[poser]]
                curpref[poser] += 1

                # person poser is holding
                cchoice = holds[nchoice]
                log.info("{0} proposes to {1};".format(poser,nchoice))


                # lower ranking is better
                if cchoice is None or \
                        ranks[nchoice][poser] < ranks[nchoice][cchoice]:
                    break
                log.info("{0} rejects {1};".format(nchoice, poser))


            log.info("{0} holds {1}".format(nchoice, poser))
            holds[nchoice] = poser

            if nchoice not in proposed_to:
                log.info("done")
                assert cchoice is None
                break

            log.info("and rejects {0}".format(cchoice))
            poser = cchoice

        proposed_to.add(nchoice)

    return holds



def stableroomate(prefsfn, debug=False):
    """
    find a stable roomate matching
    """

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
    verify_ranks(ranks, prefs)

    # phase1
    holds = phase1(prefs, ranks)

    log_holds(holds)

    reject(prefs, ranks, holds)

    cycle = find_all_or_nothing(prefs, ranks, holds)

    if cycle is not None and  len(cycle) == 3:
        print "no solution exists"
        return

    ## phase 2
    while cycle is not None:
        log.debug("-- cycle detected -----------")
        log.debug("{0}".format(cycle))

        curpref = {}
        for x in prefs:
            if x in cycle:
                curpref[x] = 1
            else:
                curpref[x] = 0

        holds = phase1(prefs, ranks, curpref)

        log_holds(holds)

        reject(prefs, ranks, holds)

        cycle = find_all_or_nothing(prefs, ranks, holds)



    # print prefs
    # print ranks
    return holds

def log_holds(holds):
    """

    Arguments:
    - `holds`:
    """

    log.info("-- holds -----------")
    for h in holds:
        log.info("{0} {1}".format(h, holds[h]))



def log_prefs(prefs):
    """

    Arguments:
    - `prefs`:
    """

    log.info("-- prefs -----------")
    for x in sorted(prefs):
        log.info("{0}\t{1}".format(x, " ".join(prefs[x])))


def swap_better(set1, set2, ranks):
    """
    """

    x1, y1 = set1

    x2, y2 = set2

    x1y1 = ranks[x1][y1]
    y1x1 = ranks[y1][x1]
    x2y2 = ranks[x2][y2]
    y2x2 = ranks[y2][x2]

    x1x2 = ranks[x1][x2]
    x2x1 = ranks[x2][x1]
    y1y2 = ranks[y1][y2]
    y2y1 = ranks[y2][y1]

    x2y1 = ranks[x2][y1]
    y1x2 = ranks[y1][x2]
    x1y2 = ranks[x1][y2]
    y2x1 = ranks[y2][x1]

    if x1x2 < x1y1 and x2x1 < x2y2 and y1y2 < y1x1 and y2y1 < y2x2:
        log.error("({0},{1}) ({2},{3}) -> ({4},{5}) ({6},{7})".format(
            x1, y1, x2, y2, x1, x2, y1, y2))
        log.error("({0},{1}) ({2},{3}) -> ({4},{5}) ({6},{7})".format(
            x1y1, y1x1, x2y2, y2x2, x1x2, x2x1, y1y2, y2y1))

    if x2y1 < x2y2 and y1x2 < y1x1 and x1y2 < x1y1 and y2x1 < y2x2:
        log.error("({0},{1}) ({2},{3}) -> ({4},{5}) ({6},{7})".format(
            x1, y1, x2, y2, x1, y2, x2, y1))
        log.error("({0},{1}) ({2},{3}) -> ({4},{5}) ({6},{7})".format(
            x1y1, y1x1, x2y2, y2x2, x1y2, y2x1, x2y1, y1x2))



def verify_match(matches):
    """
    """

    prefsfn = sys.argv[1]

    # read prefs from file
    prefs = readprefs(prefsfn)
    fillin(prefs)

    # generate a dictionary of rank values for each name
    ranks = dict( (idx, dict(zip(val,range(len(val)) )))
                 for idx,val in prefs.iteritems() )

    for x in matches:
        for y in matches:
            if y == x or y == matches[x]:
                continue

            set1 = (x, matches[x])
            set2 = (y, matches[y])

            swap_better(set1, set2, ranks)


def main():
    """
    main function
    """

    # random.seed(1000)

    parser = optparse.OptionParser(usage="usage: %prog [options] prefsfn")
    parser.add_option("-v", dest="validate", action="store_true",
                      default=False, help="Validate the Algorithm")
    parser.add_option("-d", dest="debug", action="store_true",
                      default=False, help="Print Debuggin Code")
    (options, args) = parser.parse_args()


    if options.debug:
        logging.basicConfig(level=logging.DEBUG)

    if len(args) < 1:
        parser.print_help()
        return

    matches = stableroomate(args[0], options.debug)

    if matches is not None:
        print("-- matches -----------")
        for m in matches:
            print "{0} {1}".format(m, matches[m])

        if options.validate:
            log.info("verifying matches...")
            verify_match(matches)




if __name__ == '__main__':
    main()
