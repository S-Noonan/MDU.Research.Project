# Download this script and save to your directory
# To run this script using the command line, run the following code:
# /path_to_file/BANCSIA_v2.py /path/to/input_file.tsv 0.04 (alter if you want a lower threshold)
# where input_file.tsv is the file created after running ska distance
# the output file will save in the current directory

import pandas as pd
import sys

if len(sys.argv) != 3:
    print("Usage: python species_grouping.py <input_file.tsv> <max_distance>")
    sys.exit(1)

input_file = sys.argv[1]
max_dist = float(sys.argv[2])

##### Functions 
# Extract samples within a set distance
def extract_groups(df, sample_of_interest, max_distance):
     filtered_df = df[(df['Sample 1'] == sample_of_interest) & (df['Mash-like distance'] <= max_dist) | (df['Sample 2'] == sample_of_interest) & (df['Mash-like distance'] <= max_dist)]
     samples_within_dist1 = list(set(filtered_df['Sample 1'])) 
     samples_within_dist2 = list(set(filtered_df['Sample 2'])) 
     samples_with_dist = list(set(samples_within_dist1 + samples_within_dist2))
     if len(samples_with_dist) == 0:
         samples_with_dist = [sample_of_interest]
     return samples_with_dist

# Check if two lists overlap
def check_overlap(list1, list2):
    # Convert the lists to sets and check if their intersection is non-empty
    return bool(set(list1) & set(list2)) 

# Find new items to add from two overlapping lists
def list_diff(list1, list2):
    # Convert lists to sets and get all the unique items
    diff = sorted(list(set(list1 + list2)))
    return diff

# Check dictionary to see if list already exists, if not add new key
def check_dict(dict, list):
    for key in dict.keys():
         if check_overlap(list, dict[key]) == True:
             return key
         else:
             continue
    return False
    # if there are no matches, add a new item to the dict

# Allocate each item in input data to a species group and output results
def species_groups(df):
    # Dictionary to store results
    result_samples = {}
    unique_sample_names = pd.unique(df[['Sample 1', 'Sample 2']].values.ravel('K'))
    i = 1
    for sample in unique_sample_names:
        group = sorted(extract_groups(df, sample, max_dist))
        # check dictionary
        if len(result_samples) == 0:
            # there are no items in dict, so add list of samples
            result_samples[i] = group
            i+=1
        else:
            if len(group) ==0:
                result_samples[i] = sample 
                # if there are no other isolates that are within the threshold, add the sample you checked
                i+=1
            elif check_dict(result_samples, group) == False:
                # there were no values that overlap, so add new item to dict
                result_samples[i] = group
                i+=1
            else:
                index = check_dict(result_samples, group)
                new = list_diff(group, result_samples[index])
                result_samples[index] = new
                i+=1
    print("You analysed ", len(unique_sample_names), " isolates.")
    print("At a threshold of ", max_dist, "there are ", len(result_samples), " groups.")
    return result_samples

# Check if any samples appear in more than one group and print the ones that do.
def unique_grps(dataframe):
    # Group by 'entry' and filter out entries that appear more than once
    duplicate_entries = dataframe.groupby('isolate').filter(lambda x: len(x) > 1)
    if len(duplicate_entries) == 0:
        print("Each isolate is in a unique group.")
    else:
        print("The following isolates are allocated to multiple groups: ")
        # Iterate through the duplicate entries and print them along with their group keys
        for entry in duplicate_entries['isolate'].unique():
            groups = duplicate_entries[duplicate_entries['isolate'] == entry]['group_no'].tolist()
            print(entry, "is in groups ",groups)
        #print(f"Isolate: {isolate}, Groups: {group_no}")
    return
    
# Create a dataframe from the dictionary created with each isolates allocated a species group number
def df_with_spec(dict):
    # create empty dataframe
    empty_df = pd.DataFrame(columns = ["isolate", "spec_no"])
    for i, entry in enumerate(dict):
        for j in dict[entry]:
            empty_df.loc[len(empty_df)] = [j, i+1] 
    return empty_df

###### run python species grouping analysis on output from the ska results dataframe from R

###### Main Program

# Turn CSV file into a DataFrame
df = pd.read_csv(input_file, sep='\t')

# run function to get species groups
grouping = species_groups(df)

# Check for isolates in multiple groups
check_df = pd.DataFrame([(key, value) for key, values in grouping.items() for value in values], columns=['group_no', 'isolate'])
unique_grps(check_df)

# Save output to a new DataFrame and CSV
df_output = df_with_spec(grouping)
output_file = "Species_Grouping_result.csv"
df_output.to_csv(output_file, index=False)
print(f"Results saved to {output_file}")
