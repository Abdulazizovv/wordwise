import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError
from bot.data.config import API_URL

class API:
    def __init__(self, url: str):
        self.url = url
        self.session = requests.Session()
        self.session.mount("https://", HTTPAdapter(max_retries=3))
        self.session.mount("http://", HTTPAdapter(max_retries=3))

    def get(self, endpoint: str, **kwargs):
        try:
            response = self.session.get(f"{self.url}/{endpoint}", **kwargs)
            response.raise_for_status()
        except HTTPError as e:
            raise e
        return response.json()

    def post(self, endpoint: str, **kwargs):
        try:
            response = self.session.post(f"{self.url}/{endpoint}", **kwargs)
            response.raise_for_status()
        except HTTPError as e:
            raise e
        return response.json()

    def put(self, endpoint: str, **kwargs):
        try:
            response = self.session.put(f"{self.url}/{endpoint}", **kwargs)
            response.raise_for_status()
        except HTTPError as e:
            raise e
        return response.json()

    def delete(self, endpoint: str, **kwargs):
        try:
            response = self.session.delete(f"{self.url}/{endpoint}", **kwargs)
            response.raise_for_status()
        except HTTPError as e:
            raise e
        return response.json()

    def patch(self, endpoint: str, **kwargs):
        try:
            response = self.session.patch(f"{self.url}/{endpoint}", **kwargs)
            response.raise_for_status()
        except HTTPError as e:
            raise e
        return response.json()
    

api = API(API_URL)
# API requests

# Get user by id
def get_user(user_id: int):
    """
    Get user by id
    user_id is telegram user id
    :param user_id: int
    :return: dict
    """
    return api.get(f"botuser/{user_id}")


# Get user via telegram account
def get_user_by_tg_account(tg_account: str):
    """
    Get user via telegram account
    tg_account is telegram user id
    :param tg_account: str
    :return: dict
    """
    return api.get(f"users/{tg_account}")


# Check user
def check_user(user_id: int):
    """
    Check user
    user_id is telegram user id
    :param user_id: int
    :return: dict
    """
    return api.get(f"botuser/check_user/?user_id={user_id}")


# Create user
def create_user(user_id: int, phone_number:str, username: str|None, first_name: str, last_name: str|None):
    """
    Create user
    user_id is telegram user id
    :param user_id: int
    :param username: str
    :param first_name: str
    :param last_name: str
    :return: dict
    """
    response = api.post("botuser/", json={"user_id": user_id, "phone_number": phone_number, "username": username, "first_name": first_name, "last_name": last_name})
    if response:
        return True
    return False


# Update user
def update_user(user_id: int, **kwargs):
    """
    Update user
    user_id is telegram user id
    :param user_id: int
    :param kwargs: dict
    :return: dict
    """
    return api.put(f"botuser/{user_id}", json=kwargs)


# get all user categories
def get_user_categories(user_id: int):
    """
    Get all user categories
    user_id is telegram user id
    :param user_id: int
    :return: dict
    """
    return api.get(f"botuser/{user_id}/categories")


# get bot user categories
def get_bot_user_categories(user_id: int):
    """
    Get bot user categories
    user_id is telegram user id
    :param user_id: int
    :return: dict
    """
    return api.get(f"userwordcategories/get_bot_user_categories/?user_id={user_id}")


# create category
def create_category(user_id: int, name: str, description: str):
    """
    Create category
    user_id is telegram user id
    :param user_id: int
    :param name: str
    :param description: str
    :return: dict
    """
    return api.post("wordcategories/create_category/", json={"user_id": user_id, "category_name": name, "category_description": description})