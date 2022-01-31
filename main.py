import logging.config
import configparser
import argparse
import datetime
from twitter import Twitter
from user_cache import UserCache
from tweet_writer import write_timeline

CONFIG_FILE = 'config.ini'
LOGGING_CONFIG = 'logging.ini'

# Configure logging
logging.config.fileConfig(LOGGING_CONFIG)


def parse_command_line():
    parser = argparse.ArgumentParser(description='Twitter information gathering tool')
    parser.add_argument('username', type=str,
                        help='Get information for a particular user')
    parser.add_argument('--start-date', type=str,
                        help='Start date to retrieve tweets DD/MM/YYYY')
    parser.add_argument('--end-date', type=str,
                        help='End date to retrieve tweets DD/MM/YYYY')
    parser.add_argument('--num-pages', type=str,
                        help='Number of tweet pages to retrieve')
    return parser.parse_args()


def get_iso_time(date):
    date_time = datetime.datetime.strptime(date, '%d/%m/%Y')
    return date_time.isoformat(timespec='milliseconds') + 'Z'


def main():
    """
    Twitter training program entry point
    """
    args = parse_command_line()

    # Read application configuration file
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    twitter = Twitter(config['TWITTER']['API_URL'],
                      config['TWITTER']['BEARER_TOKEN'],
                      config['TWITTER']['APP_NAME'])
    screen_name = args.username
    cache = UserCache('user-cache.txt')
    user_id = cache.find_user(screen_name)
    if user_id is None:
        user_id = twitter.get_user_id(screen_name)
        cache.write_user(screen_name, user_id)
        logging.info(f'Found ID {user_id} for user {screen_name} from API')
    else:
        logging.info(f'Found ID {user_id} for user {screen_name} from cache')

    time_range = None
    if args.start_date is not None and args.end_date is not None:
        time_range = (get_iso_time(args.start_date), get_iso_time(args.end_date))
        print(time_range)
        timeline = twitter.get_timeline(user_id, time_range=time_range)
    else:
        timeline = twitter.get_timeline(user_id)

    write_timeline(timeline, screen_name)
    oldest_id = None
    if args.num_pages is not None:
        for i in range(int(args.num_pages) - 1):
            if int(timeline['meta']['result_count']) == 0:
                if oldest_id is not None:
                    timeline = twitter.get_timeline(user_id, time_range=time_range, max_id=oldest_id)
                    if int(timeline['meta']['result_count']) == 0:
                        break
            else:
                oldest_id = timeline['meta']['oldest_id']
                timeline = twitter.get_timeline(user_id, page_id=timeline['meta']['next_token'])
                write_timeline(timeline, screen_name)


if __name__ == '__main__':
    main()
