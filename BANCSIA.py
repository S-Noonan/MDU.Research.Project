# BANCSIA - Bacterial Naming for Correct Species Identification & Allocation 
# created by: Susan Noonan
# Python script to determine species groups for ECC Masters research project
# This script can be used to determine species groups based on genetic relatedness and a set threshold distance

# Input = the output from running ska dist (.tsv) file (https://github.com/simonrharris/SKA)
# Input = threshold distance relevant to your analysis (eg. 0.02 for subspecies, 0.04 for species)
# Output = .csv file with isolate name and group number

!pip install pandas
import pandas as pd

##### Functions 
# Extract samples within a set distance
def extract_groups(df, sample_of_interest, max_distance):
    filtered_df = df[(df['S1'] == sample_of_interest) & (df['dist'] <= max_dist) | (df['S2'] == sample_of_interest) & (df['dist'] <= max_dist)]
    samples_within_dist1 = list(set(filtered_df['S1'])) 
    samples_within_dist2 = list(set(filtered_df['S2'])) 
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
    unique_sample_names = pd.unique(df[['S1', 'S2']].values.ravel('K'))
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
    return result_samples

# Create a dataframe from the dictionary created with each isolates allocated a species group number
def df_with_spec(dict):
    # create empty dataframe
    empty_df = pd.DataFrame(columns = ["isolate", "spec_no"])
    for i, entry in enumerate(dict):
        for j in dict[entry]:
            empty_df.loc[len(empty_df)] = [j, i+1] 
    return empty_df

###### run python species grouping analysis on output from the ska results dataframe from R

# read file
file_path = '/path_to_file/ska_output.csv'
# Turn CSV file into a DataFrame
df = pd.read_csv(file_path)
# set max_dist
max_dist = 0.04
# run function to get species groups
grouping = species_groups(df)
# turn output into dataframe where each isolate has a grouping number
df_output = df_with_spec(grouping)
# save this file as csv and use for further analysis in R
df_output.to_csv('/path_to_file/allocation_result.csv', index=True)
        
# Manually check your results to determine which species names are appropriate or complete further analysis using group number
