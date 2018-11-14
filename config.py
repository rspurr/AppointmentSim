from pprint import pprint

import pandas as pd


parameters = {
    "H": 0,
    "c": 0,
    "D": 0,
    "Ha": 0,
    "Pf": 0.0,
    "Hf": 0,
    "gamma": 0.0,
    "beta": 0.0
}


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
