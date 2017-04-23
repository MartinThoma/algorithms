#!/usr/bin/env python
import numpy as np
import seaborn as sns
sns.set_style("whitegrid")
sns.set_palette(sns.color_palette("Greens", 8))
from scipy.ndimage.filters import gaussian_filter1d

for i in range(8):
    # Create data
    y = np.roll(np.cumsum(np.random.randn(1000, 1)),
                np.random.randint(0, 1000))
    y = gaussian_filter1d(y, 10)
    sns.plt.plot(y, label=str(i))
sns.plt.legend()
sns.plt.show()
