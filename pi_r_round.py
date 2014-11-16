#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
is210 Section 01 Week 12

Bench marking methods

Works Cited:

    The following Pi calculation functions were sourced from the "Captian
    DeadBones Chronicles" blog posting "Computing Pi With Python".

    http://thelivingpearl.com/2013/05/28/computing-pi-with-python/

    Minor changes were made to conform with lesson plan.

"""

import math
# from decimal import *
from decimal import Decimal
import time
import sys


class Timer2Class(object):
    '''dicstring'''
    timer = time.clock if sys.platform[:3] == 'win' else time.time

    def __init__(self, func, *args, **kwargs):
        '''basic parts of the class'''
        self.func = func
        self.args = args
        self.kwargs = kwargs

    # def total(self, reps, func, *pargs, **kargs):
    def total(self):
        '''
        Total time to run func() reps times.
        Returns (total time, last result)
        '''
        _reps = self.kwargs.pop('_reps', 1000)
        repslist = list(range(_reps))
        start = self.timer()
        for i in repslist:
            # ret = self.func(*pargs, **kargs)
            ret = self.func(*self.args)
        elapsed = self.timer() - start
        return (elapsed, ret)

    # def bestof(self, func, *pargs, **kargs):
    def bestof(self):
        '''
        Quickest func() among reps runs.
        Returns (best time, last result)
        '''
        _reps = self.kwargs.pop('_reps', 5)
        best = 2 ** 32
        for i in range(_reps):
            start = self.timer()
            # ret = self.func(*pargs, **kargs)
            ret = self.func(*self.args)
            elapsed = self.timer() - start
            if elapsed < best:
                best = elapsed
        return (best, ret)

    # def bestoftotal(self, reps1, reps2, func, *pargs, **kargs):
    def bestoftotal(self):
        '''
        Best of totals:
        (best of reps1 runs of (total of reps2 runs of func))
        '''
        _reps1 = self.kwargs.pop('_reps1', 5)
        return (self.func.__name__, min(self.total() for i in range(_reps1)))


def stdlib(depth):
    """
    Calculate Pi using the math.pi from Python standard library

    :param depth:
    :return:
    """
    a_dec = Decimal(1.0)
    b_dec = Decimal(1.0 / math.sqrt(2))
    t_dec = Decimal(1.0) / Decimal(4.0)
    p_dec = Decimal(1.0)

    for i in range(depth):
        at_dec = Decimal((a_dec + b_dec) / 2)
        bt_dec = Decimal(math.sqrt(a_dec * b_dec))
        tt_dec = Decimal(t_dec - p_dec * (a_dec - at_dec) ** 2)
        pt_dec = Decimal(2 * p_dec)

        a_dec = at_dec
        b_dec = bt_dec
        t_dec = tt_dec
        p_dec = pt_dec

    pies = (a_dec + b_dec) ** 2 / (4 * t_dec)

    return str(pies)


def bbp(depth):
    """
    Calculate Pi using the Bailey–Borwein–Plouffe formula
    http://en.wikipedia.org/wiki/Bailey%E2%80%93Borwein%E2%80%93Plouffe_formula

    :param depth:
    :return:
    """
    pies = Decimal(0)
    k = 0
    while k < depth:
        pies += (Decimal(1) / (16 ** k)) * (
            (Decimal(4) / (8 * k + 1)) -
            (Decimal(2) / (8 * k + 4)) -
            (Decimal(1) / (8 * k + 5)) -
            (Decimal(1) / (8 * k + 6))
        )
        k += 1
    return str(pies)


def bellard(depth):
    """
    New school Pi calculation method discovered in 1997 by Fabrice Bellard in
    1997. Usually clocks in 43% faster than the BBP formula.

    http://en.wikipedia.org/wiki/Bellard%27s_formula

    :param depth:
    :return:
    """
    pies = Decimal(0)
    k = 0
    while k < depth:
        pies += (Decimal(-1) ** k / (1024 ** k)) * (
            Decimal(256) / (10 * k + 1) +
            Decimal(1) / (10 * k + 9) -
            Decimal(64) / (10 * k + 3) -
            Decimal(32) / (4 * k + 1) -
            Decimal(4) / (10 * k + 5) -
            Decimal(4) / (10 * k + 7) -
            Decimal(1) / (4 * k + 3)
        )
        k += 1
    pies = pies * 1 / (2 ** 6)
    return str(pies)


def chudnovsky(depth):
    """
    World record holding formula for calculating 5 trillion digits of Pi in
    August 2010. It's a heavy hitter on CPU. This one is about quality over
    quantity.

    http://en.wikipedia.org/wiki/Chudnovsky_algorithm

    :param depth:
    :return:
    """
    pies = Decimal(0)
    k = 0
    while k < depth:
        pies += (Decimal(-1) ** k) * (
            Decimal(math.factorial(6 * k)) /
            (
                (math.factorial(k) ** 3) * (math.factorial(3 * k))
            ) * (13591409 + 545140134 * k) /
            (640320 ** (3 * k))
        )
        k += 1
    pies = pies * Decimal(10005).sqrt() / 4270934400
    pies **= -1
    return pies


if __name__ == "__main__":

    number = 1000

    for test in (stdlib, bbp, bellard, chudnovsky):
        timer2 = Timer2Class(test, number, _reps1=1, _reps=3)
        print timer2.bestoftotal()