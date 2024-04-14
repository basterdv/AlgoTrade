import matplotlib.pyplot as plt
import pandas as pd

import numpy as np

plt.style.use('_mpl-gallery')

# make data:
# у - длинна полоски, х - расположение

x = [[1, 1.5, 1.5, 2, 2.5, 6], [3, 1, 2, 4, ], [2, 5, 7, 8, 5, 3]]
y = [[0, 0, 0.25, 0.75, 0.15, 1], [1, 0.15, 1, 1, ], [0.5, 0.25, 0, 0, 0, 1]]
df = pd.DataFrame(x)
unique_time = df.index.get_level_values(0).unique().sort_values()
ylabels = unique_time.astype(str)
print(df)
print(ylabels)

# D = np.random.gamma(4, size=(4, 10))
D = [[1.5, 2, 1.5, 4, 5, 6, 7, 7, 8, 1.5],
     [3, 2, 1, 6, 5, 2, 3, 4, 2, 2],
     [1, 4, 3, 2, 3, 2, 3, 4, 4, 3],
     [3, 4, 4, 5, 4, 3, 6, 7, 9, 1]]

# plot:
fig, ax = plt.subplots(figsize=(5, 5))

# ax.eventplot(D, orientation="vertical", lineoffsets=x, linewidth=0.75)

# ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
#        ylim=(0, 8), yticks=np.arange(1, 8))

# ax.set_title("   ".join(symbol), fontsize=60)

ax.yaxis.set_ticks_position('right')
ax.set_xlim([-0.5, 5])
# ax.set_ylim([-1, 5])
for i in range(len(x)):
    ax.barh(x[i], y[i], 0.3, i, color='green')
    # print(i)


# ax.barh(x, y, 0.3, 0, color='green')
# ax.barh(x2, y2, 0.3, 1, color='red')

plt.show()
