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
    df = pd.read_excel("configs.xlsx", sheet_name="conf")

    configs = []

    for num in range(len(df)):
        simulation = dict(H=df.H[num],
                          c=df.c[num],
                          D=df.D[num],
                          Ha=df.Ha[num],
                          Pf=df.Pf[num],
                          Hf=df.Hf[num],
                          gamma=df.gamma[num],
                          beta=df.beta[num],
                          lam=8.5*(1.-df.Pf[num])
                          )

        configs.append(simulation)

    return configs
