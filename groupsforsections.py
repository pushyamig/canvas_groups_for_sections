import json
import sys
import logging
import requests
import utils
from canvasapis import GroupsForSections
import yaml
from os.path import basename
from collections import defaultdict
from os import environ

CONST_CANVAS = 'canvas'
CONST_COURSE = 'course'
CONST_TOKEN = 'token'
CONST_URL = 'url'
CONST_ID = 'id'
CONST_GRP_CAT_NAME = 'group_category_name'


def create_group_category(group_category_name, groups_for_section, course_id):
    """
    The call creating the group category in a course, parse the Json, exception handling
    :param group_category_name:
    :param groups_for_section:
    :param course_id
    :type group_category_name: str
    :type groups_for_section: GroupsForSections
    :type course_id: str
    :return: group category id
    :rtype: str, None
    """
    try:
        response = groups_for_section.create_group_category(group_category_name, course_id)

    except (requests.exceptions.RequestException, Exception) as e:
        logging.exception('creating a group categories has erroneous response ' + e.message)
        return None

    if not handle_request_if_failed(response):
        return None

    group_category = json.loads(response.text)

    return str(group_category['id'])


def get_sections_for_course(sections_dict, groups_for_section, course_id, next_page_url=None):
    """
    getting all the section for a  course,  paginates if needed, parse the json, do the exception handling.
    :param sections_dict:
    :param groups_for_section:
    :param course_id
    :param next_page_url:
    :type sections_dict: dict
    :type groups_for_section: GroupsForSections
    :type course_id:str
    :type next_page_url: str
    :return: sections = {name, id}
    :rtype: dict, None
    """
    logging.debug(get_sections_for_course.__name__ + '() called')

    try:
        response = groups_for_section.sections_for_course(course_id, next_page_url)

    except (requests.exceptions.RequestException, Exception) as e:
        logging.exception('getting sections has erroneous response ' + e.message)
        return None

    if not handle_request_if_failed(response):
        return None

    section_list = json.loads(response.text)

    if not section_list:
        return sections_dict

    for section in section_list:
        sections_dict[section['id']] = section['name']

    next_page_url = groups_for_section.get_next_page_url(response)
    if next_page_url is not None:
        get_sections_for_course(sections_dict, groups_for_section, course_id, next_page_url)

    return sections_dict


def get_users_in_section(groups_for_section, users_in_section, section_id=None, next_page_url=None):
    """
    get all the users in the sections, paginates, parse Json,  exception handling.

    :param groups_for_section:
    :param users_in_section:
    :param section_id:
    :param next_page_url:
    :type groups_for_section: GroupsForSections
    :type users_in_section: list
    :type section_id: str
    :type next_page_url: str
    :return: users[id]
    :rtype: list, None
    """
    logging.debug(get_users_in_section.__name__ + '() called')
    try:
        response = groups_for_section.users_in_section(section_id, next_page_url)

    except (requests.exceptions.RequestException, Exception) as e:
        logging.exception('getting USERS list has erroneous response ' + e.message)
        return None

    if not handle_request_if_failed(response):
        return None

    user_list = json.loads(response.text)

    for user in user_list:
        users_in_section.append(str(user['user_id']))

    next_page_url = groups_for_section.get_next_page_url(response)
    if next_page_url is not None:
        get_users_in_section(groups_for_section, users_in_section, None, next_page_url)

    return users_in_section


def create_group(groups_for_section, group_category_id, group_name, course_id):
    """
    creates a group with name same as section name, parses Json, do exception handling
    :param groups_for_section:
    :param group_category_id:
    :param group_name:
    :param course_id:
    :type groups_for_section: GroupsForSections
    :type group_category_id: str
    :type group_name: str
    :type course_id: str
    :return: group_id
    :rtype str, None
    """
    logging.debug(create_group.__name__ + '() called')
    try:
        response = groups_for_section.create_group(group_category_id, group_name, course_id)
    except (requests.exceptions.RequestException, Exception) as e:
        logging.exception('creating a GROUP has erroneous response ' + e.message)
        return None

    if not handle_request_if_failed(response):
        return None

    group = json.loads(response.text)
    return str(group['id'])


def add_users_to_group(groups_for_section, group_id, user):
    """
    adding user to a group, parses Json, do exception handling
    :param groups_for_section:
    :param group_id:
    :param user:
    :type groups_for_section GroupsForSections
    :type group_id str
    :type user str
    :return: membership_id
    :rtype: int, None
    """
    logging.debug(add_users_to_group.__name__ + '() called')
    try:
        response = groups_for_section.add_users_to_group(group_id, user)

    except (requests.exceptions.RequestException, Exception) as e:
        logging.exception('adding USER to group has erroneous response ' + e.message)
        return None

    if not handle_request_if_failed(response):
        return None

    membership = json.loads(response.text)
    return membership['id']


def handle_request_if_failed(response):
    if response.status_code != requests.codes.ok:
        error_msg_handler(response)
        return False
    else:
        return True


def error_msg_handler(response):
    """
    Parsing the error json response. Using yaml instead of json.load to get the error message as logs will show non
    unicode values for eg., [{u'message': u'Invalid access token.'}] ---> [{'message': 'Invalid access token.'}]
    :param response:
    :type requests
    :return: nothing
    """
    try:
        error_res = yaml.safe_load(response.text)
    except Exception as exp:
        logging.exception('Api error response is not in Json format and Response Code: ' + str(
                response.status_code) + exp.message)
    else:
        logging.error('Api response has some errors: ' + str(error_res['errors']) + ' and Response Code: ' + str(
                response.status_code))


def main():
    utils.setup_logging()
    logging.info('Script Started')
    logging.debug('args: ' + str(sys.argv))

    # if len(sys.argv) is not 3:
    #     logging.error("Some of the command line arguments (path to properties files) are missing should be like "
    #                   "'python groupsforsections.py /config.yaml /security.yaml'")
    #     sys.exit(1)
    # config_file = sys.argv[1]
    # security_file = sys.argv[2]
    #
    # logging.debug('reading the file %s ' % basename(security_file))
    #
    # with open(security_file, 'r') as yml_file:
    #     sf = yaml.load(yml_file)
    #
    # if not sf or CONST_CANVAS not in sf:
    #     logging.error('The key \'canvas\' is missing ')
    #     sys.exit(1)
    #
    # logging.debug('reading the file %s ' % basename(config_file))
    #
    # with open(config_file, 'r') as yml_file:
    #     cfg = yaml.load(yml_file)
    #
    # if not cfg or CONST_COURSE not in cfg:
    #     logging.error('The key \'course\' is missing ')
    #     sys.exit(1)
    #
    # if not sf[CONST_CANVAS] or CONST_TOKEN not in sf[CONST_CANVAS] or CONST_URL not in sf[CONST_CANVAS] or \
    #         not cfg[CONST_COURSE] or CONST_ID not in cfg[CONST_COURSE] or CONST_GRP_CAT_NAME not in cfg[CONST_COURSE]:
    #     logging.error("Some of the keys are missing from the properties files %s:  %s , %s:   %s"
    #                   % (basename(security_file), '"canvas keys missing" ' if sf[CONST_CANVAS] is None else sf[CONST_CANVAS].keys(),
    #                      basename(config_file), '"course keys missing"' if cfg[CONST_COURSE] is None else cfg[CONST_COURSE].keys()))
    #     sys.exit(1)

    # course_id = cfg[CONST_COURSE][CONST_ID]
    # group_category_name = cfg[CONST_COURSE][CONST_GRP_CAT_NAME]
    # canvas_token = sf[CONST_CANVAS][CONST_TOKEN]
    # canvas_url = sf[CONST_CANVAS][CONST_URL]

    course_id = environ['COURSE_ID']
    group_category_name = environ['CAT_NAME']
    canvas_token = environ['CANVAS_TOKEN']
    canvas_url = environ['CANVAS_URL']

    if course_id is None or group_category_name is None or canvas_token is None or canvas_url is None:
        logging.error("some of the configurations from properties file are missing: "
                      "course_id = " + str(course_id) + " ; group_category_name = " + str(group_category_name) +
                      " ; canvas_url = " + str(canvas_url) + " ;  canvas_token = " +
                      (str(canvas_token) if canvas_token is None else "Not_Shown"))
        sys.exit(1)

    logging.debug('Canvas Token: ' + canvas_token)
    logging.info('Canvas URL: ' + canvas_url)
    logging.info('Course Id: ' + course_id)
    logging.info('Group Category Name: ' + group_category_name)

    # instantiating the class
    groups_for_section_class = GroupsForSections(canvas_token, canvas_url)
    # this hold the list of users that needs to be added to a group, group => users
    groups_to_users_dict = {}

    group_category_id = create_group_category(group_category_name, groups_for_section_class, course_id)

    if group_category_id is None:
        logging.error('Group category "%s" is not created for course %s ' %(group_category_name, course_id))
        sys.exit(1)

    sections = get_sections_for_course({}, groups_for_section_class, course_id)

    if sections is None or not sections:
        logging.error('No sections in the course or error in getting sections for the course: ' + course_id)
        sys.exit(1)

    logging.info(
        'Total # of sections that are in course %s are %d and are %s ' % (course_id, len(sections), sections.keys()))
    for section_id in sections:
        users = get_users_in_section(groups_for_section_class, [], str(section_id))

        if users is None:
            logging.error('Could not get users in section %s(%s): ' % (section_id, sections[section_id]))
            sys.exit(1)

        logging.info('section %s (%s) has %s users : ' % (section_id, sections[section_id], str(len(users))))

        # creating one group for each section in course.
        group_id = create_group(groups_for_section_class, str(group_category_id), sections[section_id], course_id)

        if group_id is None:
            logging.error('Could not create group for section %s(%s): ' % (section_id, sections[section_id]))
            sys.exit(1)

        logging.info('The Group id %s created for the Section %s with name %s'
                     % (str(group_id), section_id, sections[section_id]))

        # mapping all the users in a sections to corresponding group
        groups_to_users_dict[group_id] = users

    failed_groups_to_users_dict=defaultdict(list)
    success_groups_to_users_dict=defaultdict(list)

    # adding users to the group
    for group, users in groups_to_users_dict.items():
        for user in users:
            membership_id = add_users_to_group(groups_for_section_class, group, user)
            if membership_id is None:
                logging.error('The user %s is not added to the group %s' % (user, group))
                failed_groups_to_users_dict[group].append(user)
            else:
                success_groups_to_users_dict[group].append(user)
                logging.info('The User %s got added to the Group %s  with membership id  %s ' %(user, group, str(membership_id)))

    # logging total users that belongs to corresponding group
    logging.info("**** Total Users List in a Group set: ")
    for group in groups_to_users_dict:
        logging.info('%d users should be added to the group %s' % (len(groups_to_users_dict[group]), group))

    # logging the total successful users added to the each group
    if success_groups_to_users_dict:
        logging.info("**** Successful Addition of Users to Groups: ")
        for group in success_groups_to_users_dict:
            logging.info('%d users successfully added to the group %s' % (len(success_groups_to_users_dict[group]),group))

    # logging the users list that was not added to a group
    if failed_groups_to_users_dict :
        logging.error("**** Failed Addition of Users to Groups: ")
        for group in failed_groups_to_users_dict:
            users = ','.join(failed_groups_to_users_dict[group])
            logging.info('%d users are not added in the group %s and they are %s ' % (len(failed_groups_to_users_dict[group]),group, users))

    logging.info('script ran successfully')


if __name__ == '__main__':
    main()
