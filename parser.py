import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
import sys

directory = sys.argv[1]

fig, axes = plt.subplots(nrows=2, ncols=1, sharex="none", sharey="none", constrained_layout=True)

shipPlot = axes[0]
shipPlot.set(xlabel=r'$v \; / \; |C_{all}|$', ylabel=r'$P(\mathbf{T}^{\Omega_L}_{strat} \leq v)$', title="Ship distribution")
shipPlot.xaxis.label.set_size(14)
shipPlot.yaxis.label.set_size(14)
shipPlot.axis((0, 1, 0, 1))

fleetPlot = axes[1]
fleetPlot.yaxis.label.set_size(14)
fleetPlot.xaxis.label.set_size(14)
fleetPlot.set(xlabel=r'$v \; / \; |C_{all}|$', ylabel=r'$P(\mathbf{X}^{F_{all}}_{strat} \leq v)$', title="Fleet distribution")
fleetPlot.set_yscale("log")
fleetPlot.yaxis.set_major_formatter(ticker.FormatStrFormatter(r"$2^{-%d}$"))


def load_and_plot(file):
    f = open(os.path.join(directory, file), "r")
    strings = f.read().split(" ")
    file_strings = os.path.splitext(file)[0].split("-")

    n = int(file_strings[1])
    d = int(file_strings[2])

    name = ""
    if len(file_strings) > 3:
        name = file_strings[3]

    runs = int(1)
    if len(file_strings) > 4:
        runs = int(file_strings[4])

    sample_size = int(int(strings[0]) / runs)
    ships = int(strings[1])
    cells = int(strings[2])

    xs = [0]
    ys_1 = [0]
    ys_2 = [ships]
    for i in range(3, len(strings) - 2):
        v = strings[i].split(',')
        x = int(v[0]) / float(cells)
        xs.append(x)
        y_1 = float(v[1])
        ys_1.append(y_1)
        y_2 = -int(v[2])
        ys_2.append(y_2)

    sample_space = r"$\Omega_L=L_{all}$" if ships == sample_size else r"$|\Omega_L|=$" + str(sample_size)
    runs_str = " @ " + str(runs) + " run(s)" if runs > 1 else ""
    l = shipPlot.step(xs,ys_1, label=name + " n=" + str(n) + ", d=" + str(d) + ", " + sample_space + runs_str)
    shipPlot.legend(loc='lower right', borderaxespad=0.)

    expected_ships = float(strings[len(strings) - 2])
    shipPlot.axvline(x=(expected_ships / cells), color=l[0].get_color(), linestyle='--')

    l = fleetPlot.step(xs,ys_2, label=name + " n=" + str(n) + ", d=" + str(d))
    fleetPlot.legend(loc='lower right', borderaxespad=0.)
    fleetPlot.axis((0, 1, ships, 0))

    expected_fleets = float(strings[len(strings) - 1])
    fleetPlot.axvline(x=(expected_fleets / cells), color=l[0].get_color(), linestyle='--')


for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        load_and_plot(filename)

plt.show()
