"""Script for running multithreaded powerlaw calculations
When run directly it
"""
from multiprocessing import Pool, TimeoutError
import numpy as np
from matplotlib import rc
rc('animation', html='html5')
import matplotlib.pyplot as plt

from Cell2D import Cell2DViewer
import thinkplot

from plot_quake import calculate_power_law
from quake import Earthquake

def power_law_wrapper(params):
    """Unpacks parameters for calculate_power_law function"""
    return calculate_power_law(**params)

def calc_power_law_range_multithreaded(test_range=(0.05, 0.25),
                         test_def=20,
                         processes=4,
                         **params):
    pool = Pool(processes)
    b_vals = [] # Build the list of exponents as a function of elasticity coefficient
    a_vals = np.linspace(*test_range, num=test_def) # Build a list of elasticity coefficients
    K_val = 1
    KL_vals = K_val/a_vals - 4*K_val  # Calculate KL based on K and alpha

    # keywords = [{"k1": K_val, "kl":kl, **params} for kl in KL_vals]  # build keywords into list for process distribution
    keywords = []
    for kl in KL_vals:
        kwd = {'k1': K_val, "kl":kl}
        kwd.update(params)
        keywords.append(kwd)

    b_vals = pool.map(power_law_wrapper, keywords)
    # b_vals = pool.apply(calculate_power_law, kwds=keywords)

    return a_vals, b_vals

def calc_power_law_range(test_range=(0.05, 0.25),
                         test_def=20,
                         **params):
    b_vals = [] # Build the list of exponents as a function of elasticity coefficient
    a_vals = np.linspace(*test_range, num=test_def) # Build a list of elasticity coefficients
    for alpha in a_vals:
        K_val = 1
        KL_val = K_val/alpha - 4*K_val # Calculate KL based on K and alpha
        exponent = calculate_power_law(k1=K_val, kl=KL_val, **params)
        b_vals.append(exponent)

    return a_vals, b_vals

def plot_power_law(a_vals, b_vals):
    thinkplot.scatter(a_vals, np.abs(b_vals), label='Beta')
    thinkplot.config(xlabel='Elasticity coefficient',
    ylabel='Exponent B')


if __name__ == "__main__":
    from os.path import exists
    import sys
    import pickle
    import types

    import datetime
    timestamp = str(datetime.datetime.now())

    params = {
        "processes": 4,
        "test_range": (0.05, 0.25),
        "test_def": 15,
        "iters": 100,
        "n": 35
    }

    a_vals, b_vals = calc_power_law_range_multithreaded(**params)

    run = types.SimpleNamespace(**{
        "params": params,
        "results": (a_vals, b_vals)
    })

    pickle.dump(run, open("replication_" + timestamp + ".p", "wb"))

    plot_power_law(a_vals, b_vals)
    # thinkplot.save("powerlaw_" + timestamp)
    plt.savefig("powerlaw_" + timestamp + ".pdf")
