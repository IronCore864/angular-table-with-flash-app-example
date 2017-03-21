import cx_Oracle

from zk_util import zk_get_dict

from common.settings import zk_path_test_db, zk_path_prod_db, USE_PROD_DB


def get_connection():
    db_conf_zk_path = zk_path_prod_db if USE_PROD_DB else zk_path_test_db
    db_conf = zk_get_dict(db_conf_zk_path)
    conn_str_tpl = '{user}/{pwd}@{host}:{port}/{sid}'
    conn_str = conn_str_tpl.format(user=db_conf['USER'],
                                   pwd=db_conf['PWD'],
                                   host=db_conf['HOST'],
                                   port=db_conf['PORT'],
                                   sid=db_conf['SID'])
    return cx_Oracle.connect(conn_str)
