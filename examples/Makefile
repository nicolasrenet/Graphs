  



pdfs = bfs_undirected_classroom.pdf bfs_undirected_classroom_key.pdf bfs_directed_classroom.pdf bfs_directed_classroom_key.pdf clrs_example_bfs.pdf clrs_example_bfs_key.pdf clrs_example_dfs.pdf clrs_example_dfs_key.pdf dfs_directed_classroom.pdf dfs_directed_classroom_key.pdf dfs_undirected_classroom.pdf dfs_undirected_classroom_key.pdf dijkstra_gross_yellen.pdf dijkstra_gross_yellen_key.pdf dag_shortest_path.pdf dag_shortest_path_key.pdf


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
	../alg_to_tex.py -b -l 5 -s -d "Classroom example, directed graph" -a dag-shortest-path -v 's' $< $*_ > $@

dag_shortest_path_key.tex: %_key.tex : weighted_dag.dot
	../alg_to_tex.py -l 5 -s -d "Classroom example, directed graph" -a dag-shortest-path -v s $< $*_ > $@ 


clean:
	rm -f $(pdfs) *.tex
