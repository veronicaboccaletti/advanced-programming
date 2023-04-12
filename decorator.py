#import wraps for readability of active_operations
from functools import wraps

#list of operations name with related "Active" information.
def active():
	d = {
		'get_basic_info': True,
		'get_unique_seqids' : True,
		'get_unique_operations' : True,
		'count_features_by_source' : True,
		'count_entries_by_type' : True,
		'entire_chromosome' : True,
		'fraction_unassembled' : True,
		'get_selected_sources' : True, #Attention: function related to other functions.
		'count_selected_operations' : True,
		'get_gene_names' : True
        }
	return d  
		
#decorator for every operation that return function with args if the function is active.
def decorator(function):
	#wraps for maintain function name and other parameter as input function
	@wraps(function)
	def wrapper(*arg, **kwargs):
		act = active()
		name = function.__name__
		if act.get(name, False):
			return function(*arg, **kwargs)
		else: 
			return f"The operation {name} is not active"
	return wrapper