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
def calculate_power_law(iters=100000, plot=False, plot_options={}, **params):
    quake = Earthquake(**params)
    mags = quake.run(iters)
    hist_mags = Counter(mags)

    size_logs = list(hist_mags.keys())
    mag_logs = list(hist_mags.values())

    params = linregress(np.log(size_logs), np.log(mag_logs))
    if plot: # If we're plotting, plot on a log-log scale.
        thinkplot.scatter(size_logs, np.divide(mag_logs,max(mag_logs)), label="alpha = " + str(quake.a1), **plot_options) # Normalize by the size of the list to convert to probabilities
        thinkplot.config(xlabel='Earthquake size',
             xlim=[1, 10e4],
             ylim=[10e-8, 10],
             ylabel='Number of occurrences',
             xscale='log',
             yscale='log',
             legend=True)

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
    thinkplot.scatter(a_vals, np.abs(b_vals), label='Beta')
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
def find_fractals(val=3, dim=1, plot=False, iters=100000, **params):
    n_vals = np.linspace(10,100, 19, dtype='int64')
    print(n_vals)
    cell_counts = []
    for size in n_vals:
        quake = Earthquake(n=size, fth=val, **params)
        quake.run(iters)
        bins = np.linspace(0,val,5) # Create three "bins" for the forces to fall into, from 0 to the threshold value
        bins_array = np.digitize(np.absolute(quake.array), bins=bins) # Sort the final forces on each block into bins
        fractals_list = (bins_array==dim) # Make a list of arrays with blocks in each bin
        cell_counts.append(np.sum(fractals_list))
    if plot: # If we're plotting, plot on a log-log scale.
        print(n_vals, cell_counts)
        thinkplot.plot(n_vals, cell_counts, linewidth=1)
        thinkplot.config(xlabel='Size of earthquake',
             ylabel='Number of cells',
             xscale='log',
             yscale='log',
             legend=True)
    params = linregress(np.log(n_vals), np.log(cell_counts))
    return params[0]

if __name__ == '__main__':
    calculate_power_law(iters=100,n=3,plot=True, plot_options={'color':'r'})
    # find_fractals(iters=10,plot=True)
