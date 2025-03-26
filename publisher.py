import json
from requests_sse import EventSource

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
                print('{user} edited {title}'.format(**change))