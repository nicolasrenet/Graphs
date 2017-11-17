  




pdf: bfs_undirected_classroom bfs_directed_classroom clrs_example_bfs clrs_example_dfs dfs_directed_classroom dfs_undirected_classroom

zip: $(pdf)
	zip -r graph_examples.zip  bfs_undirected_classroom.pdf  bfs_undirected_classroom_key.pdf bfs_directed_classroom.pdf bfs_directed_classroom_key.pdf clrs_example_bfs.pdf clrs_example_bfs_key.pdf clrs_example_dfs.pdf clrs_example_dfs_key.pdf dfs_directed_classroom.pdf dfs_directed_classroom_key.pdf dfs_undirected_classroom.pdf dfs_undirected_classroom_key.pdf

bfs_undirected_classroom: % : undirected_graph_classroom.dot
	rm  -f $@_[0-9]*
	../alg_to_tex.py -b -l 4 -s -d "Classroom example, undirected graph" -a bfs -v 'a' $< $@_ > $@.tex 
	pdflatex $@

	rm  -f $@_[0-9]*
	../alg_to_tex.py -l 4 -s -d "Classroom example, undirected graph" -a bfs -v 'a' $< $@_ > $@_key.tex 
	pdflatex $@_key


bfs_directed_classroom: % : directed_graph_classroom.dot
	rm  -f $@_[0-9]*
	../alg_to_tex.py -b -l 4 -s -d "Classroom example, directed graph" -a bfs -v 'a' $< $@_ > $@.tex 
	pdflatex $@

	rm  -f $@_[0-9]*
	../alg_to_tex.py -l 4 -s -d "Classroom example, directed graph" -a bfs -v 'a' $< $@_ > $@_key.tex 
	pdflatex $@_key

dfs_directed_classroom: % : directed_graph_classroom.dot
	rm  -f $@_[0-9]*
	../alg_to_tex.py -b -l 4 -s -d "Classroom example, directed graph" -a dfs $< $@_ > $@.tex 
	pdflatex $@

	rm  -f $@_[0-9]*
	../alg_to_tex.py -l 4 -s -d "Classroom example, directed graph" -a dfs $< $@_ > $@_key.tex 
	pdflatex $@_key

dfs_undirected_classroom: % : undirected_graph_classroom.dot
	rm  -f $@_[0-9]*
	../alg_to_tex.py -b -l 4 -s -d "Classroom example, undirected graph" -a dfs $< $@_ > $@.tex 
	pdflatex $@

	rm  -f $@_[0-9]*
	../alg_to_tex.py -l 4 -s -d "Classroom example, undirected graph" -a dfs $< $@_ > $@_key.tex 
	pdflatex $@_key

clrs_example_bfs: % : %.dot
	rm  -f $@_[0-9]*
	../alg_to_tex.py -b -l 4 -s -d "CLR3, Figure 22.3, p.~596, undirected graph" -a bfs -v 's' $@.dot $@_ > $@.tex 
	pdflatex $@

	rm  -f $@_[0-9]*
	../alg_to_tex.py -l 4 -s -d "CLR3, Figure 22.3, p.~596, undirected graph" -a bfs -v 's' $@.dot $@_ > $@_key.tex 
	pdflatex $@_key


	
clrs_example_dfs: % : %.dot
	rm  -f $@_[0-9]*
	../alg_to_tex.py -b -l 4 -s -d "CLR3, Figure 22.4, p.~605, directed graph" -a dfs $@.dot $@_ > $@.tex 
	pdflatex $@

	rm  -f $@_[0-9]*
	../alg_to_tex.py -l 4 -s -d "CLR3, Figure 22.4, p.~605, directed graph" -a dfs $@.dot $@_ > $@_key.tex 
	pdflatex $@_key


	
