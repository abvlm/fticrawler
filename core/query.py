# encoding: utf-8

from html.parser import HTMLParser
from re import findall

import requests


class FtiQuery(HTMLParser):
    """
    Class to implement a query to the remote 'fourtoutici' database.
    """

    GET_URL_PATTERN = "http://www.fourtoutici.top/search.php?action=showsearchresults&q={}&listyear=20xx&search=Recherche"

    def __init__(self):
        """
        Create a Query object to process requests to the 'fourtoutici' database.
        """
        HTMLParser.__init__(self)
        self._result = []

    def handle_starttag(self, tag, attributes):
        if tag == 'a':
            for key, value in attributes:
                if key == 'href' and value.startswith('javascript:popupup'):
                    values = findall(r'\'(.*?)\\\'', value)
                    self._result.append((values[0], values[1]))

    def __getitem__(self, item):
        return self._result[item]

    def get_results(self):
        return self._result

    def process(self, text):
        """
        Process the search query.
        :param text: Text of the query.
        :return: A boolean coarse status.
        """
        status = False
        url = self.GET_URL_PATTERN.format(text.replace(' ', '+'))
        response = requests.get(url)
        if response.status_code == 200:
            self.feed(str(response.content))
            status = True
        return status


if __name__ == '__main__':
    query = FtiQuery()
    if query.process('shakespeare'):
        for name, date in query:
            print("Name: [{}] - Date [{}]".format(name, date))
