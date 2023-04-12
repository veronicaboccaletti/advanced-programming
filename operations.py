import pandas as pd 
from decorator import *

#Getting the some basic information about the dataset. The basic information are the name and data type of each column
@decorator
def get_basic_info(df):
	column_names = df.columns.tolist()
	data_types = df.dtypes.tolist()
	basic_info = {"columnNames": column_names, "dataTypes": data_types} 
	return pd.DataFrame.from_dict(basic_info)

#Obtaining the list of unique sequence IDs available in the dataset 
@decorator
def get_unique_seqids(df):
	seqid_info = {"seqId_Unique": df['seqid'].unique().tolist()}
	return pd.DataFrame.from_dict(seqid_info)

#Obtaining the list of unique type of operations available in the dataset 
@decorator
def get_unique_operations(df):
	unique_operations = {"typeOp_Unique": df['type'].unique().tolist()} 
	return pd.DataFrame.from_dict(unique_operations)
 
#Counting the number of features provided by the same source 
@decorator
def count_features_by_source(df):
	source_count = df.groupby('source').size()
	source_count_info = {'source': source_count.index.tolist(), 'size': source_count.values.tolist()}
	return pd.DataFrame.from_dict(source_count_info)

#Counting the number of entries for each type of operation 
@decorator
def count_entries_by_type(df):
	type_counts = df.groupby('type').size()
	type_counts_info = {'typeOp': type_counts.index.tolist(), 'size': type_counts.values.tolist()}
	return pd.DataFrame.from_dict(type_counts_info)

#Deriving a new dataset containing only the information about entire chromosomes. Entries with entire chromosomes comes from source GRCh38 
@decorator
def entire_chromosome(df):
	new_dataframe= df.loc[(df['source']=="GRCh38") & (df['type']== 'chromosome')] 
	return new_dataframe.reset_index(drop=False) #reset_index to update rowIndex from 0 to n and print in HTML

#Calculating the fraction of unassembled sequences from source GRCh38. Hint: unassembled sequences are of type supercontig while the others are of chromosome
@decorator
def fraction_unassembled(df):
	#number of rows superconting-GRCh38
	num_supercontig = df[(df['type']=='supercontig') &
(df['source']=='GRCh38')].shape[0]
	#number of rows chromosome-GRCh38
	num_chromosome = df[(df['type']=='chromosome') &
(df['source']=='GRCh38')].shape[0]
	#fraction of supercontig/tot
	fraction_info= {'fraction': [num_supercontig/(num_supercontig+num_chromosome)]}
	return pd.DataFrame.from_dict(fraction_info)

#Obtaining a new dataset containing only entries from source ensembl , havana and ensembl_havana
@decorator
def get_selected_sources(df):
	sources = ['ensembl', 'havana', 'ensembl_havana'] 
	return df[df['source'].isin(sources)].reset_index(drop=False) #reset_index to update rowIndex from 0 to n and print in HTML

#Counting the number of entries for each type of operation for the dataset containing only entries from source ensembl , havana and ensembl_havana
@decorator
def count_selected_operations(df):
	df_selected = get_selected_sources(df)
	size_each = df_selected.groupby('type').size()
	size_each_info = {'typeOp': size_each.index.tolist(), 'size': size_each.values.tolist()} 
	return pd.DataFrame.from_dict(size_each_info)

#Returning the gene names from the dataset containing containing only entries from source ensembl , havana and ensembl_havana
@decorator
def get_gene_names(df):
	df_selected = get_selected_sources(df)
	gene_names = df_selected[df_selected['type']=='gene']['attributes'].str.extract(r'Name=([^;]*)')[0] #[^;]* is a regex for exclude ';' from name
	gene_names_info = {'geneName' : gene_names.values.tolist()}
	return pd.DataFrame.from_dict(gene_names_info)