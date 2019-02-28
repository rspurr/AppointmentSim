import math
from pprint import pprint
from random import uniform, random, randint

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import beta

# pyplot objects for graphing the policies
fig, ax = plt.subplots(1, 1)


def build_policies(horizon, capacity, initital_release):
    """
    Builds the policies for the simulation to run.
    :param horizon: horizon specified by gui input, determines how many days to look in advance
    :param capacity: total capacity that can be released
    :param initital_release: capacity to release immediately for 'horizon' days in the future
    :return: policies a map of policies with keys as integers and values as the release schedule
    """

    # hard code day types for now
    day_types = [1, 2]
    days_until = list(range(0, horizon + 2))

    policies = {}
    rel_scheds = []

    # generate 10 different policies to run
    for i in range(0, 10):
        # generate a release schedule for each day type
        for j in range(0, len(day_types)):
            # generate a policy with the specified parameters
            schedule, vals, a, b = generate_policy(horizon + 1, capacity, initital_release)
            added = False
            tries = 0

            # Loop to ensure we generate a random policy that hasn't been added to the policy dict already
            # abandon loop if we somehow can't generate one in 1000 tries (perhaps there's an upper bound here?)
            # TODO: Check if combined policies exist in policies dict before adding new daily schedule
            while not added or tries > 1000:
                tries += 1
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
                    schedule, vals, a, b = generate_policy(horizon + 1, capacity)
        print i
    # plot the release schedules that were generated
    plt.show()
    return policies


def generate_policy(horizon, capacity=10, init=5):
    """
    Generate a release schedule (policy) for 'horizon' days
    :param horizon: how many days to generate the release schedule for
    :param capacity: total available capacity for a day
    :param init: initial release for the horizon-th day
    :return: release schedule, distribution values, alpha value, and beta value
    """

    # pick a random alpha and beta value for the Beta Distribution
    a, b = uniform(0.0, 20.0), uniform(0.0, 20.0)

    """
        Generate the x-axis values for the Beta Distribution.
        Specifically, linspace returns evenly spaced numbers over 
        the interval of [(initial_release/capacity), 1]
        since the Beta Distribution needs x-values from [0, 1]
        but we only want values starting at our initial release
    """
    x = np.linspace(float(init) / capacity, 1.0, num=horizon - 1)

    """
        Generate the percent point function, which is the inverse
        of the cumulative distribution function. Each value from
        the list of x-values will be a point in the distribution.
        We use this technique to generate 'horizon' percentages from 0.0->1.0
        to multiply capacity by. This achieves a capacity release between
        [init, capacity] for each day.
    """
    vals = beta.ppf(x, a, b)

    # print vals

    # reverse the values, since we want the maximum amount of capacity
    # to be released 0 days out (basically reverse prob distribution to range
    # from [1, 0])
    rev_vals = list(reversed(vals))

    # Multiply each PPF value by Capacity-Initial_Release-1
    mult_by = lambda x: x * (capacity-init-1)
    mult_vals = map(mult_by, rev_vals)
    print mult_vals

    # Add our Initial_Release value to get back to range [init,capacity]
    # This ensures our largest value is Capacity-1 and the smallest is
    # at least greater than or equal to the Initial_Release
    add_all = lambda x: x+init
    add_vals = map(add_all, mult_vals)
    print add_vals

    # Floor the values so we can obtain integers
    # NOTE: We can use either floor or ceiling here,
    # and the difference in function will yield different
    # results for cap_released , perhaps make it a variable
    f = lambda x: int(math.floor(x))
    day_vals = map(f, add_vals)

    # create release schedule by inserting our randomly generated
    # values between Capacity and Initial_Release
    ret_vals = [capacity]+day_vals+[init]

    # return release schedule, distribution values, alpha, and beta
    return ret_vals, vals, a, b


if __name__ == "__main__":
    pprint(build_policies(4, 10, randint(0, 10)))
