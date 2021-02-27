import export
import requests
import os
import json
import tweepy as tw


# To set your enviornment variables in your terminal run the following line:
BEARER_TOKEN='AAAAAAAAAAAAAAAAAAAAAOE%2BKgEAAAAAA4FImndyXBO4hwq5X80up86jhgo%3DJLcBhaHJFbn1IkBfhiuEExEroUZmkTm8161p2kgJidZvlilkaD'

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def get_rules(headers, bearer_token):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", headers=headers
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()


def delete_all_rules(headers, bearer_token, rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))


def set_rules(headers, delete, bearer_token):
    # You can adjust the rules if needed
    sample_rules = [
        {"value": "dog has:images", "tag": "dog pictures"},
        {"value": "cat has:images -grumpy", "tag": "cat pictures"},
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))


def get_stream(headers, set, bearer_token):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream", headers=headers, stream=True,
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            print(json.dumps(json_response, indent=4, sort_keys=True))


def main():
    consumer_key = 'Tn7VAwFqJQOyuXZPDkiRDt7RX'
    consumer_secret = 'YzWMHBrwmeS8bjK68zq609fCIuAqIDLQqZA6oXDsVB6FB5fg7Y'
    access_token = '1279534592668598277-xeetdkB6XEhHgEUKADO4QVloczwRlo'
    access_token_secret = 'G5H6quuPrz2MhHYm9cKn7Svx5M9IGz4AOeml8brtunicW'

    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tw.API(auth, wait_on_rate_limit=True)
    bearer_token = "BEARER_TOKEN"
    headers = create_headers(bearer_token)
    rules = get_rules(headers, bearer_token)
    delete = delete_all_rules(headers, bearer_token, rules)
    set = set_rules(headers, delete, bearer_token)
    get_stream(headers, set, bearer_token)


if __name__ == "__main__":
    main()