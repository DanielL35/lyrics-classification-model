import pandas as pd
import re
from difflib import SequenceMatcher

def drop_duplicate_titles(link_list):
    """
    identify duplicate links and drop the rows from data frame
    """
    regex = r"\D+"  # identify all NON-DIGIT elements
    # create a list of links without the digits
    link_list_processed = [''.join(re.findall(regex, i)) for i in link_list]
    # put edited and original links in data frame
    df_temp = pd.DataFrame({'link_formatted': link_list_processed,
                            'link_original': link_list})
    # find all ducplicates
    indices = df_temp['link_formatted'].drop_duplicates().index
    # return list wihtout duplicates
    return list(df_temp.loc[indices]['link_original'])

def re_transform(txt):
    """
    prepare string for model    
    """
    txt = txt.lower()  # lower case everything
    # txt=txt.strip()  # remove spaces
    txt=re.sub("\n"," ",txt)  # remove new line characters
    txt=re.sub("\r"," ",txt)  # remove new line characters
    # txt=re.sub("(","",txt)  # remove new line characters
    # txt=re.sub(")","",txt)  # remove new line characters
    txt=re.sub("'","",txt)  # remove '
    return txt

def list_re_transform(lyrics_list):
    """
    create a list comprehension
    """
    return [re_transform(i) for i in lyrics_list]  # make list comprehension

def similar(a, b):
    """
    Check if to strings are similar.

    """
    return SequenceMatcher(None, a, b).ratio()

# !TODO the remove_duplicates is is quite resource-intense and should
# be changed in the future. The lyrics can also be checked by their titles.
def remove_duplicates(dict_artists):
    """
    This function removes duplicate songs from the dict.

    """
    # loop through all artists
    for key in dict_artists:
        # check how many songs per artist
        len_1 = len(dict_artists[key])
        indices_list = []
        # go through all songs
        for i in range(len(dict_artists[key])):
            # compare with all other songs (but only once!)
            for j in range(i+1, len(dict_artists[key])):
                # if they are very similar
                if similar(dict_artists[key]['document'][i],
                           dict_artists[key]['document'][j]) > 0.9:
                    # append their index to a list
                    indices_list.append(i)
        # drop all duplicates
        dict_artists[key] = dict_artists[key].drop(index=list(set(indices_list)))
        # check number of songs again
        len_2 = len(dict_artists[key])
        # and print a message
        print('removed ' + str(len_1-len_2) + ' duplicates from ' + str(key) + ' lyrics')
    return dict_artists

def make_corpus_labels(documents):

    corpus = []
    labels = []

    no_characters = []
    for key in documents:
        no_characters.append(sum([len(i) for i in documents[key]['document']]))
    min_no_characters = min(no_characters)

    for key in documents:
        total_string_length = 0
        for index, row in documents[key].iterrows():
            corpus.append(row['document'])
            labels.append(key)
            total_string_length = total_string_length + len(row['document'])
            # print(total_string_length)
            if total_string_length > min_no_characters:
                print('reached ' + str(total_string_length) + ' characters for ' + str(key))
                break

    return corpus, labels
