from sqlalchemy.ext.declarative import DeclarativeMeta
import json

# filter other sqlalchemy junk
# maybe there are better way to do filter this
user_model = ["email", 'password', 'id']


class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            
            #complex loop. Do try understand it but take your time.
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata' and x in user_model]:
                data = obj.__getattribute__(field)
                try:
                    # this will fail on non-encodable values, like other classes
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)
