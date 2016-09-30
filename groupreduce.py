#-------------------------------------------
#import libraries

import pandas as pd
import random

#-------------------------------------------
#main function

def k_means(df, n_clusters=8, n_iter=10):
    '''main function'''
    all_results = []
    load_in(df)
    get_groups(df)
    n_iter = min(n_iter,len(Group.groups))
    while len(all_results) < n_iter:
        iter_results = perform_k_means(df,n_clusters)
        all_results.append(iter_results)
        for group in Group.groups:
            Group.lower_flag(group)
    best_result = min(all_results, key=lambda x:x['inertia'])
    output = {'best_result': best_result, 'all_results': all_results}
    return output

#-------------------------------------------
#other functions not associated with a class

def perform_k_means(df, n_clusters):
    '''function for performing one iteration of k-means'''
    group_clusters = create_first_cluster(df)
    group_clusters = add_clusters(group_clusters, n_clusters, df)
    while len([x for x in Group.groups if x.in_cluster==False]) > 0:
        add_closest_group_to_cluster(group_clusters,df)
    group_cluster_names = [x.group_list for x in group_clusters]
    total_inertia = sum([group_cluster.inertia for group_cluster in group_clusters])
    clusters_and_inertia = {'groupings': group_cluster_names, 'inertia': total_inertia}
    return clusters_and_inertia

def load_in(df):
    '''load in, rename source dataframe as df'''
    df = df
    return df

def get_groups(df):
    '''get groups'''
    for c in df.columns:
        Group(c,df)
        
def create_first_cluster(df):
    '''get first cluster
    first cluster should be a group that has not been first cluster in
    prior iterations    
    '''
    group_clusters = []
    seed = get_seed(df)
    Group.now_has_been_seed(seed)
    seed_cluster = GroupCluster(seed,df)
    group_clusters.append(seed_cluster)
    return group_clusters

def get_seed(df):
    '''get a seed group to be first cluster for one iteration
    works by picking a seed number, checking if group has been seed:
    - if group hasn't been seed, set that group as seed for iteration
    - if group has been seed, use recursion to return to top of function
    '''
    seed_number = random.randint(0, len(df.columns)-1)
    if Group.groups[seed_number].has_been_seed == False:
        seed = Group.groups[seed_number]
        return seed
    else:
        return get_seed(df)

def add_clusters(clusters, n_clusters, df):
    '''function to add k additional clusters by finding group furthest
    from existing cluster groups'''
    while len(clusters) < n_clusters:
        new_cluster = get_furthest_from_clusters(clusters, df)
        clusters.append(new_cluster)
    return clusters

def get_furthest_from_clusters(clusters, df):
    '''helper function for add_clusters function
    for computation of furthest distance and assignment of a new cluster'''
    distances = []
    for jj in Group.groups:
        total_distance = 0
        for cluster in clusters:
            total_distance = total_distance + Group.get_distance_between_addresses(cluster, jj)
        sum_pair_distances = {'group': jj, 'name': jj.name, 'distance': total_distance}
        distances.append(sum_pair_distances)
    maxDistanceItem = max(distances, key=lambda x:x['distance'])
    maxDistanceGroup = maxDistanceItem['group']
    new_cluster = GroupCluster(maxDistanceGroup, df)
    return new_cluster

def add_closest_group_to_cluster(clusters, df):
    '''function to add the closest group to a cluster to that cluster,
    also finds new closest groups to other clusters'''
    target_cluster = get_cluster_with_closest_unassigned_group(clusters)
    GroupCluster.add_group_to_cluster(target_cluster, target_cluster.closest_group['group'], df)
    for cluster in clusters:
        GroupCluster.get_distances_from_group_addresses(cluster, Group.groups)

def get_cluster_with_closest_unassigned_group(clusters):
    '''helper function for add_closest_group_to_cluster function
    finds cluster with closest unassigned group'''
    cluster_with_closest_unassigned_group = min(clusters, key=lambda x:x.closest_group['distance'])
    return cluster_with_closest_unassigned_group
       
#-------------------------------------------
#class for each group
    
class Group():
    '''class for each group'''
    
    groups = []
    group_names = []
    
    def __init__(self, name, df: pd.DataFrame()):
        '''init method'''
        self.name = name
        self.in_cluster = False
        self.has_been_seed = False
        Group.groups.append(self)
        Group.group_names.append(self.name)
        self.create_group_df(df)
        
    def create_group_df(self, df):
        '''create df for all albums in group'''
        self.group_df = df[df[self.name]==1]
        self.find_group_address()
    
    def find_group_address(self):
        '''calculate address/centroid'''
        self.group_address = pd.DataFrame.mean(self.group_df,axis=0).values
        
    def get_distance_between_addresses(group1, group2):
        '''helper method to get euclidean distance between groups'''
        p_minus_q = group1.group_address - group2.group_address
        p_minus_q_squared = p_minus_q**2
        squared_distance = p_minus_q_squared.sum()
        distance_between_addresses = squared_distance**.5
        return distance_between_addresses
    
    def raise_flag(group):
        '''mark group as in a cluster'''
        group.in_cluster = True
        
    def lower_flag(group):
        '''reset flag'''
        group.in_cluster = False
    
    def now_has_been_seed(group):
        '''mark that a group has been seed'''
        group.has_been_seed = True

#-------------------------------------------
#class for each cluster of groups
   
class GroupCluster(Group):
    '''class for each cluster of groups
    Inherited methods that are used:
    1) find_group_address -> params: self, returns group address 
    2) get_distance_betweeen_addresses -> params: 2 groups, returns euclidean distance between groups
    '''
        
    def __init__(self, group, df: pd.DataFrame()):
        '''init method'''
        self.groups = [group]
        self.distance_from_group_addresses = []
        self.inertia = 0
        Group.raise_flag(group)
        self.create_group_list()        
        self.create_group_df(df)
        self.get_distances_from_group_addresses(Group.groups)        

    def create_group_list(self):
        '''assign self.group_list as the names from each group in cluster'''
        self.group_list = [x.name for x in self.groups]

    def create_group_df(self, df):
        '''create df for all albums in at least one group in cluster
        overloaded method, in Group takes string, here takes list
        evaluation approach changes to reflect input'''
        self.group_df = df[df[self.group_list].sum(axis=1)>=1]
        self.find_group_address()

    def add_group_to_cluster(self, group, df):
        '''create df for all albums in at least one group in cluster'''
        self.groups.append(group)        
        self.group_list.append(group.name)
        Group.raise_flag(group)
        self.create_group_df(df)

    def get_distances_from_group_addresses(self, all_groups):
        '''get distances from cluster centroids to group centroids'''
        for group in all_groups:
            distance = self.get_distance_between_addresses(group)
            group_info = {'group': group, 'name': group.name, 'distance': distance}            
            self.distance_from_group_addresses.append(group_info)
        self.calculate_inertia()
        #if any unassigned groups, call find_closest_unassigned_group method
        if len([x for x in Group.groups if x.in_cluster==False]) > 0:
            self.find_closest_unassigned_group()

    def find_closest_unassigned_group(self):
        '''find group not already in a cluster with closest centroid'''
        unassigned_groups = [x for x in self.distance_from_group_addresses if x['group'].in_cluster==False]
        self.closest_group = min(unassigned_groups, key=lambda x:x['distance'])
    
    def calculate_inertia(self):
        '''calculate inertia for one cluster'''
        self.inertia = sum([self.get_distance_between_addresses(group) for group in self.groups])