from pprint import pprint

import pandas as pd
import numpy as np


def make_policies(alpha, beta):
    print np.random.beta(0.03, 0.12)





def get_configs():
    """

    :return:
    """

    pol_df = pd.read_excel("configs.xlsx", sheet_name="policies")

    policies = build_policies(pol_df)

    return policies


def build_policies(pol_df):
    """
    Build all policies
    :param pol_df:
    :return:
    """
    policies = {}
    for j in range(len(pol_df)):
        if not pd.isna(pol_df.Policy[j]):
            if pol_df.Policy[j] in policies.keys():
                # if we've begun building our policy, add the day type and days until/cap release
                if pol_df.DayType[j] in policies[pol_df.Policy[j]].keys():
                    policies[pol_df.Policy[j]][pol_df.DayType[j]]['DaysUntil'].append(pol_df.DaysUntil[j])
                    policies[pol_df.Policy[j]][pol_df.DayType[j]]['CapRel'].append(pol_df.CapRel[j])
                else:
                    policies[pol_df.Policy[j]][pol_df.DayType[j]] = {"DaysUntil": [pol_df.DaysUntil[j]],
                                                                     "CapRel": [pol_df.CapRel[j]]}
            else:
                # build new policy
                policies[pol_df.Policy[j]] = {}
                # initialize lists for the day type
                policies[pol_df.Policy[j]][pol_df.DayType[j]] = {"DaysUntil": [pol_df.DaysUntil[j]],
                                                                 "CapRel": [pol_df.CapRel[j]]}

    return policies

if __name__ == "__main__":
    from scipy.stats import beta
    import matplotlib.pyplot as plt
    import math
    from random import uniform

    fig, ax = plt.subplots(1, 1)

    a, b = uniform(0.0, 10.0), uniform(0.0, 10.0)

    x = np.linspace(0, 1.0, num=4)

    vals = beta.ppf(x, a, b)

    rev_x = list(reversed(x))
    rev_vals =  list(reversed(vals))

    mult_by = lambda x: x*10
    mult_vals = map(mult_by, list(reversed(vals)))
    f = lambda x: math.floor(x)

    floor_vals =  map(f, list(reversed(mult_vals)))

    print list(x)
    print floor_vals

    ax.plot(vals, beta.cdf(vals, a, b),
            'g-', lw=4, alpha=0.6, label='beta cdf')


    plt.show()