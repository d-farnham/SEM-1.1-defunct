# -*- coding: utf-8 -*-

"""

Save_Basic_Results.py

save basic results for the simple energy model
    
"""

# -----------------------------------------------------------------------------


import os
import numpy as np
import csv
import datetime
import contextlib
import pickle



#%%
def pickle_raw_results( global_dic, case_dic, result_dic ):
    
    output_path = global_dic['OUTPUT_PATH']
    global_name = global_dic['GLOBAL_NAME']
    case_name = case_dic['CASE_NAME']
    
    output_folder = output_path + '/' + global_name
    
    output_file_name = global_name + '_' + case_name + '.pickle'
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    with open(output_folder + "/" + output_file_name, 'wb') as db:
        pickle.dump([global_dic,case_dic,result_dic], db, protocol=pickle.HIGHEST_PROTOCOL)

#%%
def read_pickle_raw_results( global_dic, case_dic ):
    
    output_path = global_dic['OUTPUT_PATH']
    global_name = global_dic['GLOBAL_NAME']
    case_name = case_dic['CASE_NAME']
    
    output_folder = output_path + '/' + global_name
    
    output_file_name = global_name + '_' + case_name + '.pickle'
    
    with open(output_folder + "/" + output_file_name, 'rb') as db:
        [global_dic,case_dic,result_dic] = pickle.load( db )
    
    return result_dic

#%%
def pickle_raw_results_list( global_dic, case_dic_list, result_dic_list ):
    
    output_path = global_dic['OUTPUT_PATH']
    global_name = global_dic['GLOBAL_NAME']
    output_folder = output_path + '/' + global_name
    output_file_name = global_name + '.pickle'
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    with open(output_folder + "/" + output_file_name, 'wb') as db:
        pickle.dump([global_dic,case_dic_list,result_dic_list], db, protocol=pickle.HIGHEST_PROTOCOL)

#%%
def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

#%%
# save results by case
def save_list_of_vector_results_as_csv( global_dic, case_dic_list, result_dic_list ):
    
    for idx in range(len(result_dic_list)):
        
        case_dic = case_dic_list[idx]
        result_dic = result_dic_list[idx]
        save_vector_results_as_csv( global_dic, case_dic, result_dic )
        

#%%
# save results by case
def save_vector_results_as_csv( global_dic, case_dic, result_dic ):
    
    output_path = global_dic['OUTPUT_PATH']
    global_name = global_dic['GLOBAL_NAME']
    output_folder = output_path + '/' + global_name

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
             
    if len(case_dic['WIND_SERIES']) == 0:
        case_dic['WIND_SERIES'] = ( 0.*np.array(case_dic['DEMAND_SERIES'])).tolist()
    if len(case_dic['SOLAR_SERIES']) == 0:
        case_dic['SOLAR_SERIES'] = ( 0.*np.array(case_dic['DEMAND_SERIES'])).tolist()
    
    header_list = []
    series_list = []
    
    header_list += ['Time (hr)']
    series_list.append( np.arange(len(case_dic['DEMAND_SERIES'])))
    
    header_list += ['demand (kW)']
    series_list.append( case_dic['DEMAND_SERIES'] )
    
    header_list += ['solar capacity factor (kW)']
    series_list.append( np.array(case_dic['SOLAR_SERIES']))    
    
    header_list += ['wind capacity factor (kW per unit deployed)']
    series_list.append( np.array(case_dic['WIND_SERIES']))

    header_list += ['dispatch_solar (kW per unit deployed)']
    series_list.append( result_dic['DISPATCH_SOLAR'].flatten() ) 
    
    header_list += ['dispatch wind (kW)']
    series_list.append( result_dic['DISPATCH_WIND'].flatten() )
    
    header_list += ['dispatch_natgas (kW)']
    series_list.append( result_dic['DISPATCH_NATGAS'].flatten() )
    
    header_list += ['dispatch_nuclear (kW)']
    series_list.append( result_dic['DISPATCH_NUCLEAR'].flatten() )
    
    header_list += ['dispatch_to_storage (kW)']
    series_list.append( result_dic['DISPATCH_TO_STORAGE'].flatten() )
    
    header_list += ['dispatch_from_storage (kW)']
    series_list.append( result_dic['DISPATCH_FROM_STORAGE'].flatten() )  # THere is no FROM in dispatch results

    header_list += ['energy storage (kWh)']
    series_list.append( result_dic['ENERGY_STORAGE'].flatten() )
  
    header_list += ['dispatch_to_pgp_storage (kW)']
    series_list.append( result_dic['DISPATCH_TO_PGP_STORAGE'].flatten() )
    
    header_list += ['dispatch_pgp_storage (kW)']
    series_list.append( result_dic['DISPATCH_FROM_PGP_STORAGE'].flatten() )

    header_list += ['energy pgp storage (kWh)']
    series_list.append( result_dic['ENERGY_PGP_STORAGE'].flatten() )
    
    header_list += ['dispatch_unmet_demand (kW)']
    series_list.append( result_dic['DISPATCH_UNMET_DEMAND'].flatten() )
    
    header_list += ['cutailment_solar (kW)']
    series_list.append( result_dic['CURTAILMENT_SOLAR'].flatten() )
    
    header_list += ['cutailment_wind (kW)']
    series_list.append( result_dic['CURTAILMENT_WIND'].flatten() )
    
    header_list += ['cutailment_nuclear (kW)']
    series_list.append( result_dic['CURTAILMENT_NUCLEAR'].flatten() )
    
    header_list += ['price ($/kWh)']
    series_list.append( result_dic['PRICE'].flatten() )
     
    output_file_name = global_dic['GLOBAL_NAME']+'_'+case_dic['CASE_NAME']
    
    with contextlib.closing(open(output_folder + "/" + output_file_name + '.csv', 'w',newline='')) as output_file:
        writer = csv.writer(output_file)
        writer.writerow(header_list)
        writer.writerows((np.asarray(series_list)).transpose())
        output_file.close()
        
#%%
# save scalar results for all cases
def save_basic_results( global_dic, case_dic_list ):
    
    verbose = global_dic['VERBOSE']
        
    scalar_names = [
            'case name',
            'fixed_cost_natgas ($/kW/h)',
            'fixed_cost_solar ($/kW/h)',
            'fixed_cost_wind ($/kW/h)',
            'fixed_cost_nuclear ($/kW/h)',
            'fixed_cost_storage (($/h)/kWh)',
            'fixed_cost_pgp_storage (($/h)/kWh)',
            
            'var_cost_natgas ($/kWh)',
            'var_cost_solar ($/kWh)',
            'var_cost_wind ($/kWh)',
            'var_cost_nuclear ($/kWh)',
            'var_cost_to_storage ($/kWh)',
            'var_cost_storage ($/kWh)',
            'var_cost_to_pgp_storage ($/kWh)',
            'var_cost_pgp_storage ($/kWh)',
            'var_cost_unmet_demand ($/kWh)',
            
            'storage_charging_efficiency',
            'storage_charging_time (h)',
            'storage_decay_rate (1/h)',
            'pgp_storage_charging_efficiency',
            'pgp_storage_decay_rate (1/h)',
            
            'mean demand (kW)',
            'capacity factor wind series (kW)',
            'capacity factor solar series (kW)',
            
            'capacity_natgas (kW)',
            'capacity_solar (kW)',
            'capacity_wind (kW)',
            'capacity_nuclear (kW)',
            'capacity_storage (kWh)',
            'capacity_pgp_storage (kWh)',
            'capacity_to_pgp_storage (kW)',
            'capacity_from_pgp_storage (kW)',
            'system_cost ($/kW/h)', # assuming demand normalized to 1 kW
            'problem_status',
            
            'dispatch_natgas (kW)',
            'dispatch_solar (kW)',
            'dispatch_wind (kW)',
            'dispatch_nuclear (kW)',
            'dispatch_to_storage (kW)',
            'dispatch_from_storage (kW)',
            'energy_storage (kWh)',
            'dispatch_to_pgp_storage (kW)',
            'dispatch_pgp_storage (kW)',
            'energy_pgp_storage (kWh)',
            'dispatch_unmet_demand (kW)'
            
            'curtailment_solar (kW)',
            'curtailment_wind (kW)',
            'curtailment_nuclear (kW)'
            ]

    scalar_table = []
    for idx in range(len(case_dic_list)):
        case_dic = case_dic_list[idx]
        result_dic = read_pickle_raw_results(global_dic, case_dic)
        
        scalar_table.append(
            [       case_dic['CASE_NAME'],
             
                    # assumptions
                    
                    case_dic['FIXED_COST_NATGAS'],
                    case_dic['FIXED_COST_SOLAR'],
                    case_dic['FIXED_COST_WIND'],
                    case_dic['FIXED_COST_NUCLEAR'],
                    case_dic['FIXED_COST_STORAGE'],
                    case_dic['FIXED_COST_PGP_STORAGE'],
                    
                    case_dic['VAR_COST_NATGAS'],
                    case_dic['VAR_COST_SOLAR'],
                    case_dic['VAR_COST_WIND'],
                    case_dic['VAR_COST_NUCLEAR'],
                    case_dic['VAR_COST_TO_STORAGE'],
                    case_dic['VAR_COST_FROM_STORAGE'],
                    case_dic['VAR_COST_TO_PGP_STORAGE'],
                    case_dic['VAR_COST_FROM_PGP_STORAGE'],
                    case_dic['VAR_COST_UNMET_DEMAND'],
                    
                    case_dic['STORAGE_CHARGING_EFFICIENCY'],
                    case_dic['STORAGE_CHARGING_TIME'],
                    case_dic['STORAGE_DECAY_RATE'],
                    case_dic['PGP_STORAGE_CHARGING_EFFICIENCY'],
                    case_dic['PGP_STORAGE_DECAY_RATE'],
                    
                    # mean of time series assumptions
                    np.average(case_dic['DEMAND_SERIES']),
                    np.average(case_dic['WIND_SERIES']),
                    np.average(case_dic['SOLAR_SERIES']),
                                    
                    # scalar results
                    
                    result_dic['CAPACITY_NATGAS'],
                    result_dic['CAPACITY_SOLAR'],
                    result_dic['CAPACITY_WIND'],
                    result_dic['CAPACITY_NUCLEAR'],
                    result_dic['CAPACITY_STORAGE'],
                    result_dic['CAPACITY_PGP_STORAGE'],
                    result_dic['CAPACITY_TO_PGP_STORAGE'],
                    result_dic['CAPACITY_FROM_PGP_STORAGE'],
                    result_dic['SYSTEM_COST'],
                    result_dic['PROBLEM_STATUS'],
                    
                    # mean of time series results                
                                
                    np.average(result_dic['DISPATCH_NATGAS']),
                    np.average(result_dic['DISPATCH_SOLAR']),
                    np.average(result_dic['DISPATCH_WIND']),
                    np.average(result_dic['DISPATCH_NUCLEAR']),
                    np.average(result_dic['DISPATCH_TO_STORAGE']),
                    np.average(result_dic['DISPATCH_FROM_STORAGE']),
                    np.average(result_dic['ENERGY_STORAGE']),
                    np.average(result_dic['DISPATCH_TO_PGP_STORAGE']),
                    np.average(result_dic['DISPATCH_FROM_PGP_STORAGE']),
                    np.average(result_dic['ENERGY_PGP_STORAGE']),
                    np.average(result_dic['DISPATCH_UNMET_DEMAND']),
                    
                    np.average(result_dic['CURTAILMENT_SOLAR']),
                    np.average(result_dic['CURTAILMENT_WIND']),
                    np.average(result_dic['CURTAILMENT_NUCLEAR'])
                    
                    
             ]
            )
            
    output_path = global_dic['OUTPUT_PATH']
    global_name = global_dic['GLOBAL_NAME']
    output_folder = output_path + "/" + global_name
    today = datetime.datetime.now()
    todayString = str(today.year) + str(today.month).zfill(2) + str(today.day).zfill(2) + '_' + \
        str(today.hour).zfill(2) + str(today.minute).zfill(2) + str(today.second).zfill(2)
    
    output_file_name = global_name + '_' + todayString
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
	with contextlib.closing(open(output_folder + "/" + output_file_name + '.csv', 'w',newline='')) as output_file:
        writer = csv.writer(output_file)
        writer.writerow(scalar_names)
        writer.writerows(scalar_table)
        output_file.close()
        
    if verbose: 
        print ( 'file written: ' + output_file_name + '.csv')
    
    return scalar_names,scalar_table
    
def out_csv(output_folder,output_file_name,names,table,verbose):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    with contextlib.closing(open(output_folder + "/" + output_file_name + '.csv', 'w',newline='')) as output_file:
        writer = csv.writer(output_file)
        writer.writerow(names)
        writer.writerows(table)
        output_file.close()
        
    if verbose: 
        print ( 'file written: ' + output_file_name + '.csv')
    


    
