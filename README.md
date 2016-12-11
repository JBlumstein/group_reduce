<h1> Group Reduce</h1>

<p>Check out the <a href="https://github.com/JBlumstein/group_reduce/blob/master/groupreduce.py">groupreduce.py python file</a> for the algorithm and the <a href="https://github.com/JBlumstein/group_reduce/blob/master/test_notebook.ipynb">jupyter notebook</a> for an example of the groupreduce algorithm in action.

<hr>

<p>Group Reduce is a k-means clustering algorithm for reducing the number of groups in a data set (i.e., for clustering groups). It takes in pandas dataframes categorical data in 0/1 form, and outputs lists of groups close to one another based on based on k-means clustering. Group Reduce is designed for data sets where instances have multiple group membership.</p>

<p>A naive k-means clustering algorithms, when adding to a cluster, simply finds the midpoint between the n points in the cluster (i.e., it finds the point in a space that is the smallest summed euclidean distance between the points). When clustering individual instances, this method makes perfect sense.</p>

<p>However, when trying to cluster groups, it must be taken into account that groups can have different size populations and that group memberships can overlap. As a result, instead of finding the minimum sum of unweighted euclidean distances from points represented by each group (one point per group), when clustering groups the search for a centroid can be done more effectively by finding the minimum sum of unweighted euclidean distances of the union of the populations of the groups in the cluster. This is exactly how Group Reduce works.</p>

<p>For example, let's say cluster D includes groups A, B, and C, and that group A includes the set of points (K, J, M), group B includes the set of points (M, N, P, Q, X, Y), and group C includes the set of points (X, Y, Z). Here Group Reduce will find the union of the groups' memberships--the set of points (K, J, M, N, P, Q, X, Y, Z)--and then the minimum sum of unweighted euclidean distances from this newly created set representing the members of the cluster.</p>

<p>While Group Reduce is by no means the most efficient or cleanly coded algorithm ever created, it works as advertised. I'm hoping in to continue working on Group Reduce to make it more flexible and resilient.</p>

<h4>Basic steps in Group Reduce algorithm:</h4>
<ol>
<li>Designate seed randomly</li>
<li>Find groups with centroids furthest from seed (and each other)</li>
<li>Create a dataframe for each seed, with rows where df[seed]==1</li>
<li>Iteratively find group with centroid closest to a cluster and integrate it into the cluster by creating a dataframe where df[seed]==1 or df[groups_already_integrated_into_cluster]==1 or df[integrated_group]==1</li>
</ol>

<h4>Function:</h4>
<p>k_means (df, n_clusters (optional, default = 8), n_iter (optional, default = 10))</p>

<h4>Parameters:</h4>
<ul>
<li><strong>df</strong>: dataframe used in analysis</li>
<li><strong>n_clusters</strong>: number of clusters returned</li>
<li><strong>n_iter</strong>: number of iterations of k-means performed</li>
</ul>

<h4>Returned Values:</h4>
<p>The k-means function returns one variable, a dictionary with two keys, 'best_result' and 'all_results'. The 'best_result' key holds a list of the groupings created with the iteration of the clustering algorithm that had lowest centroid movement and the associated centroid movement (inertia). The 'all_result' key holds a list of [groupings,inertia] created through the algorithm.</p>

<h4>Library dependencies:</h4>
<p>Pandas, Random</p>
