import csv
import logging


def write_timeline(timeline, screen_name):
    res_count = int(timeline['meta']['result_count'])
    if res_count == 0:
        return
    with open('tweet-data.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        num_tweets = len(timeline['data'])
        logging.info('Writing %i tweets for %s', num_tweets, screen_name)
        for tweet in timeline['data']:
            csv_data = [screen_name,
                        tweet['id'],
                        tweet['created_at'],
                        tweet['public_metrics']['like_count'],
                        tweet['public_metrics']['retweet_count'],
                        tweet['public_metrics']['reply_count'],
                        tweet['public_metrics']['quote_count'],
                        tweet['text'].encode('ascii', 'ignore')]
            writer.writerow(csv_data)
