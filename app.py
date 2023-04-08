from flask import Flask, render_template, request
from dataset import *
import operations
from decorator import *

app = Flask(__name__)

def get_df():
	d = GFF3Dataset('x.gff3')
	return d.dataframe

av_operations = {
	'get_basic_info': 'Get basic information',
    'get_unique_seqids': 'Get unique sequence IDs',
    'get_unique_operations': 'Get unique operations',
    'count_features_by_source': 'Count features by source',
    'count_entries_by_type': 'Count entries by type',
    'entire_chromosome': 'Entire chromosome',
    'fraction_unassembled': 'Fraction unassembled',
    'count_selected_operations': 'Count selected operations',
    'get_gene_names': 'Get gene names'
    }
active_operations= {}
for operation_name in av_operations:
     active_operations[operation_name]= operations.decorator(getattr(operations, operation_name))
# Homepage
@app.route("/")
def homepage():
    return render_template("homepage.html", av_operations=av_operations)

# Active operations view
@app.route("/active_operations")
def active_operations_view():
    return render_template("active_operations.html", active_operations=active_operations)

# Execute operation and display result
@app.route("/execute_operation/", methods=['POST'])
def execute_operation():
    operation_name= request.form['operation']
    if operation_name in active_operations:
         operation_result = active_operations[operation_name](dataset.df)
         return render_template("operation_result.html", operation_name=operation_name, operation_result=operation_result)
    else:
         return 'The operation is not active'

# Project document view
@app.route("/project_document")
def project_document():
    return render_template("project_document.html")

if __name__ == "__main__":
    app.run(debug=True)