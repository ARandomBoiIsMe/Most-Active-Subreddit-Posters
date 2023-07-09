import praw

def initialize_reddit(config):
    client_id = config['REDDIT']['CLIENT_ID']
    client_secret = config['REDDIT']['CLIENT_SECRET']
    password = config['REDDIT']['PASSWORD']
    username = config['REDDIT']['USERNAME_REDDIT']

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        password=password,
        username=username,
        user_agent='Top Posters Script v2.0 by ARandomBoiIsMe'
    )

    return reddit