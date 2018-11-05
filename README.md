# electricity-analysis
The script generates these metrics from .csv's containing electricity usage for locations

* Total electricity usage for the month
* Average usage on business days only
* Month-over-month change to average business day usage

The script expects csv's to be in a folder named "Data" located in the same directory as the script
The csv's must be named "LocationName yyyymm"
This is the csv format:
date(yyy-mm-dd),usage(kWh)(int)
