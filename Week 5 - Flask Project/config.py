import os

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY')

    REGISTERED_USERS = {
        'pika@poke.com': {
            'name': 'Ash',
            'password': 'ichooseyou'
        },
        'starmie@poke.com': {
            'name': 'Misty',
            'password': 'water123'
        },
        'onyx@poke.com': {
            'name': 'Brock',
            'password': 'rockonbb'
        }
    }