def active():
	d = {
		'get_basic_info': True,
		'seqID' : True,
		'type_operation' : True,
		'count_features' : True,
		'count_entries' : True,
		'entire_chromosome' : True,
		'count_supercontigs' : True,
		'entries_ens_hav_enshav' : False,
		'count_entries_ens_hav_enshav' : True,
		'gene_names' : True
        }
	return d  
		

def decorator(function):
	act = active()
	def wrapper(*arg, **kwargs):
		name = function.__name__
		if act.get(name,False):
			return function(*arg, **kwargs)
		else: 
			return f'The operation {name} is not active'
	return wrapper