from quake import Earthquake
import thinkplot
from thinkstats2 import Hist, Cdf
from scipy.signal import welch
from scipy.stats import linregress
import numpy as np
from collections import Counter


"""
Determines the exponent (b) of the power law distribution of earthquake sizes.
"""
def calculate_power_law(iters=100000, plot=False, **params):
    quake = Earthquake(**params)
    mags = quake.run(iters)
    hist_mags = Counter(mags)
    sizes = range(max(mags)) # Build the list of earthquake sizesj

    size_logs = list(hist_mags.keys())
    mag_logs = list(hist_mags.values())


    params = linregress(np.log(size_logs), np.log(mag_logs))
    if plot: # If we're plotting, plot on a log-log scale.
        thinkplot.scatter(size_logs, mag_logs)
        thinkplot.config(xlabel='Earthquake size',
             xlim=[1, list(sizes)[-1]],
             ylabel='Number of occurrences',
             xscale='log',
             yscale='log')

    return params[0]

"""
Determines the exponent (b) of the power law distribution of the earthquake across a variety of elasticity coefficients.
"""
def plot_power_law(test_range=(0.05, 0.25), **params):
    b_vals = [] # Build the list of exponents as a function of elasticity coefficient
    a_vals = np.linspace(*test_range, num=20) # Build a list of elasticity coefficients
    for alpha in a_vals:
        K_val = 1
        KL_val = K_val/alpha - 4*K_val # Calculate KL based on K and alpha
        exponent = calculate_power_law(k1=K_val, kl=KL_val, **params)
        b_vals.append(exponent)
    thinkplot.scatter(a_vals, b_vals, label='Beta')
    thinkplot.config(xlabel='Elasticity coefficient',
                      ylabel='Exponent B')

"""
Plots the powers of various frequencies in the 'signal' created by the earthquakes.
"""
def plot_frequency(iters=100000, plot=False, **params):
    quake = Earthquake(**params)
    amp = quake.run(iters) # Get the list of the number of sliding blocks each timestep
    nperseg = 2048
    freqs, powers = welch(amp, nperseg=nperseg, fs=nperseg)
    if plot: # If we're plotting, plot on a log-log scale.
        thinkplot.plot(freqs, powers, label='Power', linewidth=1)
        thinkplot.config(xlabel='Frequency',
             ylabel='Power',
             xscale='log',
             yscale='log')
    params = linregress(np.log(freqs), np.log(powers))
    return params[0]

"""
Estimates the fractal dimension of the earthquake.
"""
def find_fractals(dim=1, plot=False, iters=100000, **params):
    n_vals = np.linspace(10,100, 20)
    cell_counts = []
    for size in n_vals:
        quake = Earthquake(n=size, **params)
        quake.run_quake(iters)
        bins = np.linspace(0,val,5)
        bins_array = np.digitize(quake.array) # Sort the final forces on each block into bins
        fractals_list = (bins_array==dim) # Make a list of arrays with blocks in each bin
        cell_counts.append(sum(fractals_list))
    if plot: # If we're plotting, plot on a log-log scale.
        thinkplot.plot(n_vals, cell_counts, label='Filled cells', linewidth=1)
        thinkplot.config(xlabel='Size of earthquake',
             ylabel='Number of cells',
             xscale='log',
             yscale='log')
    params = linregress(np.log(n_vals), np.log(cell_counts))
    return params[0]

if __name__ == '__main__':
    calculate_power_law(iters=100,n=3,plot=True)
