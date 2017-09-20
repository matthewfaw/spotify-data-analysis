from db import query as q
from spotify import artists
from spotify import suggested_artists as sug
from spotify import genres
from serialize import save

related_artist_dict = {}
genre_dict = {}
listening_history_dict = {}
total_number_of_listens_dict = {}
for doc in q.get_all_artists():
    artist = doc['_id']
    print(artist)
    info = artists.get_artist_info(artist)
    if info != {}:
        artist_id = info['id']
        related_artist_dict[artist] = sug.get_related_artists(artist_id=artist_id)
        genre_dict[artist] = genres.get_genres(info=info)
        listening_history_dict[artist] = doc['infoOnDay']
        total_number_of_listens_dict[artist] = doc['totalNumListens']

save.save(related_artist_dict,'related_artists')
save.save(genre_dict,'genres')
save.save(listening_history_dict,'listening_history')
save.save(total_number_of_listens_dict,'total_number_of_listens')
