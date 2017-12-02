  



pdfs = bfs_undirected_classroom.pdf bfs_undirected_classroom_key.pdf bfs_directed_classroom.pdf bfs_directed_classroom_key.pdf clrs_example_bfs.pdf clrs_example_bfs_key.pdf clrs_example_dfs.pdf clrs_example_dfs_key.pdf dfs_directed_classroom.pdf dfs_directed_classroom_key.pdf dfs_undirected_classroom.pdf dfs_undirected_classroom_key.pdf dijkstra_gross_yellen.pdf dijkstra_gross_yellen_key.pdf dag_shortest_path.pdf dag_shortest_path_key.pdf dag_228_key.pdf clrs_24-2.pdf clrs_24-2_key.pdf undirected_graph_homework_bfs_key.pdf undirected_graph_homework_dfs_key.pdf directed_graph_homework_bfs_key.pdf directed_graph_homework_dfs_key.pdf pert_chart_key.pdf



all: $(pdfs)

$(pdfs): %.pdf : %.tex
	pdflatex $<

bfs_undirected_classroom.tex: %.tex : undirected_graph_classroom.dot
	../alg_to_tex.py -b -l 3 -s -d "Classroom example, undirected graph" -a bfs -v 'a' $< $*_ > $@


bfs_undirected_classroom_key.tex: %.tex : undirected_graph_classroom.dot
	../alg_to_tex.py -l 3 -s -d "Classroom example, undirected graph" -a bfs -v 'a' $< $*_ > $@


bfs_directed_classroom.tex: %.tex : directed_graph_classroom.dot
	../alg_to_tex.py -b -l 4 -s -d "Classroom example, directed graph" -a bfs -v 'a' $< $*_ > $@

bfs_directed_classroom_key.tex: %_key.tex : directed_graph_classroom.dot
	../alg_to_tex.py -l 4 -s -d "Classroom example, directed graph" -a bfs -v 'a' $< $*_ > $@

dfs_directed_classroom.tex: %.tex : directed_graph_classroom.dot
	../alg_to_tex.py -b -l 4 -s -d "Classroom example, directed graph" -a dfs $< $*_ > $@

dfs_directed_classroom_key.tex: %_key.tex : directed_graph_classroom.dot
	../alg_to_tex.py -l 4 -s -d "Classroom example, directed graph" -a dfs $< $*_ > $@

dag_228_key.tex: %_key.tex : dag_228.dot
	../alg_to_tex.py -l 3 -s -d "CLRS3, 22.8 example: topological sort" -a topo $< $*_ > $@

dfs_undirected_classroom.tex: %.tex : undirected_graph_classroom.dot
	../alg_to_tex.py -b -l 3 -s -d "Classroom example, undirected graph" -a dfs $< $*_ > $@

dfs_undirected_classroom_key.tex: %_key.tex : undirected_graph_classroom.dot
	../alg_to_tex.py -l 3 -s -d "Classroom example, undirected graph" -a dfs $< $*_ > $@

clrs_example_bfs.tex: %.tex : %.dot
	../alg_to_tex.py -b -l 3 -s -d "CLR3, Figure 22.3, p.~596, undirected graph" -a bfs -v 's' $< $*_ > $@

clrs_example_bfs_key.tex: %_key.tex : %.dot
	../alg_to_tex.py -l 3 -s -r .25 -d "CLR3, Figure 22.3, p.~596, undirected graph" -a bfs -v 's' $< $*_ > $@

clrs_example_dfs.tex: %.tex : %.dot
	../alg_to_tex.py -b -l 3 -s -d "CLR3, Figure 22.4, p.~605, directed graph" -a dfs $< $*_ > $@

clrs_example_dfs_key.tex: %_key.tex : %.dot
	../alg_to_tex.py -l 3 -s -r .25 -d "CLR3, Figure 22.4, p.~605, directed graph" -a dfs $< $*_ > $@

dijkstra_gross_yellen.tex: %.tex : %.dot
	../alg_to_tex.py -b -l 3 -s -d "Gross \& Yellen, p.~180" -a dijkstra -v s $< $*_ > $@ 

dijkstra_gross_yellen_key.tex: %_key.tex : %.dot
	../alg_to_tex.py -l 3 -s -d "Gross \& Yellen, p.~180" -a dijkstra -v s $< $*_ > $@

dag_shortest_path.tex: %.tex : weighted_dag.dot
	../alg_to_tex.py -b -l 5 -s -d "DAG Shortest Path, CLRS 24.2, Figure 24.5" -a dag-shortest-path -v 's' $< $*_ > $@

dag_shortest_path_key.tex: %_key.tex : weighted_dag.dot
	../alg_to_tex.py -l 5 -s -d "DAG Shortest Path, CLRS 24.2, Figure 24.5" -a dag-shortest-path -v s $< $*_ > $@ 

clrs_24-2.tex: %.tex : weighted_dag.dot
	../alg_to_tex.py -b -l 4 -s -d "CLRS exercise 24.2-1, weighted DAG" -a dag-shortest-path -v r $< $*_ > $@ 

clrs_24-2_key.tex: %_key.tex : weighted_dag.dot
	../alg_to_tex.py -l 4 -s -d "CLRS exercise 24.2-1, weighted DAG" -a dag-shortest-path -v r $< $*_ > $@ 


undirected_graph_homework_bfs_key.tex: %_key.tex : undirected_graph_homework.dot
	../alg_to_tex.py -l 3 -s -r .25 -d "Homework, undirected graph" -a bfs -v 'a' $< $*_ > $@
	
undirected_graph_homework_dfs_key.tex: undirected_graph_homework.dot
	../alg_to_tex.py -l 3 -s -r .23 -d "Homework, undirected graph" -a dfs  $< $*_ > $@

directed_graph_homework_bfs_key.tex: %_key.tex : directed_graph_homework.dot
	../alg_to_tex.py -l 3 -s -r .25 -d "Homework, directed graph" -a bfs -v 'a' $< $*_ > $@

directed_graph_homework_dfs_key.tex: %_key.tex : directed_graph_homework.dot
	../alg_to_tex.py -l 3 -s -r .25 -d "Homework, directed graph" -a dfs  $< $*_ > $@


pert_chart_key.tex: %_key.tex : pert_chart_graph.dot
	../alg_to_tex.py -l 3 -s -d "PERT chart analysis, classroom example" -a dag-longest-path -v s $< $*_ > $@

clean:
	rm -f $(pdfs) *.tex
