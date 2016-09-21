#-------------------------------------------
#import libraries

import pandas as pd
import random


#-------------------------------------------
#main function

def k_means(df,n_clusters=8,n_iter=10):
    all_results = []
    load_in(df)
    get_groups(df)
    while len(all_results) < n_iter:
        iter_results = perform_k_means(df,n_clusters)
        all_results.append(iter_results)
        for group in Group.groups:
            Group.lower_flag(group)
    best_result = min(all_results, key=lambda x:x['inertia'])
    output = {'best_result': best_result, 'all_results': all_results}
    return output


#-------------------------------------------
#top level functions

#function for performing one iteration of k-means
def perform_k_means(df,n_clusters):
    group_clusters = get_seed(df)
    group_clusters = add_clusters(group_clusters, n_clusters, df)
    while len([x for x in Group.groups if x.in_cluster==False]) > 0:
        add_closest_group_to_cluster(group_clusters)
    group_cluster_names = [x.group_list for x in group_clusters]
    total_inertia = sum([group_cluster.inertia for group_cluster in group_clusters])
    clusters_and_inertia = {'groupings': group_cluster_names, 'inertia': total_inertia}
    return clusters_and_inertia

#load in, rename source dataframe as df
def load_in (df):
    df = df
    return df

#get groups
def get_groups (df):
    for c in df.columns:
        Group(c,df)
        
#get seed
def get_seed (df):
    group_clusters = []
    seed_number = random.randint(1,len(df.columns))
    seed = Group.groups[seed_number]
    seed_cluster = GroupCluster(seed,df)
    group_clusters.append(seed_cluster)
    return group_clusters

#method to add k additional clusters by finding group furthest
#from existing cluster groups
def add_clusters (clusters, n_clusters, df):
    while len(clusters) < n_clusters:
        new_cluster = get_furthest_from_clusters(clusters, df)
        clusters.append(new_cluster)
    return clusters

#helper method for add_clusters function
#for computation of furthest distance and assignment of a new cluster
def get_furthest_from_clusters (clusters, df):
    distances = []
    for jj in Group.groups:
        total_distance = 0
        for cluster in clusters:
            total_distance = total_distance + Group.get_distance_between_addresses(cluster,jj)
        sum_pair_distances = {'group': jj, 'name': jj.name, 'distance': total_distance}
        distances.append(sum_pair_distances)
    maxDistanceItem = max(distances, key=lambda x:x['distance'])
    maxDistanceGroup = maxDistanceItem['group']
    new_cluster = GroupCluster(maxDistanceGroup, df)
    return new_cluster

#function to add the closest group to a cluster to that cluster
#also finds new closest groups to other clusters
def add_closest_group_to_cluster (clusters):
    target_cluster = get_cluster_with_closest_unassigned_group(clusters)
    Group.raise_flag(target_cluster.closest_group['group'])
    GroupCluster.add_group_to_cluster(target_cluster,target_cluster.closest_group['group'])
    for cluster in clusters:
        GroupCluster.get_distances_from_group_addresses(cluster,Group.groups)

#helper method for add_closest_group_to_cluster
#finds cluster with closest unassigned group
def get_cluster_with_closest_unassigned_group (clusters):
    cluster_with_closest_unassigned_group = min(clusters, key=lambda x:x.closest_group['distance'])
    return cluster_with_closest_unassigned_group
    
    
#-------------------------------------------
#class for each group
    
class Group():
    
    groups = []
    group_names = []
    
    def __init__(self, name, df: pd.DataFrame()):
        self.name = name
        self.df = df
        self.in_cluster = False
        Group.groups.append(self)
        Group.group_names.append(self.name)
        self.create_group_df()
        
    #create df for all albums in group
    def create_group_df(self):
        self.group_df = self.df[self.df[self.name]==1]
        self.find_group_address()
        return self.group_df
    
    #calculate address/centroid
    def find_group_address(self):
        self.group_address = pd.DataFrame.mean(self.group_df,axis=0).values
        return self.group_address
        
    # helper method to get euclidean distance between groups
    def get_distance_between_addresses (group1, group2):
        p_minus_q = group1.group_address - group2.group_address
        p_minus_q_squared = p_minus_q**2
        squared_distance = p_minus_q_squared.sum()
        distance_between_addresses = squared_distance**.5
        return distance_between_addresses
    
    #mark group as in a cluster
    def raise_flag(group):
        group.in_cluster = True
        
    #reset flag
    def lower_flag(group):
        group.in_cluster = False


#-------------------------------------------
#class for each cluster of groups
   
class GroupCluster(Group):
        
    def __init__(self, group, df: pd.DataFrame()):
        self.groups = [group]
        self.df = df
        self.distance_from_group_addresses = []
        self.inertia = 0
        group.in_cluster = True
        self.get_group_list()
        self.create_group_df()
        self.get_distances_from_group_addresses(Group.groups)        

    #Inherited methods:
    #find_group_address -> params: self, returns group address 
    #get_distance_betweeen_addresses -> params: 2 groups, returns euclidean distance between groups

    #create df for all albums in at least one group in cluster
    #overloaded method, different method needed for evaluation

    def get_group_list(self):
        self.group_list = [x.name for x in self.groups]

    def create_group_df(self):
        self.group_df = self.df[self.df[self.group_list].sum(axis=1)>=1]
        self.find_group_address()
        return self.group_df, self.group_list, self.groups

    #create df for all albums in at least one group in cluster
    def add_group_to_cluster (self, other_group):
        self.group_list.append(other_group.name)
        self.groups.append(other_group)
        self.create_group_df()

    #get distances from cluster centroids to group centroids
    def get_distances_from_group_addresses (self, all_groups):
        for group in all_groups:
            distance = self.get_distance_between_addresses(group)
            group_info = {'group': group, 'name': group.name, 'distance': distance}            
            self.distance_from_group_addresses.append(group_info)
        self.calculate_inertia()
        #if any unassigned groups, call find_closest_unassigned_group method
        if len([x for x in Group.groups if x.in_cluster==False]) > 0:
            self.find_closest_unassigned_group()
    
    #find group not already in a cluster with closest centroid
    def find_closest_unassigned_group (self):
        unassigned_groups = [x for x in self.distance_from_group_addresses if x['group'].in_cluster==False]
        self.closest_group = min(unassigned_groups, key=lambda x:x['distance'])
    
    #calculate inertia for one cluster
    def calculate_inertia (self):
        self.inertia = sum([self.get_distance_between_addresses(group) for group in self.groups])