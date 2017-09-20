from .setup_mongo_connection import get_songs_collection

mongo = get_songs_collection()

'''
Get the cursor for all artists from the database

Each document in the response is of format:
    {
    _id: artistName,
    songs: [{
            song: songName, 
            album: albumName,
            numListens: totalNumberOfListensToThisSong
        },...],
    numListens: totalNumberOfListensToTheArtist
    }

The documents are sorted in increasing lexicographic order
i.e. artist "ZZZ" comes before artist "aaa"
'''
def get_all_artists():
    cur = mongo.aggregate([
        {"$group": {
            "_id": {
                "artist": "$artist",
                "album": "$album",
                "song": "$name"
                },
            "numListens": {"$sum":1},
            }},
        {"$group": {
            "_id": "$_id.artist",
            "songs": {"$push": {
                "song": "$_id.song",
                "album": "$_id.album",
                "numListens": "$numListens"
                }},
            "totalNumListens": {"$sum": "$numListens"}
            }},
        {"$sort": {
            "_id":1
            }}
        ])
    return cur
