from flask import Flask, render_template, request
from dataset import *
import operations
from decorator import *

app = Flask(__name__)

#function to extract data from filepath
def get_df():
	d = GFF3Dataset('dataset.zip')
	return d.dataframe
# df1 = get_df() is a step to get async the data from Dataset. We can pass df1 to every operation with no need to retrive data every time.

#now we need to build a list of active operation starting form a list of available operations
#build list of available operations
av_operations = {
    'get_basic_info': 'Info: some basic information about the dataset',
    'get_unique_seqids': 'Sequence ID: list of unique sequence IDs available in the dataset',
    'get_unique_operations': 'Type operation: list of unique type of operations available in the dataset',
    'count_features_by_source': 'Count features: number of features provided by the same source',
    'count_entries_by_type': 'Count entries: number of entries for each type of operation',
    'entire_chromosome': 'Get entire chromosomes: new dataset containing only the information about entire chromosomes coming from source GRCh38',
    'fraction_unassembled': 'Count supercontigs: fraction of unassembled sequences from source GRCh38',
    'get_selected_sources': 'Entries from sources ensembl, havana, and ensembl_havana',
    'count_selected_operations': 'Count entries from ensembl, havana, and ensembl_havana: number of entries for each type of operation for the dataset containing only entries from source ensembl, havana and ensembl_havana',
    'get_gene_names': 'Gene names: gene names from the dataset containing containing only entries from source ensembl, havana and ensembl_havana'
    }
#initialize list of active operations and descriptions
active_operations= {}
active_operations_descr= {}
#get list of active operations from decorator.py
active_list= active()
for operation_name in av_operations:
     #check if operation is active
     if active_list.get(operation_name, False):
        #take the functions from operations.py
        active_operations[operation_name]= getattr(operations, operation_name)
        #take description from av_operations
        active_operations_descr[operation_name]= av_operations.get(operation_name, 'Description missing')

# WebApp rendering: flask "@app" decorator to render the right template.html for the right path with contextual params

# 1)Homepage: we pass only the base homepage.html
@app.route("/")
def homepage():
    return render_template("homepage.html")

# 2)Active operations view: we pass the list of active operation names and related descriptions to fill the html dynamically;
#   A form take the operation name as input and redirect the HTTP Post Request to "/execute_operation" path in a new view;
@app.route("/active_operations")
def active_operations_view():
    return render_template("active_operations.html", active_operations=active_operations, operation_descr=active_operations_descr)

# 3)Execute operation and display result
@app.route("/execute_operation", methods=['POST'])
def execute_operation():
    # we take in input the HTTP Post Request with the request.form attribute [select_operation] with the value of the selected operation 
    operation_selected= request.form['select_operation']
    # check if the operation is active (just a check, in /active_operations we pass only active_operations)
    if operation_selected in active_operations:
         # We call the right operation passing our live extraction from datasetas input (). If we pass df1 = get_df(), we save time during execution. 
         # The result is trasfer to operation_result.html for printing result table
         operation_result = active_operations[operation_selected](get_df())
         return render_template("operation_result.html", operation_name=active_operations_descr[operation_selected], operation_result=operation_result)
    else:
         return 'The operation is not active'
#note: all results returned from operations are Pandas' Dataframe, because "operation_result.html" is designed to dynamically build a table of result around dataframe in input.

# Project document view
@app.route("/project_document")
def project_document():
    return render_template("project_document.html")

# About the website view
@app.route("/about")
def about():
    return render_template("about.html")

#debugging option
if __name__ == "__main__":
    app.run(debug=True)