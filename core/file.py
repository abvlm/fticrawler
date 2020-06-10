from urllib.parse import quote
from re import findall

import requests


class FtiFile:
    """
    Class to retrieve a file from the 'fourtoutici' server.
    The 'secret' code is automatically generated by analyzing the response to the first GET request.
    """

    GET_URL_PATTERN = 'http://www.fourtoutici.top/upload.php?action=downloadfile&filename={}&directory={}&'
    POST_URL_PATTERN = 'http://www.fourtoutici.top/upload.php?action=download&directory={}&filename={}&valcodeup={}'

    def __init__(self, name, date):
        """
        Create a RemoteResource given the name of the resource and its date.
        :param name: Name of the resource.
        :param date: Date associated to the resource.
        """
        self._response = None
        self._name = name
        self._date = date

    def request_file(self):
        """
        Process with the file download.
        :return: A boolean coarse status.
        """
        status = False
        response = requests.get(self._build_get_url())
        if response.status_code == 200:
            data = str(response.content)
            try:
                code_id = findall(r'"codeup.php\?(\d*)"', data)[0]
                post_code = self._get_code(code_id)
                print("Code [{}] - [{}]".format(code_id, post_code))
                status = self._download_file(post_code)
            except IndexError:
                raise FtiException('Unable to parse the HTML response [{}]'.format(data))
        return status

    def get_response(self):
        """
        Retrieve the response of the request.
        :return: The result as a Response object, or None if something failed.
        """
        return self._response

    def _build_get_url(self):
        """
        Convert the name and date of a resource to its URL, as done by popupup javascript.
        :param name: Name of the resource as given to the popupup script.
        :param date: Date associated to the resource as given to the popupup script.
        :return: The URL to access the resource download form.
        """
        return self.GET_URL_PATTERN.format(quote(self._name), self._date)

    def _build_post_url(self, code):
        """
        Convert the name, date and code of a resource to its URL.
        :param code: The code needed for the post request.
        :return: The URL to download the resource.
        """
        return self.POST_URL_PATTERN.format(quote(self._date), self._name.replace(' ', '+'), code)

    def _get_code(self, code_id):
        """
        Parse the ID given to the codeup.php script. It is the current timestamp.
        As far as I understood, the code is built the following way:
            - 3rd character of the ID.
            - 9th and 10th characters of the ID.
            - 8th character of the ID.
        :param code_id: ID of the request, sent to the codeup.php script.
        :return: the code to apply for the download.
        """
        if len(code_id) != 10:
            raise FtiException("Unable to parse the ID [{}] - Length {} vs 10 expected".format(code_id, len(code_id)))
        return int("{}{}{}".format(code_id[2], code_id[8:10], code_id[7]))

    def _download_file(self, code):
        """
        Process to the file download.
        :param destination_directory: Directory where to store the downloaded file.
        :param code: The code to use within the POST request.
        :return: A boolean coarse status.
        """
        status = False
        post_url = self._build_post_url(code)
        response = requests.post(post_url)
        if response.status_code == 200:
            # A html start tag denotes a failure.
            if not response.content.startswith(b'<html>'):
                status = True
                self._response = response
            else:
                print('Unexpected content [{}/{}]'.format(self._name, code))
        else:
            print('Unexpected status code [{}]'.format(response.status_code))
        return status


if __name__ == '__main__':
    file_name = 'EBOOK William Shakespeare - Titus Andronicus.epub'
    file_date = '/2018/2018-02/2018-02-16'
    file = FtiFile(file_name, file_date)
    status = file.request_file()
    print("Download status is {}".format(status))
    if status:
        response = file.get_response()
        print("Response length is {} bytes".format(len(response.content)))
