from typing import Callable
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit

def func(t, v, k):
    """ Computes the function S(t) with constants v and k """
    return v * np.exp(-k * t)

def find_constants(df: pd.DataFrame, func: Callable):
    """ Returns the constants v and k """
    t = df['t'].values
    S = df['S'].values

    # Fit the curve using SciPy to estimate v and k
    popt, _ = curve_fit(func, t, S)
    v, k = popt

    return v, k

if __name__ == "__main__":
    df = pd.read_csv("data.csv")
    v, k = find_constants(df, func)
    v = round(v, 4)
    k = round(k, 4)
    print(v, k)

    # Generate predicted values using the estimated constants
    t = df['t'].values
    S_pred = func(t, v, k)

    # Plot a histogram of the residuals
    residuals = df['S'].values - S_pred
    plt.hist(residuals, bins=30, edgecolor='black')
    plt.title("Histogram of Residuals")
    plt.xlabel("Residual")
    plt.ylabel("Frequency")
    plt.savefig("fit_curve.png")
    plt.show()
