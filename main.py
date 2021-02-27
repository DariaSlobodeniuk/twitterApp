import seaborn as sns
import json
import tweepy as tw
import warnings


search_words = ["#mike", "#kharkiv", "#ukraine", "#tramp", "#fair"]
date_since = "2018-11-16"

id = 0
listJson = {}
twList = {}
twListJson = {}

#get api
def get_api_twitter():
    warnings.filterwarnings("ignore")
    sns.set(font_scale=1.5)
    sns.set_style("whitegrid")

    consumer_key = 'Tn7VAwFqJQOyuXZPDkiRDt7RX'
    consumer_secret = 'YzWMHBrwmeS8bjK68zq609fCIuAqIDLQqZA6oXDsVB6FB5fg7Y'
    access_token = '1279534592668598277-xeetdkB6XEhHgEUKADO4QVloczwRlo'
    access_token_secret = 'G5H6quuPrz2MhHYm9cKn7Svx5M9IGz4AOeml8brtunicW'

    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)
    return api


# get tweets

def get_tweets(listWords, date, api):
    for sw in listWords:
        tweets = tw.Cursor(api.search,
                           q=sw,
                           lang="en",
                           since=date).items(5)
        for tweet in tweets:
            twList['tweet'] = tweet
            twListJson = tweet._json
            print(twListJson)
        return twListJson


#print(get_tweets(search_words, date_since, get_api_twitter()))
listoftweetswithselectedhashtags={}
with open('tweets.json', 'w', encoding='utf-8') as f:
    for word in search_words:
        listoftweetswithselectedhashtags[word] = get_tweets(word,date_since,get_api_twitter())
    json.dump(listoftweetswithselectedhashtags, f, ensure_ascii=False, indent=id)
    f.write('\n')
