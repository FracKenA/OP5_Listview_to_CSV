#!/usr/bin/python3

import csv
import http.client
import json
from urllib.parse import urlencode, quote_plus
import base64
import ssl
import argparse
import os

parser = argparse.ArgumentParser(description="OP5 API Query to CSV")
parser._action_groups.pop()
required = parser.add_argument_group('Required Arguments')
optional = parser.add_argument_group('Modifier Arguments')

required.add_argument("-u", "--username", help="OP5 API args.username", type=str, required=True)
required.add_argument("-p", "--password", help="OP5 API args.password", type=str, required=True)
required.add_argument("-q", "--query", help="OP5 Listview Filter to create CSV from. Make sure to enclose with a single quote due to brackets. You can copy the listview filter manual input into this argument. More information can be found at https://docs.itrsgroup.com/docs/op5-monitor/8.1.0/topics/configure/list-view-filters.html", type=str, required=True)
required.add_argument("-f", "--file", help="CSV file to create. Relative path is supported. If the file exists, it will be appended.", type=str, required=True)
optional.add_argument("-s", "--server", help="OP5 Server DNS Name or IP. Defaults to localhost", default="localhost", type=str)
optional.add_argument("-i", "--insecure", help="Allow invalid and self signed SSL Certificates. This argument has no options", action='store_true')
optional.add_argument("-c", "--columns", help="OPTIONAL: Columns to display. More information can be found at https://docs.itrsgroup.com/docs/op5-monitor/8.1.0/topics/configure/listview-filter-columns.html#List_view_filter_column_reference", type=str)
optional.add_argument("-l", "--limit", help="OPTIONAL: Limit records count. Use Only Integers.", type=int)
optional.add_argument("-o", "--offset", help="OPTIONAL: Offset to start. Use Only Integers.", type=int)
optional.add_argument("-t", "--sort", help="OPTIONAL: Sort records. Comma separated list of columns that dictates the objects order, for example sort=name; sort=name,state or sort=name DESC,state ASC. Note that you cannot sort on \"lists\", such as the \"parents\" field in the \"hosts\" table.", type=str)


args = parser.parse_args()

if args.insecure:
    conn = http.client.HTTPSConnection(
        args.server,
        context=ssl._create_unverified_context()
    )
else:
    conn = http.client.HTTPSConnection(
        args.server
    )

payload = ""

to_encode = {
    'format': 'json',
    'query': args.query
}

if args.columns:
    to_encode['columns'] = args.columns

if args.limit:
    to_encode['limit'] = args.limit

if args.offset:
    to_encode['offset'] = args.offset

if args.sort:
    to_encode['sort'] = args.sort

user_pass = str.encode('{username}:{password}'.format(username=args.username, password=args.password))

encoded_auth = base64.b64encode(user_pass).decode('utf=8')

encoded_url = urlencode(to_encode, quote_via=quote_plus)

headers = {
    'accept': "application/json",
    'Authorization': "Basic %s" % encoded_auth
}

conn.request("GET", "/api/filter/query?{query}".format(query=encoded_url), payload, headers)

res = conn.getresponse()
data = res.read()

json_results = json.loads(data)

if os.path.exists(args.file):
    filemode = "a"
else:
    filemode = "w"

csv_file = open(args.file, filemode)

csv_write = csv.writer(csv_file)

count = 0

for result in json_results:
    if count == 0:
        header = result.keys()
        csv_write.writerow(header)
        count += 1
    csv_write.writerow(result.values())

csv_file.close()

print('completed creating {path}'.format(path=os.path.abspath(args.file)))
