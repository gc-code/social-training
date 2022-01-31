from urllib.parse import urljoin
import requests
import requests.auth


class TwitterAuth(requests.auth.AuthBase):
    def __init__(self, bearer_token, app_name):
        self.bearer_token = bearer_token
        self.app_name = app_name

    def __call__(self, r):
        r.headers['Authorization'] = f'Bearer {self.bearer_token}'
        r.headers['User-Agent'] = self.app_name
        return r


class Twitter:
    def __init__(self, api_url, bearer_token, app_name):
        self.api_url = api_url
        self.bearer_token = bearer_token
        self.app_name = app_name
        self.auth = TwitterAuth(bearer_token, app_name)

    def check_error(self, resp):
        if resp.status_code != 200:
            raise Exception(
                f'Request returned an error: {resp.status_code} {resp.text}'
            )

    def get_user_id(self, screen_name):
        full_url = urljoin(self.api_url, f'2/users/by/username/{screen_name}')
        resp = requests.get(full_url, auth=self.auth)
        user_id = resp.json()['data']['id']
        self.check_error(resp)
        return user_id

    def get_timeline(self, user_id, time_range=None, max_id=None, page_id=None):
        params = f'2/users/{user_id}/tweets?'\
                 f'tweet.fields=created_at,public_metrics'
        if time_range is not None:
            params += f'&start_time={time_range[0]}&end_time={time_range[1]}'
        if max_id is not None:
            params += f'&until_id={max_id}'
        if page_id is not None:
            params += f'&pagination_token={page_id}'
        full_url = urljoin(self.api_url, params)
        resp = requests.get(full_url, auth=self.auth)
        self.check_error(resp)
        return resp.json()
