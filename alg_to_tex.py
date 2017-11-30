#!/usr/bin/python3

import sys
from graph import *
import os
import argparse


parser=argparse.ArgumentParser()

parser.add_argument("dotfile", help="A graph-definition file, in DOT format", type=str)
parser.add_argument("prefix", help="A file prefix", type=str)
parser.add_argument("-l", "--layout", type=int, help="The number of figures to be packed on a same line of the page")
parser.add_argument("-r", "--linewidth-ratio", type=float, help="The width taken by a single graph, as a ratio of the linewidth")
parser.add_argument("-b", "--blank", help="Generate an exercise template, with blank value fields", action="store_true" )
parser.add_argument("-s", "--standalone", help="Generate a self-contained LaTeX document, instead of inline LaTeX code", action="store_true" )
parser.add_argument("-d", "--description-string", type=str, help="The description string to be used in the key box. Ex.  'CLRS3, Exercise 6.1-3'")
parser.add_argument("-a", "--algorithm", type=str, help="Algorithm: 'dfs' or 'bfs'.")
parser.add_argument("-v", "--vertex", type=str, help="Start vertex")

args = parser.parse_args()

# 3 diagrams row in the LaTeX page
layout = 4
if args.layout is not None:
	layout = args.layout
	

g = Graph.from_dot( args.dotfile)

os.system('rm -f {}[0-9]*'.format(args.prefix))

if args.algorithm=='dfs':
	g.depth_first( args.prefix, blank=args.blank )
	algorithm_str = "Depth-First Search"
elif args.algorithm=='topo':
	g.topo_sort( args.prefix, blank=args.blank )
	algorithm_str = "Topological Sort"
elif args.algorithm=='dijkstra':
	g.dijkstra( args.vertex, args.prefix, blank=args.blank )
	algorithm_str = "Dijkstra Shortest Path"
elif args.algorithm=="dag-shortest-path":
	g.dag_shortest_path( args.vertex, args.prefix, blank=args.blank)
	algorithm_str = "DAG Shortest Path"
elif args.vertex is not None:
	g.breadth_first( args.vertex, args.prefix, blank=args.blank )
	algorithm_str = "Breadth-First Search"

os.system('for i in {}*[0-9].dot; do eps=${{i%.dot}}.eps ; dot -Teps $i > $eps ; done'.format(args.prefix) )

diagrams = list( filter(lambda x: x.startswith(args.prefix) and x.endswith('.eps'),   os.listdir()  ))


preamble = """ \\documentclass{article}
\\usepackage{manfnt,amsmath,amsfonts,amssymb}
\\usepackage{clrscode3e,latexsym}
\\usepackage{graphicx,subfig}
\\usepackage[margin=.5in]{geometry}
\\usepackage{tikz}
\\usepackage{enumitem,booktabs,array}
\\usepackage{color}
"""



preamble +='\\title{{Graph Algorithms: {}}}'.format( algorithm_str )
preamble += '\\begin{document}'
preamble += '\\maketitle'
preamble += '\\newcommand\\HR{\\rule{.5em}{.4pt}}'
if args.standalone:
	description_string = 'CLRS3, ' + ('DFS' if args.algorithm=='dfs' else 'BFS')
	if args.description_string is not None:
		description_string = args.description_string
	print(preamble)

	print('\\fbox{'
		'\\begin{minipage}{\\linewidth}'
		'{\\sl Example: ' + description_string + '}'
		'\\end{minipage}}'
		'\\vspace{1em}\n\n')

diagrams.sort()

ratio = 1/(layout*1.1)


for d in range(0,len(diagrams)):
	if d%layout == 0:
		print('\\vspace{1em}\n\n')
	else:
		print('\\vspace{1em}')
	if d==len(diagrams)-1 and not args.blank:
		#print('\\HR')
		print('\\begin{{minipage}}[b][.25\\textheight]{{{}\\linewidth}}'.format(ratio))
		print('The resulting subgraph: ')
		print('\\includegraphics[height=.25\\textheight]{{{}}}'.format(diagrams[d] ))	
		print('\\end{minipage}')
	else:
		if args.linewidth_ratio is not None:
			print('\\includegraphics[width={}\\linewidth]{{{}}}'.format( args.linewidth_ratio, diagrams[d] ))	
		else:
			print('\\includegraphics[height=.3\\textheight]{{{}}}'.format(diagrams[d] ))	
if args.standalone:
	print('\n\\end{document}')





