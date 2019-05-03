import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
import sys
from decimal import *

directory = sys.argv[1]

fig, axes2 = plt.subplots(nrows=2, ncols=2, sharex="none", sharey="none")
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

fleetPlot = axes2[0][0]
fleetPlot.yaxis.label.set_size(14)
fleetPlot.xaxis.label.set_size(14)
fleetPlot.set(xlabel=r'$v \; / \; |C_{all}|$', ylabel=r'$P(\mathbf{X}^{F_{all}}_{strat} \leq v)$', title="Fleet distribution random Strat for different dimensions")
fleetPlot.set_yscale("log", basey=10)
fleetPlot.yaxis.set_major_formatter(major_formatter)

fleetPlot2 = axes2[0][1]
fleetPlot2.yaxis.label.set_size(14)
fleetPlot2.xaxis.label.set_size(14)
fleetPlot2.set(xlabel=r'$D$', ylabel=r'$v \; / \; |C_{all}|$', title=r'Expected Value zoom 1')

fleetPlot3 = axes2[1][0]
fleetPlot3.yaxis.label.set_size(14)
fleetPlot3.xaxis.label.set_size(14)
fleetPlot3.set(xlabel=r'$D$', ylabel=r'$v \; / \; |C_{all}|$', title=r'Expected Value zoom 2')

fleetPlot4 = axes2[1][1]
fleetPlot4.yaxis.label.set_size(14)
fleetPlot4.xaxis.label.set_size(14)
fleetPlot4.set(xlabel=r'$D$', ylabel=r'$v \; / \; |C_{all}|$', title=r'Expected Value of shots $v$ relative to total cell count $|C_{all}|$')

dimensions = list();
expectedFleet= list();

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
		#print(ys_2)
		

	sample_space = r"$\Omega_L=L_{all}$" if ships == sample_size else r"$|\Omega_L|=$" + scientific_notation_as_tex(sample_size)
	runs_str = " @ " + str(runs) + " run(s)" if runs > 1 else ""
	dims_str = "0" + str(d) if d < 10 else str(d)

	
	
	
	l = fleetPlot.step(xs,ys_2, where="post", label=name + " n=" + str(n) + ", d=" + dims_str + ", " + sample_space + runs_str)
	fleetPlot.axis((0, 1, ships, 0.1))

	expected_fleets = float(strings[- 1])
	expectedFleet.append(expected_fleets / cells);
	fleetPlot.axvline(x=(expected_fleets / cells), color=l[0].get_color(), linestyle='--')
	

for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        load_and_plot(filename)

handles, labels = fleetPlot.get_legend_handles_labels()
labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
fleetPlot.legend(handles, labels, bbox_to_anchor=(1.05, 0.5), loc='upper left', borderaxespad=0.)

fleetPlot2.plot(dimensions,expectedFleet,'o', color='black')
fleetPlot3.plot(dimensions,expectedFleet,'o', color='black')
fleetPlot4.plot(dimensions,expectedFleet,'o', color='black')

plt.show()

fig.savefig("foo.pdf", bbox_inches='tight')
