from csv_to_sql import CsvUtil

csv_util = CsvUtil('../../resources/neh-grants-2010-2019-csv-1.csv')
csv_util.convert_csv_to_sql()
