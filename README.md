<h1> Group Reduce</h1>
<p>Group Reduce is a k-means clustering algorithm for reducing the number of groups in a data set. It takes in pandas dataframes with solely categorical data in 0/1 form, and outputs lists of groups close to one another based on based on k-means clustering.</p>

<p>Group Reduce is designed for data sets where instances have multiple group membership (where many rows have more than one cell with a value of 1).</p>

<p>Basic steps in Group Reduce algorithm:</p>
<ol>
<li>Designate seed randomly</li>
<li>Find groups with centroids furthest from seed (and each other)</li>
<li>Create a dataframe for each seed, with rows where df[seed]==1</li>
<li>Iteratively find group with centroid closest to a cluster and integrate it into the cluster by creating a dataframe where df[seed]==1 or df[groups_already_integrated_into_cluster]==1 or df[integrated_group]==1</li>
</ol>

<p>Function: k_means (df, n_clusters (optional, default = 8), n_iter (optional, default = 10))</p>

<h5>Parameters:</h5>
<ul>
<li><strong>df</strong>: dataframe used in analysis</li>
<li><strong>n_clusters</strong>: number of clusters returned</li>
<li><strong>df</strong>: number of iterations of k-means performed</li>
</ul>

<h5>Returned Values</h5>
<p>The k-means function returns one variable, a dictionary with two keys, 'best_result' and 'all_results'. The 'best_result' key holds the groupings created with the iteration of the clustering algorithm that had lowest centroid movement and the associated centroid movement (inertia). The 'all_result' key holds a list of [groupings,inertia] created through the algorithm.</p>

<p>Library dependencies: Pandas, Random</p>
