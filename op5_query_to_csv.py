#!/usr/bin/python3

# This file is provided as is under the MIT license.
# This file was created by Ken Dobbins at ITRS Group (kdobbins@itrsgroup.com)

import csv
import http.client
import json
from urllib.parse import urlencode, quote_plus
import base64
import ssl
import argparse
import os

# Create the command line argument parser
parser = argparse.ArgumentParser(description="OP5 API Query to CSV")

# Add the groups for the required and optional command line arguments. Also hide the default grouping
parser._action_groups.pop()
required = parser.add_argument_group('Required Arguments')
optional = parser.add_argument_group('Modifier Arguments')

# Add the command line arguments that are required.
required.add_argument("-u", "--username", help="OP5 API username", type=str, required=True)
required.add_argument("-p", "--password", help="OP5 API password", type=str, required=True)
required.add_argument("-q", "--query", help="OP5 Listview Filter to create CSV from. Make sure to enclose with a single quote due to brackets. You can copy the listview filter manual input into this argument. More information can be found at https://docs.itrsgroup.com/docs/op5-monitor/8.1.0/topics/configure/list-view-filters.html", type=str, required=True)
required.add_argument("-f", "--file", help="CSV file to create. Relative path is supported. If the file exists, it will be appended.", type=str, required=True)

# Add the command line arguments that are optional.
optional.add_argument("-s", "--server", help="OP5 Server DNS Name or IP. Defaults to localhost", default="localhost", type=str)
optional.add_argument("-i", "--insecure", help="Allow invalid and self signed SSL Certificates. This argument has no options", action='store_true')
optional.add_argument("-c", "--columns", help="OPTIONAL: Columns to display. More information can be found at https://docs.itrsgroup.com/docs/op5-monitor/8.1.0/topics/configure/listview-filter-columns.html#List_view_filter_column_reference", type=str)
optional.add_argument("-l", "--limit", help="OPTIONAL: Limit records count. Use Only Integers.", type=int)
optional.add_argument("-o", "--offset", help="OPTIONAL: Offset to start. Use Only Integers.", type=int)
optional.add_argument("-t", "--sort", help="OPTIONAL: Sort records. Comma separated list of columns that dictates the objects order, for example sort=name; sort=name,state or sort=name DESC,state ASC. Note that you cannot sort on \"lists\", such as the \"parents\" field in the \"hosts\" table.", type=str)

# Parse the arguments into variables.
args = parser.parse_args()

# Determine if we are going to connect accepting any SSL certificate or require validation.
if args.insecure:
    conn = http.client.HTTPSConnection(
        args.server,
        context=ssl._create_unverified_context()
    )
else:
    conn = http.client.HTTPSConnection(
        args.server
    )

# Add the required fields to be parsed into the URL for the GET request.
to_encode = {
    'format': 'json',
    'query': args.query
}

# Add the optional fields to be parsed into the URL for the GET request.
if args.columns:
    to_encode['columns'] = args.columns

if args.limit:
    to_encode['limit'] = args.limit

if args.offset:
    to_encode['offset'] = args.offset

if args.sort:
    to_encode['sort'] = args.sort

# Create the headers to allow authentication and return encoding.
headers = {
    'accept': "application/json",
    'Authorization': 'Basic {auth_string}'.format(auth_string=base64.b64encode(str.encode('{username}:{password}'.format(username=args.username, password=args.password))).decode('utf=8'))
}

# perform the GET request for the results.
conn.request("GET", "/api/filter/query?{query}".format(query=urlencode(to_encode, quote_via=quote_plus)), None, headers)

# Process the response of the GET request.
res = conn.getresponse()

if res.status >= 400:
    print('Server returned status code {status} - {reason}'.format(status=res.status, reason=res.reason))
    exit(1)

# Create JSON from the results.
json_results = json.loads(res.read())

# Determine of the CSV file exists on disk.
if os.path.exists(args.file):
    filemode = "a"
    action = "appending"
else:
    filemode = "w"
    action = "creating"

# Open the CSV File
csv_file = open(args.file, filemode)

# Create the CSV writer.
csv_write = csv.writer(csv_file)

# Set the results counter to 0
count = 0

# Write each row to the CSV.
for result in json_results:
    # if this file is empty, create the CSV header row.
    if count == 0:
        # Use the JSON element Keys as the header for the CSV.
        header = result.keys()
        # Write the CSV header row.
        csv_write.writerow(header)
        # Increment the count for the next row.
        count += 1
    # Write all the data from the JSON to the CSV.
    csv_write.writerow(result.values())

# Close the CSV file.
csv_file.close()

# Notify the completion of the process.
print('completed {action} {path}'.format(action=action, path=os.path.abspath(args.file)))
