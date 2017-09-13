from .setup_mongo_connection import get_songs_collection

mongo = get_songs_collection()

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
