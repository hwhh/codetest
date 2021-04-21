import sqlite3

CO_PROJECT_DIRECTORS = '[Co Project Director]'


class Reports:

    def __init__(self, db_path: str):
        self.db_path = db_path

    def participants_by_state(self, state: str) -> [str]:
        result = set()
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        query_result = cur.execute("SELECT Participants FROM t "
                                   "WHERE Participants LIKE ?"
                                   "AND InstState = ?", ['%' + CO_PROJECT_DIRECTORS + '%', state])
        for row in query_result:
            for name in row[0].split(';'):
                if name.endswith(CO_PROJECT_DIRECTORS):
                    result.add(name[:-len(CO_PROJECT_DIRECTORS)].strip())
        con.close()
        return list(result)

    def supplements_agg(self) -> dict:
        result = dict()
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        query_result = cur.execute("SELECT Supplements FROM t "
                                   "WHERE Supplements IS NOT ''")
        for row in query_result:
            for entry in row[0].split(';'):
                amount, date = entry.strip().split(' ')
                year = date[1:-1].split('/')[-1]
                if year in result:
                    result[year] += float(amount)
                else:
                    result[year] = float(amount)
        con.close()
        return result

    """
    assumed grant sum = AwardOutright + AwardMatching
    """

    def project_by_state(self) -> dict:
        result = dict()
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        query_result = cur.execute(
            "SELECT InstState, COUNT(*), SUM(CAST(AwardOutright AS INT) + CAST(AwardMatching AS INT)) "
            "FROM t GROUP BY InstState")
        for row in query_result:
            result[row[0].strip()] = {'project count': row[1], 'grant agg': row[2]}
        con.close()
        return result
