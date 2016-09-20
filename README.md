<h1> Group Reduce</h1>
<p>Group Reduce is a k-means clustering algorithm for reducing the number of groups in a data set. It takes in pandas dataframes with solely categorical data in 0/1 form, and outputs lists of groups close to one another based on based on k-means clustering.</p>

<p>Group Reduce is designed for data sets where instances have multiple group membership (where many rows have more than one cell with a value of 1).</p>

<p>Basic steps in Group Reduce algorithm:</p>
<ol>
<li>Designate seed</li>
<li>Find groups with centroids furthest from seed (and each other)</li>
<li>Create a dataframe for each seed, with rows where df[seed]==1</li>
<li>Iteratively find group with centroid closest to a cluster and integrate it into the cluster by creating a dataframe where df[seed]==1 or df[integrated_group]==1</li>
</ol>

<p>Library dependencies: Pandas, Random</p>
