#general modules
import copy, random

#modules for data science
import pandas as pd
import numpy as np

print 'All modules finished importing'

if __name__ == "__main__":
    file_path = "C:\\Users\\devin\\Downloads\\first_names_data.csv"
    df = pd.read_csv(file_path, ',')

    # print first 10 records
    print df.head(10)

    # number of records
    num_records = len(df)
    print "There are " + str(num_records) + " records in the dataframe."

    # Male/Female value counts
    print df['gender'].value_counts()

    # Get top 100 counts for male and female names then
    #  randomly select 10 names from the 100 names.
    num_samples = 100
    num_elements = 3
    random.seed = '1234'
    random_idx = np.array( random.sample(range(num_samples), num_samples) )

    # extract top 100 male names
    df_male = df[(df.gender == 'M')].head(num_samples)
    # sort by first name
    temp_df = df_male[random_idx < num_elements].sort('first_name')
    # extract only first names and defined as "group_male"
    group_male = list(temp_df.first_name.values)
    del temp_df, df_male

    # do the same things for females
    df_female = df[(df.gender == 'F')].head(num_samples)
    temp_df = df_female[random_idx < num_elements].sort('first_name')
    group_female = list(temp_df.first_name.values)

    print "MALES: ", group_male
    print "FEMALES: ", group_female

    # define preference dictionary for males
    male_prefers_ref = {}
    for name in group_male:
        # created list from randomly selected names in female list
        temp_list = random.sample(group_female, len(group_female))

        # update dictionary with preference list for name
        male_prefers_ref.update({name:temp_list})

    # repeat for females
    female_prefers_ref = {}
    for name in group_female:
        temp_list = random.sample(group_male, len(group_male))
        female_prefers_ref.update({name: temp_list})

    print pd.DataFrame(male_prefers_ref.items()).sort(0)
    print " "
    print pd.DataFrame(female_prefers_ref.items()).sort(0)

    partner_free = group_male[:]
    matching ={}

    # copy reference dictionaries
    male_prefers = copy.deepcopy(male_prefers_ref)
    female_prefers = copy.deepcopy(female_prefers_ref)

    # while there are still unmatched partners keep looping
    while partner_free:
        # grab and remove first element from partner_free
        target_elem = partner_free.pop(0)
        # grab preference list associated by name
        target_list = male_prefers[target_elem]
        # pick possible partner from preference list
        possible_pair_partner = target_list.pop(0)
        # check for matching
        paired_elem = matching.get(possible_pair_partner)
        # if no matching exist create it
        if not paired_elem:
            matching[possible_pair_partner] = target_elem
        else:
            # possible partners preferences
            partner_list = female_prefers_ref[possible_pair_partner]
            # check rank on current and possible match
            # take the higher rank of the two
            # append unpaired element back into partner_free list
            rank_paired_elem = partner_list.index(paired_elem)
            rank_target_elem = partner_list.index(target_elem)

            if rank_paired_elem > rank_target_elem:
                matching[possible_pair_partner] = target_elem
                partner_free.append(paired_elem)
            else:
                partner_free.append(target_elem)
    matching_df = pd.DataFrame(matching.items()).sort(0)
    matching_df.columns = ['females', 'males']

    print matching_df