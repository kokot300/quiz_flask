#!/usr/bin/python

from requests import get


def get_cats():
    api_endpoint = 'https://opentdb.com/api_category.php'
    response = get(api_endpoint)
    data = response.json()
    return data['trivia_categories']


def get_questions(category=None):
    if category is None:
        api_endpoint = 'https://opentdb.com/api.php?amount=5&type=multiple'
    else:
        api_endpoint = f'https://opentdb.com/api.php?amount=5&category={category}&type=multiple'
    response = get(api_endpoint)
    data = response.json()
    return data['results']


if __name__ == '__main__':
    get_questions()
