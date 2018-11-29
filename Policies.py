import pandas as pd
import numpy as np
from scipy.stats import beta
import matplotlib.pyplot as plt
import math
from pprint import pprint
from random import uniform, random


def get_configs():
    """

    :return:
    """

    policies = build_policies()

    return policies


def build_policies():
    """
    Build all policies
    :param pol_df:
    :return:
    """

    # TODO: Fetch horizon and day type values from GUI input
    H = 5
    day_types = [1, 2]
    capacity = 10
    days_until = list(range(1, H))

    fig, ax = plt.subplots(1, 1)
    policies = {}
    rel_scheds = []
    for i in range(0, 10):
        for j in range(0, len(day_types)):
            print i, j
            vals, schedule = generate_policy(H, capacity)
            added = False

            # Loop to ensure we generate a random policy

            while not added:
                if schedule not in rel_scheds:

                    if i not in policies.keys():
                        policies[i] = {}
                    policies[i][j] = {}
                    policies[i][j]["CapRel"] = schedule[:-1]
                    policies[i][j]["DaysUntil"] = days_until
                    rel_scheds.append(schedule)
                    added = True
                else:
                    vals, schedule = generate_policy(H, capacity)


    plt.show()

    pprint(policies)
    print ""
    pprint(get_configs())

    return policies


def generate_policy(horizon, capacity=10):
    a, b = uniform(0.0, 10.0), uniform(0.0, 10.0)
    # generate x values ( days until ? )
    x = np.linspace(0, 1.0, num=horizon)

    # create percentage point function
    vals = beta.ppf(x, a, b)

    # reverse our values to emulate days until
    rev_vals = list(reversed(vals))

    # multiply by 9 so our largest value is the daily capacity-1
    mult_by = lambda x: x * (capacity-1)
    mult_vals = map(mult_by, rev_vals)

    # floor the values and our day release schedule is ready
    f = lambda x: int(math.floor(x))
    day_vals = map(f, mult_vals)

    ax.plot(vals, beta.cdf(vals, a, b),
            color=(random(), random(), random()), lw=4, alpha=0.6, label='beta cdf')

    return vals, day_vals


if __name__ == "__main__":

