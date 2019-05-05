import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
import sys

directory = sys.argv[1]

fig, axes = plt.subplots(nrows=2, ncols=2, sharex="none", sharey="none")
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.9, hspace=0.4)

def scientific_notation(number):
    ex = 0
    while number >= 10:
        number = number / 10.0
        ex = ex + 1
    return str(float(number)) + r'\times 10^{%d}' % ex if number != 1.0 else r'10^{%d}' % ex


def scientific_notation_as_tex(number):
    return '$' + scientific_notation(number) + '$'


@ticker.FuncFormatter
def major_formatter(x, pos):
    return r"$2^{-" + scientific_notation(x) + "}$" if x != 0.1 else "1"


shipPlot = axes[0][0]
shipPlot.set(xlabel=r'$v \; / \; |C_{all}|$', ylabel=r'$P(\mathbf{T}^{\Omega_L}_{strat} \leq v)$', title="Ship distribution random Strat for different dimensions")
shipPlot.xaxis.label.set_size(14)
shipPlot.yaxis.label.set_size(14)
shipPlot.axis((0, 1, 0, 1))

shipPlot2 = axes[0][1]
shipPlot2.set(xlabel=r'$v \; / \; |C_{all}|$', ylabel=r'$P(\mathbf{T}^{\Omega_L}_{strat} \leq v)$', title="Ship distribution random Strat zoom 1")
shipPlot2.xaxis.label.set_size(14)
shipPlot2.yaxis.label.set_size(14)
shipPlot2.axis((0, 1, 0, 1))

shipPlot3 = axes[1][0]
shipPlot3.set(xlabel=r'$v \; / \; |C_{all}|$', ylabel=r'$P(\mathbf{T}^{\Omega_L}_{strat} \leq v)$', title="Ship distribution random Strat zoom 2")
shipPlot3.xaxis.label.set_size(14)
shipPlot3.yaxis.label.set_size(14)
shipPlot3.axis((0, 1, 0, 1))

shipPlot4 = axes[1][1]
shipPlot4.set(xlabel=r'$D$', ylabel=r'$v \; / \; |C_{all}|$', title=r'Expected Value of shots $v$ relative to total cell count $|C_{all}|$')
shipPlot4.xaxis.label.set_size(14)
shipPlot4.yaxis.label.set_size(14)

dimensions = list();
expectedShip = list();

def load_and_plot(file):
	f = open(os.path.join(directory, file), "r")
	strings = f.read().split(" ")
	file_strings = os.path.splitext(file)[0].split("-")

	n = int(file_strings[1])
	d = int(file_strings[2])
	dimensions.append(d);

	name = ""
	if len(file_strings) > 3:
		name = file_strings[3]

	runs = int(1)
	if len(file_strings) > 4:
		runs = int(file_strings[4])	

	sample_size = int(int(strings[0]) / runs)
	ships = float(strings[1])
	cells = int(strings[2])
	
	xs = [0]
	ys_1 = [0]
	ys_2 = [ships]
	for i in range(3, len(strings) - 2):
		if d > 6 and i % 3 != 0:
			continue
		v = strings[i].split(',')
		x = int(v[0]) / float(cells)
		xs.append(x)
		y_1 = float(v[1])
		ys_1.append(y_1)
		y_2 = -float(v[2])
	if y_2 == 0.0:
			y_2 = 0.1
        ys_2.append(y_2)

	sample_space = r"$\Omega_L=L_{all}$" if ships == sample_size else r"$|\Omega_L|=$" + scientific_notation_as_tex(sample_size)
	runs_str = " @ " + str(runs) + " run(s)" if runs > 1 else ""
	dims_str = "0" + str(d) if d < 10 else str(d)
	l = shipPlot.step(xs,ys_1, where="post", label=name + " n=" + str(n) + ", d=" + dims_str + ", " + sample_space + runs_str)

	expected_ships = float(strings[len(strings) - 2])
	expectedShip.append(expected_ships / cells);
	shipPlot.axvline(x=(expected_ships / cells), color=l[0].get_color(), linestyle='--')
	
	shipPlot2.step(xs,ys_1, where="post")
	shipPlot3.step(xs,ys_1, where="post")

for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        load_and_plot(filename)

handles, labels = shipPlot.get_legend_handles_labels()
labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
shipPlot.legend(handles, labels, bbox_to_anchor=(1.05, 0.5), loc='upper left', borderaxespad=0.)

shipPlot4.plot(dimensions,expectedShip,'o', color='black')

plt.show()

fig.savefig("foo.pdf", bbox_inches='tight')
