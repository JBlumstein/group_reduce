<h1> Group Reduce</h1>
<p>Group Reduce is a k-means clustering algorithm for reducing the number of groups in a data set (i.e., for clustering groups). It takes in pandas dataframes with solely categorical data in 0/1 form, and outputs lists of groups close to one another based on based on k-means clustering.</p>

<p>Group Reduce is designed for data sets where instances have multiple group membership (where many rows have more than one cell with a value of 1).</p>

<p>This repo includes the algorithm, a sample dataset, and a sample notebook.</p>

<h4>Why I decided to build this:</h4>
<p>Most k-means clustering algorithms, like the one provided by scikitlearn, simply find the midpoint between n centroids in a cluster. When clustering individual instances, this method makes perfect senes. But there are two problems with this method when trying to cluster <i>groups</i>: 1) groups can have different populations, and 2) groups can have overlapping membership. Group Reduce mitigates these issues by doing the following.</p>
<ol>
<li>In order to deal with some groups have greater population than others, Group Reduce weights the averaging used in finding a cluster's centroid by the population of each group.</li>
<li>In order to deal with groups with overlapping membership, when groups are combined into one cluster, the combined data set preserves an instance with membership in multiple groups in the cluster as having a count of one, instead of counting it n times (once for each group in the cluster it's a member of).</li>
</ol>

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
<p>The k-means function returns one variable, a dictionary with two keys, 'best_result' and 'all_results'. The 'best_result' key holds the groupings created with the iteration of the clustering algorithm that had lowest centroid movement and the associated centroid movement (inertia). The 'all_result' key holds a list of [groupings,inertia] created through the algorithm.</p>

<h4>Library dependencies:</h4>
<p>Pandas, Random</p>
