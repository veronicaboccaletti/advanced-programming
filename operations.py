import pandas as pd 
from decorator import *

#Getting the some basic information about the dataset. The basic information are the name and data type of each column
@decorator 
def get_basic_info(df):
    column_names = df.columns.tolist()
    data_types = df.dtypes.tolist()
    basic_info = {"column_names": column_names, "data_types": data_types}
    return pd.DataFrame.from_dict(basic_info)

#Obtaining the list of unique sequence IDs available in the dataset
@decorator
def get_unique_seqids(df):
    return df['seq_id'].unique().tolist()

#Obtaining the list of unique type of operations available in the dataset
@decorator
def get_unique_operations(df):
    unique_operations = df["type"].unique()
    return list(unique_operations)

#Counting the number of features provided by the same source
@decorator
def count_features_by_source(df):
    source_count = df.groupby('source').size()
    source_count.name = 'count'
    return source_count

#Counting the number of entries for each type of operation
@decorator
def count_entries_by_type(df):
    type_counts = df.groupby('type').size()
    return type_counts

#Deriving a new dataset containing only the information about entire chromosomes. Entries with entire chromosomes comes from source GRCh38
@decorator
def entire_chromosome(df):
    new_dataframe= df.loc[df['source']=="GRCh38"]
    return new_dataframe.loc[df['type']== 'chromosome']

#Calculating the fraction of unassembled sequences from source GRCh38. Hint: unassembled sequences are of type supercontig while the others are of chromosome
@decorator
def fraction_unassembled(df):
    num_supercontig = df[(df['type']=='supercontig') & (df['source']=='GRCh38')].shape[0]
    num_chromosome = df[(df['type']=='chromosome') & (df['source']=='GRCh38')].shape[0]
    return num_supercontig/(num_supercontig+num_chromosome)

#Obtaining a new dataset containing only entries from source ensembl , havana and ensembl_havana
@decorator
def get_selected_sources(df):
    sources = ['ensembl', 'havana', 'ensembl_havana']
    return df[df['source'].isin(sources)]

#Counting the number of entries for each type of operation for the dataset containing containing only entries from source ensembl , havana and ensembl_havana
@decorator
def count_selected_operations(df):
    df_selected = get_selected_sources(df)
    return df_selected.groupby(['type'])['seq_id'].count()

#Returning the gene names from the dataset containing containing only entries from source ensembl , havana and ensembl_havana
@decorator
def get_gene_names(df):
    df_selected = get_selected_sources(df)
    return df_selected[df_selected['type']=='gene']['attributes'].str.extract(r'Name=([^;]*)')[0]