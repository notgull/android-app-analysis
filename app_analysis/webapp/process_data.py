# GNU AGPL v3 License
# Written by John Nunley
# Process data

from . import db
import enum

def get_results(search = None):
    # Look up apps in database by app_name
    # Return a list of dictionaries
    # Each dictionary contains id, title and analysis state
    # If search is None, return all apps
    # If search is not None, return apps that match search
    # If no apps match search, return an empty list
    d = db.get_db()

    if search is None:
        rows = d.execute(
            'SELECT id, app_name, analysis_state FROM apps'
        ).fetchall()
    else:
        rows = d.execute(
            'SELECT id, app_name, analysis_state FROM apps WHERE app_name LIKE ?',
            ('%' + search + '%',)
        ).fetchall()

    results = []
    for row in rows:
        results.append({
            'id': row[0],
            'title': row[1],
            'analysis_state': AnalysisState(row[2])
        })

    return results

def app_data(id):
    # Get the apps:
    # - app_id
    # - app_name
    # - developer
    # - category
    # - summary
    # also get the vulnerabilities
    # - vulnname
    # - cwe
    # - owasp_mobile
    # - descript
    # - severity

    d = db.get_db()

    rows = d.execute(
        'SELECT id, title, developer, category, summary FROM apps WHERE id = ?',
        (id,)
    ).fetchone()

    # there is a table, vuln_mapping, that maps app_id to vuln_id
    vulns = d.execute(
        '''
        SELECT
            v.id,
            v.vulnname,
            v.cwe,
            v.owasp_mobile,
            v.descript,
            v.severity
        FROM
            vulns v
        INNER JOIN
            vuln_mapping vm
        ON
            v.id = vm.vuln_id
        WHERE
            vm.app_id = ?
        '''
        , (id,)
    ).fetchall()

    vulnerabilities = []
    for row in vulns:
        vulnerabilities.append({
            'id': row[0],
            'vulnname': row[1],
            'cwe': row[2],
            'owasp_mobile': row[3],
            'descript': row[4],
            'severity': row[5]
        })

    return {
        'id': rows[0],
        'title': rows[1],
        'developer': rows[2],
        'category': rows[3],
        'summary': rows[4],
        'vulnerabilities': vulnerabilities
    }

class AnalysisState(enum.Enum):
    # Enum to represent the state of an app analysis
    # 0 = Not analyzed
    # 1 = In progress
    # 2 = Complete
    NOT_ANALYZED = 0
    IN_PROGRESS = 1
    COMPLETE = 2