import mongoengine

# MongoDB connection
mongoengine.connect(
    db='sondagesdb',
    host='localhost',
    port=27017
)
