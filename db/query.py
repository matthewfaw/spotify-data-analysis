from .setup_mongo_connection import get_songs_collection

mongo = get_songs_collection()

def get_intervals(n):
    firstDoc = mongo.find().sort({"timestamp":1}).limit(1).next()
    lastDoc = mongo.find().sort({"timestamp":-1}).limit(1).next()

    beginning = float(firstDoc['timestamp'])
    end = float(lastDoc['timestamp'])

'''
Get the cursor for all artists from the database

Each document in the response is of format:
    {
    _id: artistName,
    infoOnDay: [{
            "date": dateTheSongsWereListenedTo,
            songs: [{
                song: songName, 
                album: albumName,
                numListensOnDay: totalNumberOfListensToThisSongOnDay
            },...],
            totalNumListens: totalNumberOfListensToArtistOnDay
        },...]
    },...],
    numListens: totalNumberOfListensToTheArtistOnAllDays
    }

The documents are sorted in increasing lexicographic order
i.e. artist "ZZZ" comes before artist "aaa"
'''
def get_all_artists():
    cur = mongo.aggregate([
        # Extract details on play time
        {"$addFields": {
            "day": {"$substr": ["$playback_date",0,2]},
            "month": {"$substr": ["$playback_date",3,3]},
            "year": {"$substr": ["$playback_date", 7, 4]},
            "hour": {"$substr": ["$playback_date", 13, 2]},
            "minute": {"$substr": ["$playback_date", 16, 2]},
            "date": {"$substr": ["$playback_date",0,11]}
            }},
        # Get number of listens to a given song in a given time period
        {"$group": {
            "_id": {
                "artist": "$artist",
                "album": "$album",
                "song": "$name",
                "date": "$date",
                },
            "numListens": {"$sum":1},
            }},
        # Group these details for each artist over each time period
        {"$group": {
            "_id": {
                "artist": "$_id.artist",
                "date": "$_id.date",
                },
            "songs": {"$push": {
                "song": "$_id.song",
                "album": "$_id.album", "numListensOnDay": "$numListens", }},
            "totalNumListensOnDay": {"$sum": "$numListens"}
            }},
        # Collapse details for each artist
        {"$group": {
            "_id": "$_id.artist",
            "infoOnDay": {"$push": {
                "date": "$_id.date",
                "songs": "$songs",
                "totalNumListensOnDay": "$totalNumListensOnDay"
                }},
            "totalNumListens": {"$sum": "$totalNumListensOnDay"}
            }},
        {"$sort": {
            "_id":1
            }}
        ])
    return cur
