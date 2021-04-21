import csv
import sqlite3
import time
from pathlib import Path


class CsvUtil:

    def __init__(self, csv_path: str, db_path: str = '', create_new_db: bool = False):
        self.csv_path = csv_path
        if not db_path or create_new_db:
            self.db_path = self._create_new_db()
        else:
            self.db_path = db_path

    @staticmethod
    def _create_new_db():
        db_name = 'db_' + str(time.time()).replace('.', '_') + '.db'
        path = Path.joinpath(Path.cwd().parent.parent, 'resources/' + db_name).absolute()
        path.touch()
        return str(path)

    def convert_csv_to_sql(self):
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        with open(self.csv_path, 'r') as f:
            csv_reader = csv.DictReader(f, delimiter=',')
            cur.execute("CREATE TABLE t ({0})".format(', '.join(csv_reader.fieldnames)))
            for row in csv_reader:
                values = [row[col_name] for col_name in csv_reader.fieldnames]
                cur.execute("INSERT INTO t VALUES ({0})".format(', '.join(['?'] * len(values))), values)
        con.commit()
        con.close()
