import pandas as pd
import numpy as np
from scipy.stats import beta
import matplotlib.pyplot as plt
import math
from pprint import pprint
from random import uniform, random, randint


fig, ax = plt.subplots(1, 1)

def get_configs():
    """

    :return:
    """

    policies = build_policies()

    return policies


def build_policies(horizon, capacity, init):
    """
    Build all policies
    :param pol_df:
    :return:
    """

    # TODO: Fetch horizon and day type values from GUI input

    H = horizon
    day_types = [1, 2]
    days_until = list(range(0, H+2))

   # print days_until

   # print H
    policies = {}
    rel_scheds = []
    for i in range(0, 10):
        for j in range(0, len(day_types)):
            schedule, vals, a, b = generate_policy(H+1, capacity, init)
            #print schedule, vals
            added = False

            # Loop to ensure we generate a random policy
            # TODO: Check if combined policies exist in policies dict before adding new daily schedule
            while not added:
                if schedule not in rel_scheds:
                    if i not in policies.keys():
                        policies[i] = {}
                    # create policy for day type
                    policies[i][j] = {}
                    policies[i][j]["CapRel"] = schedule
                    policies[i][j]["DaysUntil"] = days_until
                    # append release schedule to prevent duplicates
                    rel_scheds.append(schedule)
                    added = True

                    # plot w random color
                    ax.plot(vals, beta.cdf(vals, a, b),
                            color=(random(), random(), random()), lw=4, alpha=0.6, label='beta cdf')
                else:
                    # update policy values
                    schedule, vals, a, b = generate_policy(H+1, capacity)
    plt.show()
    return policies


def generate_policy(horizon, capacity=10, init=5):

    a, b = uniform(0.0, 20.0), uniform(0.0, 20.0)
    # generate x values ( days until ? )
    x = np.linspace(float(init)/10, 1.0, num=horizon-1)

    vals = beta.ppf(x, a, b)

    rev_vals = list(reversed(vals))

    # multiply by C-1 so our largest value is the D-1
    mult_by = lambda x: x * (capacity-init-1)
    mult_vals = map(mult_by, rev_vals)

    # add our initial value to get back to range {init:capacity}
    add_all = lambda x: x+init
    add_vals = map(add_all, mult_vals)

    # floor the values and our day release schedule is ready
    f = lambda x: int(math.floor(x))
    day_vals = map(f, add_vals)


    ret_vals = [capacity]+day_vals+[init]

    # return schedule, distribution values, alpha, and beta
    return ret_vals, vals, a, b


if __name__ == "__main__":
    pprint(build_policies(4, 10, randint(0,10)))

