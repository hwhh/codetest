from csv_util import CsvUtil
from reports import Reports

if __name__ == "__main__":
    csv_util = CsvUtil('../../resources/neh-grants-2010-2019-csv-1.csv')
    path = csv_util.convert_csv_to_sql()
    reports = Reports(path)

    print(reports.participants_by_state('NY'))
    print(reports.supplements_agg())
    print(reports.project_by_state())
