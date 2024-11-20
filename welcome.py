# %% [markdown]
# # Welcome to your Jupyter Notebook
# This is a sample notebook for your project.
# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print('Hello, Jupyter!')

# %% [markdown]
# ## Data Analysis Example
# Let's create a simple plot

# %%
x = np.linspace(0, 10, 100)
y = np.sin(x)
plt.plot(x, y)
plt.title('Sample Plot')
plt.show()