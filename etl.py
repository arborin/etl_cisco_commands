import json
import logging
import re
import sys

# from airflow.exceptions import AirflowFailException

logger = logging.getLogger(__name__)


def get_parsed_job_output(job_name, raw_data):
    if job_name == 'version':
        pass
        return get_parsed_version_job_output(raw_data)

    if job_name == 'inventory':
        pass
        # return get_parsed_inventory_job_output(raw_data)

    logger.info('invalid job_name in config.')
    sys.tracebacklimit = 0  # set sys.tracebacklimit = None to enable it back
    # raise AirflowFailException("invalid job_name in config.") # task fails without retrying


# def result_search(pattern, text):
#     result = re.search(pattern, text)
#     if result:
#         return result.group(1)


# def get_parsed_version_job_output(raw_data):
#     # {
#     #   "IOSv Software": "VIOS-ADVENTERPRISEK9-M",
#     #   "Version": "15.9(3)M4",
#     #   "RELEASE SOFTWARE": "fc3"
#     # }
#     # error handling
#     result = {}
#     result['IOSv Software'] = result_search('Software \\((.+?)\\)', raw_data)
#     result['Version'] = result_search('Version (.+?),', raw_data)
#     result['RELEASE SOFTWARE'] = result_search(
#         'SOFTWARE \\((.+?)\\)', raw_data)

#     print(result)


def get_json_from_text(raw_data):

    start = raw_data.find("{")  # start index
    end = raw_data.rfind("}")  # end index
    json_str = raw_data[start:end+1]  # get json txt

    clean_str = ''

    for line in json_str.split('\n'):
        clean_str += line.replace('\\n', ',').strip()

    return json.loads(clean_str)


def get_parsed_version_job_output(raw_data):
    # {
    #   "IOSv Software": "VIOS-ADVENTERPRISEK9-M",
    #   "Version": "15.9(3)M4",
    #   "RELEASE SOFTWARE": "fc3"
    # }

    json_data = {}
    result = get_json_from_text(raw_data)
    result = result['msg']['stdout'][0].split(',')
    json_data['iosv_software'] = result[1].strip()
    json_data['version'] = result[2].strip()
    json_data['release_software'] = result[3].strip()

    print(json_data)


def main():

    file_path = 'cisco-nxos-show-version.txt'
    job_name = 'version'

    # file_path = 'path to cisco-nxos-show-version.txt'
    # job_name = 'version'

    # parse argument list

    with open(file_path, 'r') as f:
        raw_data = f.read()

    parsed_job_output = get_parsed_job_output(job_name, raw_data)

    # logger.info(json.dumps(parsed_job_output, indent=4))
    # with open('out.json', 'w+') as f:
    #     json.dump(parsed_job_output, f, indent=4)


if __name__ == '__main__':
    main()
