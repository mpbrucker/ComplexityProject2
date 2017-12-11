from quake import Earthquake
import thinkplot
from scipy.signal import welch
from scipy.stats import linregress
import numpy as np
from collections import Counter
from thinkstats2 import Cdf
import matplotlib.pyplot as plt
import logging
import matplotlib
matplotlib.rc('figure', figsize=(8,6))
matplotlib.rc('font', size=18)


"""
Determines the exponent (b) of the power law distribution of earthquake sizes.
"""
def calculate_power_law(iters=100000, plot=False, del_bottom=False, plot_options={}, **params):
    quake = Earthquake(**params) # Create new quake
    mags = quake.run(iters)
    hist_mags = Counter(mags)

    if del_bottom: # Delete all entries with a frequency of 1
        all_keys = list(hist_mags.keys())
        for item in all_keys:
            if hist_mags[item] == 1:
                del hist_mags[item]
    # print(hist_mags)


    size_vals = list(hist_mags.keys())
    mag_list = list(hist_mags.values())
    mag_vals = np.divide(mag_list,len(mags)) # Create PMF of magnitudes


    mag_cdf = Cdf(mag_vals) # Create CDF of magnitudes
    params = linregress(np.log(size_vals), np.log(mag_vals)) # Create linear

    if plot: # If we're plotting, plot on a log-log scale.
        plt.figure(1)
        thinkplot.scatter(size_vals, mag_vals, label="alpha = " + str(quake.a1), **plot_options) # Normalize by the size of the list to convert to probabilities
        thinkplot.config(xlabel='Earthquake size',
             xlim=[1, 10e3],
             ylim=[10e-9, 1],
             ylabel='Probability of occurrences',
             xscale='log',
             yscale='log',
             legend=True)
        plt.figure(2)
        thinkplot.Cdf(mag_cdf, label="alpha = " + str(quake.a1), **plot_options)
        thinkplot.config(xlabel='Earthquake size', xscale='log',
                 ylabel='CDF')
    logging.info('B = ' + str(params[0]))

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
    quake.run(iters) # Get the list of the number of sliding blocks each timestep
    amp = quake.slide_seq
    logging.info("Running Welch's Algorithm")
    nperseg = 1024
    freqs, powers = welch(amp, nperseg=nperseg, fs=nperseg)
    if plot: # If we're plotting, plot on a log-log scale.
        thinkplot.plot(freqs, powers, linewidth=1)
        thinkplot.config(xlabel='Frequency',
             ylabel='Power',
             xscale='log',
             yscale='log',
             title='Power spectrum of earthquake signal')
    params = linregress(np.log(freqs[1:]), np.log(powers[1:])) # Remove the first element
    return params[0]

"""
Estimates the fractal dimension of the earthquake.
"""
def find_fractals(val=4, plot=False, dims=range(4), iters=10000, **params):
    n_vals = np.linspace(10,100, 19, dtype='int64')
    n_vals2 = np.power(n_vals, 2)
    cell_counts = [[] for _ in range(len(dims))]
    all_params = []

    thinkplot.preplot(rows=2,cols=2)
    for size in n_vals:
        logging.info('Size: '+ str(size))
        quake = Earthquake(n=size,fth=val, **params)
        quake.run(iters)
        bins = np.linspace(0,val,max(dims)) # Create three "bins" for the forces to fall into, from 0 to the threshold value
        bins_array = np.digitize(np.absolute(quake.array), bins=bins) # Sort the final forces on each block into bins
        for dim in dims:
            fractals_list = (bins_array==dim+1) # Make a list of arrays with blocks in each bin
            cell_counts[dim].append(np.sum(fractals_list))
    if plot: # If we're plotting, plot on a log-log scale.
        # print(n_vals, cell_counts)
        for dim in dims:
            thinkplot.subplot(dim+1)
            thinkplot.plot(n_vals, n_vals, linestyle='dashed')
            thinkplot.plot(n_vals, n_vals2, linestyle='dashed')
            thinkplot.plot(n_vals, cell_counts[dim], linewidth=1)
            thinkplot.config(xlabel='Size of earthquake',
                 ylabel='Number of cells',
                 xscale='log',
                 yscale='log',
                 title='Dimension: '+ str(dim))
            params = linregress(np.log(n_vals), np.log(cell_counts[dim]))
            all_params.append(params[0])
    
    return all_params

if __name__ == '__main__':
    # calculate_power_law(iters=1000,n=35,plot=True, del_bottom=True, plot_options={'color':'r'})
    print(plot_frequency(iters=2000,plot=True,n=35))
    # find_fractals(iters=10,plot=True)
