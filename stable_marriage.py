#general modules
import copy, random

#modules for data science
import pandas as pd
import numpy as np

print 'All modules finished importing'


def checking_pairs(matching, pref_list_a, pref_list_b):
    conflict_dict = {}
    potential_conflict_dict = {}

    # inverse matching pairs
    matching_inverse = dict((elem2, elem1) for elem1, elem2 in matching.items())

    # loop over the matching
    for partner, target_elem in matching.items():
        warning = 0
        # grab partner pref list adn target index
        partner_list = pref_list_b[partner]
        partner_list_higher = partner_list[:partner_list.index(target_elem)]
        # loop over elements with higher priorities
        for elem in partner_list_higher:
            elem_paired_partner = matching_inverse[elem]
            elem_list = pref_list_a[elem]

            # resulting preference
            rank_current_paired_partner = elem_list.index(partner)
            rank_possible_paired_partner = elem_list.index(elem_paired_partner)

            if rank_possible_paired_partner > rank_current_paired_partner:
                warning += 1
                # warning detail
                temp_pair = '"' + partner + '"' + ' and ' + '"' + target_elem + '"'
                temp_1 = '"' + partner + '"' + ' puts higher priority on '
                temp_2 = '"' + elem + '"' + ' than ' + '"' + target_elem + '"'
                temp_issue_partner_side = temp_1 + temp_2
                del temp_1, temp_2

                break

        # get target's higher priority list
        target_list = pref_list_a[target_elem]
        target_list_higher = target_list[:target_list.index(partner)]
        #loop over higher priorities
        for elem in target_list_higher:
            # elems paired partner
            paired_partner_elem = matching[elem]
            elem_list = pref_list_b[elem]
            # resulting preference
            rank_current_paired_partner = elem_list.index(target_elem)
            rank_possible_paired_partner = elem_list.index(paired_partner_elem)
            if rank_possible_paired_partner > rank_current_paired_partner:
                warning += 1
                temp_pair = '"' + partner + '"' +  ' and ' + '"' + target_elem + '"'
                temp_1 = '"' + elem + '"' + ' than ' + '"' + partner + '"'
                temp_2 = '"' + elem + '"' + ' than ' + '"' + partner + '"'
                temp_issue_target_side = temp_1 + temp_2
                del temp_1, temp_2

                break
        if warning == 2:
            conflict_dict.update({temp_pair: [temp_issue_partner_side, temp_issue_target_side]})
        elif warning == 1:
            try:
                if not temp_issue_partner_side == 0:
                    potential_conflict_dict.update({temp_pair:temp_issue_partner_side})
                    del temp_issue_partner_side
                else:
                    potential_conflict_dict.update({temp_pair:temp_issue_target_side})
            except:
                pass
        # create dataframe from conflict dict
        if len(conflict_dict) == 0:
            conflict_df = []
        else:
            conflict_df = pd.DataFrame(conflict_dict.items()).sort(0)
            conflict_df.columns = ['pair', 'comment']

        if len(potential_conflict_dict) == 0:
            potential_conflict_df = []
        else:
            potential_conflict_df = pd.DataFrame(potential_conflict_dict.items()).sort(0)
            potential_conflict_df.columns = ['pair', 'comment']

        return conflict_df, potential_conflict_df


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
    num_elements = 10
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

    conflict, potential_conflict = checking_pairs(matching, male_prefers_ref, female_prefers_ref)
    if len(conflict) == 0:
        print "No conflict in the matching"
    else:
        for idx in range(len(conflict)):
            print 'Conflicted pair: ' + conflict.ix[idx]['pair']
            for comment in conflict.ix[idx]['comment']:
                print comment
            print " "

    if len(potential_conflict) == 0:
        print "No potential conflict in the matching"
    else:
        for idx in range(len(potential_conflict)):
            print 'Potential conflicted pair: ' + potential_conflict.ix[idx]['pair']
            print potential_conflict.ix[idx]['comment']
            print " "