from apps.util.redis_query.query_factory import query
from apps.util.redis_query.task import controller_report_info


# import sys
# from os.path import dirname, realpath
#
# root_project_dir = dirname(dirname(realpath(__file__)))
# if root_project_dir not in sys.path:
#     sys.path.append(root_project_dir)


def controller_report(report_data):
    query.enqueue(controller_report_info, report_data)


data = {
    'device_num': '1',
    'loop_num': '1',
    'addr_num': '1',
    'datetime': '20220609091421',
    'event_type': '4',
    'event_state': '1',
    'event_statetype': '35',
    'type': '260'
}
controller_report(data)
