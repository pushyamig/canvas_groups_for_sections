import logging
import requests
import urllib


class GroupsForSections:
    """
    This class makes the api calls to create groups for sections. TODO: this class will be taken out into a separate
    module in a different repo
    """
    HTTP_METHOD_POST = 'Post'
    HTTP_METHOD_GET = 'Get'
    AUTHORIZATION = 'Authorization'
    BEARER = 'Bearer '
    MIME_TYPE_JSON = 'application/json'
    CONTENT_TYPE = 'Content-type'

    def __init__(self, canvas_token, canvas_url):
        self.canvas_token = canvas_token
        self.canvas_url = canvas_url

    def create_group_category(self, group_category_name, course_id):
        """
        Creates a group category with a given name for a particular course, In case of exceptions it throws it to
        calling method

        :param group_category_name:
        :param course_id:
        :type group_category_name: str
        :type course_id: str
        :return: response
        :rtype: requests
        """

        url = self.canvas_url + '/api/v1/courses/' + course_id + '/group_categories?name=' + urllib.quote_plus(
                group_category_name)
        try:
            response = self.make_api_call(url, self.HTTP_METHOD_POST)
        except:
            raise

        return response

    def sections_for_course(self, course_id, next_page_url=None):
        """
        get sections in a course, throws the exception to the calling method
        :param course_id:
        :param next_page_url:
        :type course_id: str
        :type next_page_url: str
        :return: response
        :rtype: requests
        """

        if next_page_url is not None:
            url = next_page_url
        else:
            url = self.canvas_url + '/api/v1/courses/' + course_id + '/sections?page=1&per_page=100'

        try:
            response = self.make_api_call(url, self.HTTP_METHOD_GET)
        except:
            raise

        return response

    def users_in_section(self, section_id, next_page_url=None):
        """
        get Users in a section, In case of exceptions it throws it to calling method
        :param section_id:
        :param next_page_url:
        :type section_id: str
        :type next_page_url: str
        :return: response
        :rtype: requests
        """

        if next_page_url is not None:
            url = next_page_url
        else:
            url = self.canvas_url + '/api/v1/sections/' + section_id + \
                  '/enrollments?page=1&per_page=100&type[]=StudentEnrollment'
        try:
            response = self.make_api_call(url, self.HTTP_METHOD_GET)
        except:
            raise

        return response

    def create_group(self, group_category_id, group_name, course_id):
        """
        Creates a group in course under a particular group category, In case of exceptions it throws it to calling method
        :param group_category_id:
        :param group_name:
        :param course_id:
        :type group_category_id:str
        :type group_name:str
        :type course_id: str
        :return: response
        :rtype: requests
        """

        url = self.canvas_url + '/api/v1/groups?course_id=' + course_id + '&group_category_id=' \
              + group_category_id + '&name=' + urllib.quote_plus(group_name)

        try:
            response = self.make_api_call(url, self.HTTP_METHOD_POST)
        except:
            raise

        return response

    def get_next_page_url(self, response):
        """
        get the next page url from the Http response headers
        :param response:
        :type response: requests
        :return: next_page_url
        :rtype: str
        """
        logging.debug(self.get_next_page_url.__name__ + '() called')

        if not response.links:
            logging.debug('The api call do not have Link headers')
            return None

        for page in response.links:
            if 'next' in page:
                return response.links['next']['url']

    def make_api_call(self, url, http_method):
        """
        bubbles up the exception to be caught and handled by original calling function
        :param url:
        :param http_method:
        :type url:str
        :type http_method: str
        :return: response
        :rtype: requests
        """
        try:
            response = self.api_handler(url, http_method)
        except:
            raise

        return response

    def api_handler(self, url, request_type):

        """
        This is the generic api handler for making HTTP calls, will throw a RequestException which encompass
        all of the exceptions that might go wrong in making api call
        More info, https://raw.githubusercontent.com/kennethreitz/requests/master/requests/exceptions.py
        http://docs.python-requests.org/en/master/user/quickstart/#errors-and-exceptions
        :param url:
        :param request_type:
        :type url: str
        :type request_type: str
        :return: api_response
        :rtype: requests
        """
        logging.debug(self.api_handler.__name__ + '() called')
        logging.info('URL: ' + url)
        response = None
        headers = {self.CONTENT_TYPE: self.MIME_TYPE_JSON, self.AUTHORIZATION: self.BEARER + self.canvas_token}
        try:
            if request_type == self.HTTP_METHOD_GET:
                response = requests.get(url, headers=headers)
                logging.info('Link headers: ' + str(response.links))
            elif request_type == self.HTTP_METHOD_POST:
                response = requests.post(url, headers=headers)
        except requests.exceptions.RequestException as request_exception:
            raise request_exception

        return response
