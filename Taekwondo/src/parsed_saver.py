
import pickle
import os

def save_parsed_results(output_tag, results_object, actions_object):
    
    output_directory = f"data/raw_parsed/{output_tag}"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    print(f"Saving results in: {output_directory}")

    results_pickle = f"{output_directory}/data_results.pkl"
    with open(results_pickle, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(results_object, output, pickle.HIGHEST_PROTOCOL)
    
    actions_pickle = f"{output_directory}/data_actions.pkl"
    with open(actions_pickle, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(actions_object, output, pickle.HIGHEST_PROTOCOL)