from typing import List

import numpy as np
from matplotlib import pyplot as plt # noqa
from sklearn.metrics import r2_score # noqa


def plot_curve_with_regression(sizes: List[int], times: List[float]):
    plt.scatter(sizes, times)
    plt.xlabel("Input sizes in millions")
    plt.ylabel("Execution times in seconds")
    coefs = np.polyfit(sizes, times, deg=2)
    der_coefs = np.polyder(coefs)
    print("Slope:", float(der_coefs[0]))
    x = np.linspace(min(sizes), max(sizes), num=100)
    y = np.polyval(coefs, x)
    predicted_times = np.polyval(coefs, sizes)
    r2 = r2_score(times, predicted_times)
    print("R^2:", r2)
    plt.plot(x, y, '-r')
    plt.show()
    plot_curve(sizes, times)


def plot_curve(sizes: List[int], times: List[float]):
    """
    Takes two inputs, a list of integers representing the x-axis values and a list of floats representing the y-axis values,
    and plots a curve using these two inputs:
    """
    plt.plot(sizes, times)
    plt.xlabel("Input sizes")
    plt.ylabel("Execution times")
    plt.show()