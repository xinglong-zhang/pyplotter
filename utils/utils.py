from cycler import cycler



default_cycler = (cycler(color=['r', 'g', 'b', 'y']) +
                  cycler(linestyle=['-', '--', ':', '-.']))

custom_cycler = (cycler(color=['c', 'm', 'y', 'k']) +
                 cycler(lw=[1, 2, 3, 4]))

color_cycler = cycler(color=['r', 'g', 'b', 'y', 'c', 'm', 'y', 'k'])
linestyle_cycler = cycler(linestyle=['-', '--', ':', '-.'])
linewidth_cycler = cycler(lw=[1, 2, 3, 4])

colors = ['r', 'g', 'b', 'y', 'c', 'm', 'y', 'k']
