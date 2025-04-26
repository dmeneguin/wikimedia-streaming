import json
from requests_sse import EventSource
from validation import validate_data
import pymongo

mongo_client = pymongo.MongoClient('mongodb://root:password@mongo:27017/')
url = 'https://stream.wikimedia.org/v2/stream/recentchange'
with EventSource(url) as stream:
    for event in stream:
        if event.type == 'message':
            try:
                change = json.loads(event.data)
            except ValueError:
                pass
            else:
                # discard canary events
                if change['meta']['domain'] == 'canary':
                    continue            

                validation = validate_data(change)
                mongo_client.db.events.insert_one({'payload': change, 'valid': validation['result']})

