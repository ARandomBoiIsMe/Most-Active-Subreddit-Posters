import prawcore
from datetime import datetime, timedelta, date
import re
from utilities import config_util, reddit_util, database_util

connection = database_util.connect_to_db()

def main():
    config = config_util.load_config()
    reddit = reddit_util.initialize_reddit(config)

    subreddit_name = config['VARS']['SUBREDDIT']
    subreddit = validate_subreddit(reddit, subreddit_name)
    if not subreddit_name:
        print(f"This subreddit does not exist: r/{subreddit_name}.")
        exit()

    if not subreddit.user_is_moderator:
        print(f"You must be a mod in this sub: r/{subreddit_name}")
        exit()

    clear_flairs_from_previous_holders(subreddit)

    delete_outdated_flairs(subreddit)

    posts_from_previous_week = get_posts_from_previous_week(subreddit)

    author_post_count = generate_author_post_count(posts_from_previous_week)

    create_new_flairs(subreddit)

    set_flairs(subreddit, author_post_count)

    print("It is done.")

    database_util.close_connection(connection)

def validate_subreddit(reddit, subreddit_name):
    if subreddit_name.strip() == '' or subreddit_name is None:
        return None
    
    try:
        return reddit.subreddits.search_by_name(subreddit_name, exact=True)[0]
    except prawcore.exceptions.NotFound:
        return None

def clear_flairs_from_previous_holders(subreddit):
    user_list = []

    for flair in subreddit.flair(limit=None):
        if "Poster for Week" in flair['flair_text']:
            user_list.append(flair['user'])

    subreddit.flair.update(user_list)

def delete_outdated_flairs(subreddit):
    old_flairs = database_util.retrieve_flairs(connection)

    for flair in old_flairs:
        try:
            subreddit.flair.templates.delete(flair[2])
        except prawcore.exceptions.NotFound:
            continue

    database_util.delete_all_flairs(connection)

def get_posts_from_previous_week(subreddit):
    print("Getting posts from past week...")

    posts = subreddit.new()

    time_range = timedelta(weeks=1)
    filtered_posts = []
    for post in posts:
        post_creation_date = datetime.fromtimestamp(post.created_utc)
        if (post_creation_date > (datetime.today() - time_range)):
            filtered_posts.append(post)
        else:
            break
    
    return filter_out_flaired_posters(filtered_posts)

def filter_out_flaired_posters(posts):
    filtered_posts = []

    # Filters out posts whose posters already have flairs
    for post in posts:
        if post.author_flair_text == '' or post.author_flair_text is None:
            filtered_posts.append(post)

    return filtered_posts

def generate_author_post_count(posts):
    print("Sorting users based on post count...")
    
    author_post_count = {}

    for post in posts:
        if post.author is None:
            continue

        if post.author in author_post_count:
            author_post_count[post.author] += 1
        else:
            author_post_count[post.author] = 1
    
    # Sort author post counts from highest to lowest
    return sorted(author_post_count.items(), key=lambda x: x[1], reverse=True)

def create_new_flairs(subreddit):
    print("Creating new flairs...")

    # Creates five new flairs that can only be assigned by moderators
    for i in range(1, 6):
        text = f'#{i} Poster for Week {date.today()}'
        text = re.sub("\..*$", "", text)
        
        subreddit.flair.templates.add(
            text=text,
            allowable_content='text',
            mod_only=True,
            text_editable=False
        )
    
    # Saves created flairs in database
    for flair in subreddit.flair.templates:
        if "Poster for Week" in flair['text']:
            database_util.insert_flair(connection, flair)

def set_flairs(subreddit, post_authors):
    print("Setting flairs...")

    flairs = database_util.retrieve_flairs(connection)
    i = 0
    for author in post_authors:
        if i > 5:
            break

        subreddit.flair.set(
            author[0],
            text=flairs[i][1],
            flair_template_id=flairs[i][2]
        )

        i += 1

main()