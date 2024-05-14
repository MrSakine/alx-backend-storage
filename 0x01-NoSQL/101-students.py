#!/usr/bin/env python3
""" Top students """


def top_students(mongo_collection):
    """returns all students sorted by average score"""
    pipeline = [
        {
            "$project": {
                "_id": 1,
                "name": 1,
                "topics": 1,
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        { "$sort": { "averageScore": -1 } }
    ]
    return mongo_collection.aggregate(pipeline)
