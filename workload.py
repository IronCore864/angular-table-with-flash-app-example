import json

from common.util.db_util import get_connection
from flask import Flask

from util.utils import get_max_delayed_time_in_seconds

app = Flask(__name__)


@app.route("/workload/status")
def get_workload_status():
    workload_status = _get_workload_status_overview()
    return json.dumps(workload_status)


def _get_workload_status_overview():
    SELECT_FIELDS = "hostname, instance_number, partner_id, application_id, vfn, action_time, trans_time, queue_name"
    WHERE_CLAUSE = "queue_name<>'ZZZ'"
    SQL_TPL = """
        SELECT
            {FIELDS}
        FROM
            ibstat.workload
        WHERE
            {CLAUSE}
            AND
            hostname is not null
            AND
            error_flag=' '
        ORDER BY
            hostname, instance_number, partner_id, application_id
    """
    conn = get_connection()
    cur = conn.cursor()

    sql = SQL_TPL.format(FIELDS=SELECT_FIELDS, CLAUSE=WHERE_CLAUSE)
    cur.execute(sql)
    res = cur.fetchall()

    # For dummy ZZZ queue
    WHERE_CLAUSE = "queue_name='ZZZ'"
    sql = SQL_TPL.format(FIELDS=SELECT_FIELDS, CLAUSE=WHERE_CLAUSE)
    cur.execute(sql)
    res += cur.fetchall()

    cur.close()
    conn.close()

    host_inst_map = {}
    inst_queuenum_map = {}
    inst_maxdelay_map = {}

    inst_partner_map = {}
    partner_maxdelay_map = {}
    partner_queuenum_map = {}

    partner_app_map = {}
    app_maxdelay_map = {}
    app_queuenum_map = {}
    app_vfn_map = {}
    
    for row in res:
        # get data from query results
        hostname = row[0].rstrip() 
        inst_num = row[1]
        partner_id = row[2].rstrip() if row[7].rstrip() != "ZZZ" else "TEST"
        app_id= row[3].rstrip() if row[7].rstrip() != "ZZZ" else "TEST"
        vfn = row[4].rstrip() if row[4] is not None else ''
        act_time_delay = get_max_delayed_time_in_seconds(row[5])
        trans_time_delay = get_max_delayed_time_in_seconds(row[6])
        delay = max(act_time_delay, trans_time_delay)
        
        # get host-instance map
        host_inst_map[hostname] = host_inst_map.get(hostname, list())
        if not inst_num in host_inst_map.get(hostname):
            host_inst_map.get(hostname).append(inst_num)

        # get instance-queuenum map
        inst_queuenum_map[inst_num] = inst_queuenum_map.get(inst_num, 0) + 1

        # get instance-maxdelaytime map
        inst_maxdelay_map[inst_num] = inst_maxdelay_map.get(inst_num, 0)
        if delay > inst_maxdelay_map.get(inst_num):
            inst_maxdelay_map[inst_num] = delay
    
        # get instance-partner map
        inst_partner_map[inst_num] = inst_partner_map.get(inst_num, list())
        if not partner_id in inst_partner_map.get(inst_num):
            inst_partner_map.get(inst_num).append(partner_id)

        # get partner-maxdelay map
        partner_maxdelay_map[partner_id] = partner_maxdelay_map.get(partner_id, 0)
        if delay > partner_maxdelay_map.get(partner_id):
            partner_maxdelay_map[partner_id] = delay

        # get instance-queuenum map
        partner_queuenum_map[partner_id] = partner_queuenum_map.get(partner_id, 0) + 1

        # get partner-app map
        partner_app_map[partner_id] = partner_app_map.get(partner_id, list())
        if not app_id in partner_app_map.get(partner_id):
            partner_app_map.get(partner_id).append(app_id)

        # get app-maxdelay map
        app_maxdelay_map[app_id] = app_maxdelay_map.get(app_id, 0)
        if delay > app_maxdelay_map.get(app_id):
            app_maxdelay_map[app_id] = delay

        # get app-queuenum map
        app_queuenum_map[app_id] = app_queuenum_map.get(app_id, 0) + 1

        # get app-vfn map
        app_vfn_map[app_id] = app_vfn_map.get(app_id, list())
        app_vfn_map.get(app_id).append(vfn)

    return {
        'hostInst': host_inst_map,
        'instQnum': inst_queuenum_map,
        'instDelay': inst_maxdelay_map,
        'instPartner': inst_partner_map,
        'partnerDelay': partner_maxdelay_map,
        'partnerQnum': partner_queuenum_map,
        'partnerApp': partner_app_map,
        'appDelay': app_maxdelay_map,
        'appQnum': app_queuenum_map,
        'appVfn': app_vfn_map,
    }


if __name__ == "__main__":
    app.run(host='0.0.0.0')

