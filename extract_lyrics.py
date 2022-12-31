from bs4 import BeautifulSoup
import requests
import re
import time
import pandas as pd
from functions import re_transform, list_re_transform, similar, remove_duplicates
import pickle


# create a list with all three artist pages on lyrics.com
artists = ['dope lemon', 'blind lemon jefferson', 'lemon jelly']

artist_urls = ['https://www.lyrics.com/artist/dope-lemon/3192281',
           'https://www.lyrics.com/artist/Blind-Lemon-Jefferson/390',
           'https://www.lyrics.com/artist/Lemon-Jelly/402804']

documents = {}

# extract lyrics for artists
for a in range(len(artists)):
    # check response for artist website
    response = requests.get(url=artist_urls[a])
    print(artist_urls[a] + ' - response: ' + str(response))

    # get html file and convert to bs object
    html_file = requests.get(artist_urls[a], 'html.parser').text
    lyrics_soup = BeautifulSoup(html_file, features="lxml")

    # get list of all song links for artist
    lyric_links = []
    for links in lyrics_soup.find_all(class_ = 'tal qx'):
        for subtag in links:
            full_link = 'https://www.lyrics.com' + subtag.a['href']
            lyric_links.append(full_link)

    print('exctracted ' + str(len(lyric_links)) + ' links for ' + artists[a])
    
    # filter out duplicates
    lyric_links = drop_duplicate_titles(lyric_links)
    print('found ' + str(len(lyric_links)) + ' unique links for ' + artists[a])
    
    # get lyrics for all song links
    # pretend to be a Browser to avoid being flagged.
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}
    lyrics = []
    titles = []
    for i in lyric_links:
        lyric_page_html = BeautifulSoup(requests.get(i,
                                                 'html.parser',
                                                 headers=headers).text,
                                                            features="lxml")
        lyrics_div = lyric_page_html.find(id='lyric-body-text')
        if lyrics_div is not None:
            print('saving lyrics for ' + i)
            lyrics_text = lyric_page_html.find(class_='lyric-body').text
            title_text = lyric_page_html.find(class_='lyric-title').text
            lyrics.append(lyrics_text)
            titles.append(title_text)
        else:
            print('could not find lyrics for ' + i)
        time.sleep(3)
    
    # make a data frame for the artist
    documents[artists[a]] = pd.DataFrame({'title': titles, 'document': lyrics})

# remove duplicates
documents = remove_duplicates(documents)

# save documents
with open('documents.pickle', 'wb') as handle:
    pickle.dump(documents, handle, protocol=pickle.HIGHEST_PROTOCOL)