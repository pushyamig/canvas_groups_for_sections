import json
import sys
import logging
import requests
import urllib
import utils
import yaml
from os.path import basename

AUTHORIZATION = 'Authorization'
BEARER = 'Bearer '
MIME_TYPE_JSON = 'application/json'
CONTENT_TYPE = 'Content-type'
CONST_CANVAS = 'canvas'
CONST_COURSE = 'course'
CONST_TOKEN = 'token'
CONST_URL = 'url'
CONST_ID = 'id'
CONST_GRP_CAT_NAME = 'group_category_name'
HTTP_METHOD_POST = 'Post'
HTTP_METHOD_GET = 'Get'


def create_group_category():
    logging.debug('create_group_category() Called')

    url = canvas_url + '/api/v1/courses/' + course_id + '/group_categories?name=' + urllib.quote_plus(
            group_category_name)
    response = api_handler(url, HTTP_METHOD_POST)
    if response is None:
        logging.error('Api call for \'creating group categories\' is not successful')
        sys.exit(1)

    if response.status_code != requests.codes.ok:
        error_msg_handler(response)
        sys.exit(1)
    group_category = json.loads(response.text)
    return group_category['id']


def api_handler(url, request_type):
    logging.debug('api_handler() called')
    logging.info('Api Request URL: ' + url)
    response = None
    headers = {CONTENT_TYPE: MIME_TYPE_JSON, AUTHORIZATION: BEARER + canvas_token}
    try:
        if request_type == HTTP_METHOD_GET:
            response = requests.get(url, headers=headers)
        elif request_type == HTTP_METHOD_POST:
            response = requests.post(url, headers=headers)
    except requests.exceptions.RequestException as e:
        logging.exception(api_handler.__name__ + ' has some erroneous response ' + e.message)

    return response


def error_msg_handler(response):
    # using yaml instead of json.load to get the error message as logs  will show non unicode values in logs
    # for eg., [{u'message': u'Invalid access token.'}] ---> [{'message': 'Invalid access token.'}]

    error_res = yaml.safe_load(response.text)
    logging.error('Api response has some errors: ' + str(error_res['errors']) + ' and Response Code: ' + str(
            response.status_code))


def main():
    global course_id, group_category_name, canvas_token, canvas_url

    utils.setup_logging()
    logging.info('Script Started')
    logging.debug('args: ' + str(sys.argv))

    if len(sys.argv) is not 2:
        logging.error("The command line argument (path to properties file) is not provided")
        sys.exit(1)
    config_file = sys.argv[1]
    logging.debug('reading the file %s ' % basename(config_file))

    with open(config_file, 'r') as yml_file:
        cfg = yaml.load(yml_file)

    if not cfg or CONST_COURSE not in cfg or CONST_CANVAS not in cfg:
        logging.error('The keys \'canvas\' or/and \'course\' are missing ')
        sys.exit(1)

    if not cfg[CONST_CANVAS] or CONST_TOKEN not in cfg[CONST_CANVAS] or CONST_URL not in cfg[CONST_CANVAS] or \
            not cfg[CONST_COURSE] or CONST_ID not in cfg[CONST_COURSE] or CONST_GRP_CAT_NAME not in cfg[CONST_COURSE]:
        logging.error('Some of the key are missing from the properties file' +
                      str(cfg[CONST_CANVAS].keys()) + str(cfg[CONST_COURSE].keys()))
        sys.exit(1)

    course_id = cfg[CONST_COURSE][CONST_ID]
    group_category_name = cfg[CONST_COURSE][CONST_GRP_CAT_NAME]
    canvas_token = cfg[CONST_CANVAS][CONST_TOKEN]
    canvas_url = cfg[CONST_CANVAS][CONST_URL]

    if course_id is None or group_category_name is None or canvas_token is None or canvas_url is None:
        logging.error("some of the configurations from \'config.yaml\' are missing: "
                      "course_id = " + str(course_id) + " ; group_category_name = " + str(group_category_name) +
                      " ; canvas_url = " + str(canvas_url) + " ;  canvas_token = " +
                      (str(canvas_token) if canvas_token is None else "Not_Shown"))
        sys.exit(1)

    logging.debug('Canvas Token: ' + canvas_token)
    logging.info('Canvas URL: ' + canvas_url)
    logging.info('Course Id: ' + course_id)
    logging.info('Group Category Name: ' + group_category_name)
    group_category_id = create_group_category()
    logging.info('end of the script')


if __name__ == '__main__':
    main()
