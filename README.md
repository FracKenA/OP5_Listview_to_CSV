# OP5 API Listview Filter to CSV
This is a simple python script to create a CSV from a list view filter. It uses only the default libraries included on the OP5 Server so nothing additional is required to be installed.

To use simply download the python file to your OP5 server, or any other server you with to generate the CSV files on.


```
usage: main.py [-h] -u USERNAME -p PASSWORD -q QUERY -f FILE [-s SERVER] [-i INSECURE] [-c COLUMNS] [-l LIMIT] [-o OFFSET] [-t SORT]

OP5 API Query to CSV

Required Arguments:
  -u USERNAME, --username USERNAME
                        OP5 API args.username
  -p PASSWORD, --password PASSWORD
                        OP5 API args.password
  -q QUERY, --query QUERY
                        OP5 Listview Filter to create CSV from. Make sure to enclose with a single quote due to brackets. You can copy the listview filter manual input into this argument.
                        More information can be found at https://docs.itrsgroup.com/docs/op5-monitor/8.1.0/topics/configure/list-view-filters.html
  -f FILE, --file FILE  CSV file to create. Relative path is supported

Modifier Arguments:
  -s SERVER, --server SERVER
                        OP5 Server DNS Name or IP. Defaults to localhost
  -i INSECURE, --insecure INSECURE
                        Allow invalid and self signed SSL Certificates. True/False
  -c COLUMNS, --columns COLUMNS
                        OPTIONAL: Columns to display. More information can be found at https://docs.itrsgroup.com/docs/op5-monitor/8.1.0/topics/configure/listview-filter-
                        columns.html#List_view_filter_column_reference
  -l LIMIT, --limit LIMIT
                        OPTIONAL: Limit records count. Use Only Integers.
  -o OFFSET, --offset OFFSET
                        OPTIONAL: Offset to start. Use Only Integers.
  -t SORT, --sort SORT  OPTIONAL: Sort records. Comma separated list of columns that dictates the objects order, for example sort=name; sort=name,state or sort=name DESC,state ASC. Note that
                        you cannot sort on "lists", such as the "parents" field in the "hosts" table.
```

The links to find more information on how to use these options and modifiers please visit the following URLs.

### Building Queries
[https://docs.itrsgroup.com/docs/op5-monitor/8.1.0/topics/configure/list-view-filters.html](https://docs.itrsgroup.com/docs/op5-monitor/8.1.0/topics/configure/list-view-filters.html)

### Selecting Columns
[https://docs.itrsgroup.com/docs/op5-monitor/8.1.0/topics/configure/listview-filter-columns.html#List_view_filter_column_reference]()

### Limit, Offset and Sort
Please visit your OP5 Server at the following address.
`https://OP5_Hostname_or_IP_Address/api/help/filter/query`
