This is the code package for the article

Antti Hyttinen, Frederick Eberhardt, Matti J??rvisalo:
"Constraint-Based Causal Discovery: Conflict Resolution with Answer Set Programming"

published in Uncertainty in Artificial Intelligence 2014, Quebec City, QC, Canada.

1. Fetching Clingo:
----------------
This code package does not include the clingo ASP-solver. Clingo is available
for mac,linux and windows:

Fetch it from address

http://sourceforge.net/projects/potassco/files/clingo/4.3.0/

and replace the empty file "ASP/clingo430" with the file.

We use clingo 4.3.0 mac version. The code has only been tested on mac, it has also worked in Linux. The R code
calls clingo automatically.

2. Loading the code:
-----------------
Start R in the "R/" directory and load the code with the following commands:
> source('load.R')
> loud()

In case you want to run also algorithms not presented as new in the paper run:
> source('load.R')
> loud(TRUE)


Make sure you have packages 'deal','pcalg','combinat','graph','hash' and 'bnlearn' installed. The code was originally produced using Rstudio and R version 3.0.2 (2013-09-25).

3. Running simple tests:
---------------------

>test(1)
>test(2)
>test(3)
>test(4)

4. Producing similar figures as in the paper:
-----------------------------------
First run the algorithms to produce the data in the directories.
> plot1(run=TRUE)
Then produce the plot.
> plot1()
Similarly for plot1....,plot7. See the R-files for more information.

NOTE: Due to so many changes in the PCALG package new version w.r.t. the version that was the newest at the time of publication, the algorithms calling it (PC,FCI versions) are no longer run.
NOTE: You can call e.g. "plot1(howmany=3)" to get a curve over 3 datasets.

5. Important points:
-----------------------------------------------------

-If you fail or interrupt a run some of the files that the program writes constraints into may remain open for writing and some output meant for the screen will be writer to those files. Then next run fails. Typing "sink()" a couple of times will remove this.

-In principle the code should handle experimental overlapping data sets, all of
the theory surely allows for it. However this code package has not been excessively
tested in this scenario. Also the scalability may suffer at least from the use of several data sets.

-The code basically outputs only one graph which maximizes/minimizes the objective
function. To get an idea what features are actually determined one should run HHEJ 2013 algorithm with the single graph of this paper as an input. There might be a possibility to build the same functionality over clingo, but it is not sure whether it would match the efficiency of the HHEJ 2013 paper method. For
restricted setting one might run for example FCI on the d-sep oracle with our output to produce a PAG.
Yet another option would be to print out all solutions from Clingo (see instructions of Clingo) and
see the common properties there.

-If you get warnings from Clingo about the "intervene" predicate, you should ignore them. They only point out that the data didn't have any variables intervened on. Similar warnings may appear about missing "indep" or "dep" predicates, this prints out if the data did not have any (in)dependencies. Since we are drawing an ROC-type curve, for extreme parameter values warnings like this are likely.

-When calling plots you can set the howmany parameter to a lower value to get a faster run. For example "plot1(run=TRUE,howmany=10);plot1(run=FALSE;howmany=10)" will produce a plot over 10 datasets only, instead of the assumed 200. Note that the curves are not smooth for these quicker runs.

-Score-based BN learning is implemented as a search over orders, this is not very fast, although it produces the optimal results in terms of accuracy. The new version of PCALG contains "simy" which could be used instead (this is not implemented).

Input/output definitions:
------------------------- 

G    binary matrix of directed edges, G[i,j] = 1 means j->i is present (note the similarity to B matrix, this is where the indexing order comes from)

Ge    symmetric binary matrix of bidirected edges

Gs    symmetric binary matrix of undirected edges (not used in the basic version)

B       matrix of coefficients of the data generating model x= Bx +e, nonzero elements correspond to G
Ce    Symmetric pos. definite matrix of cov(e) in the above model, nonzero elements correspond to Ge

Cx    Is the sample covariance matrix of the generated data. This matrix is used in the independence tests.

e      A vector indication which variables were intervened on e[1]=1 means intervention on the first variable

The Gs above for M define the true model structure, for L they mean the learned structure.


6. Disclaimer on the ASP encodings:
-----------------------------------

For ease of reading the UAI paper presented the encoding with sets
 V (variables in the d-connection graph), C (conditioned vars) and J (intervened
 vars).  The code which was done earlier considers
  C ( conditioned vars), J (intervened variables) and M (marginalized variables). 
The notations are equivalent, V of the paper notation is the set of original variables
minus C and M. 

In addition the d-connection graphs permitted self-cycles between variables. As only undirected self loops x???-x may affect d-connection properties of the graph, only these are considered in the code. For example a path y->x<->x<-z implies the existence of a path y->x<-z, which is d-connecting for exactly the same conditioning sets, so x<->x can always be ignored.

6. Questions
------------
Please try to figure out yourself especially if the problem is in installing or getting the code running. Otherwise email:

Antti Hyttinen <ajhyttin@gmail.com>

7. Versions
-----------

Version 6, end of 2016:
-All runs calling PCALG are now not run. This includes FCI and PC algorithms. Due to major changes in PCALGs code, the modifications to the versions used in the original runs are no longer valid. The code is still in
"mods/" directory, one can use these with the old version of PCALG (most recent version at the time of the publication). Setting "others<<-TRUE" will run these, but the current PCALG version produces errors.
-Also other minor fixes implemented. Added the flag for running non-paper algorithms.

