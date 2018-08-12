import csv
import os
import datetime

from django.http import HttpResponse
from django.shortcuts import render
from operator import itemgetter


def _extract_app_name_and_platform_from_string(string):
    index = 2  # change to 17??
    count = 1  # Count number of {} braces. (as some app ids have them, so need to break after correct closing)
    for char in string[2:]:
        if char == '{':
            count += 1
        elif char == '}':
            count -= 1
        if count == 0:
            break
        index += 1

    index_end_of_app_name = string[17:].find('"') + 17
    application_name = string[17:index_end_of_app_name]
    index_end_of_platform = string[index_end_of_app_name + 14:].find('"')
    platform = string[index_end_of_app_name + 14:index_end_of_platform + index_end_of_app_name + 14]
    return application_name, platform


def _get_datetime_display(unix_timestamp):
    try:
        return datetime.datetime.fromtimestamp(int(unix_timestamp))
    except:
        return None


def _read_csv(file_name):
    file_path = os.path.dirname(__file__) + '\\resources\\' + file_name
    with open(file_path, 'rt') as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = []
        full_data = []
        for row in reader:
            full_data.append(row)
            app_name, platform = _extract_app_name_and_platform_from_string(row[1])

            rows.append({"app": app_name,
                         "platform": platform,
                         "last_mod": _get_datetime_display(row[10]),
                         "expiration": _get_datetime_display(row[11]),
                         "payload": str(row[12]),
                         "priority": row[13],
                         "is_local_only": bool(int(row[14])),
                         "start_time": _get_datetime_display(row[17]),
                         "end_time": _get_datetime_display(row[18])
                         })
    return headers, rows, full_data


def welcome(request):
    return HttpResponse("Hello, World!")


def home(request):
    headers, rows, full_data = _read_csv('Activity.csv')
    return render(request, "home.html", {'headers': headers,
                                         'rows': sorted(rows, key=itemgetter('start_time')),
                                         'full_data': full_data[:15]})
