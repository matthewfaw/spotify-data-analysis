from setup_mongo_connection import get_songs_collection

mongo = get_songs_collection()

def get_all_artists():
    cur = mongo.aggregate([
        {"$group": {
            "_id": "$artist",
            "count": {"$sum":1}
            }},
        {"$sort": {
            "_id":1
            }}
        ])
    return cur
