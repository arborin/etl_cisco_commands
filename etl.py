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


def result_search(pattern, text):
    result = re.search(pattern, text)
    if result:
        return result.group(1)


def get_parsed_version_job_output(raw_data):
    # {
    #   "IOSv Software": "VIOS-ADVENTERPRISEK9-M",
    #   "Version": "15.9(3)M4",
    #   "RELEASE SOFTWARE": "fc3"
    # }

    print("\n-------------------------------------\n")
    result = {}
    result['IOSv Software'] = result_search('Software \\((.+?)\\)', raw_data)

    result['Version'] = result_search('Version (.+?),', raw_data)
    result['RELEASE SOFTWARE'] = result_search(
        'SOFTWARE \\((.+?)\\)', raw_data)

    print(result)
    print("\n-------------------------------------\n")


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
