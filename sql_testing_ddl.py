import sqlalchemy
from sqlalchemy.sql import text
import pymysql
from google.cloud.sql.connector import Connector, IPTypes


INSTANCE_CONNECTION_NAME = "molten-album-427115-q6:us-central1:oyster1"  # e.g. 'project:region:instance'
DB_USER = 'root'  # e.g. 'my-db-user'
DB_PASS = 'dbuserdbuser'  # e.g. 'my-db-password'
DB_NAME = 'test_4'  # e.g. 'my-database'

def connect_with_connector() -> sqlalchemy.engine.base.Engine:
    """
    Initializes a connection pool for a Cloud SQL instance of MySQL.

    Uses the Cloud SQL Python Connector package.
    """
    # Note: Saving credentials in environment variables is convenient, but not
    # secure - consider a more secure solution such as
    # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
    # keep secrets safe.


    ip_type = IPTypes.PUBLIC

    connector = Connector(ip_type)

    def getconn() -> pymysql.connections.Connection:
        conn: pymysql.connections.Connection = connector.connect(
            INSTANCE_CONNECTION_NAME,
            "pymysql",
            user=DB_USER,
            password=DB_PASS,
            db=DB_NAME,
        )
        return conn

    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn,
        # ...
    )
    return pool

en = connect_with_connector()

def run_sql(prompt: str, write = False):
    if write:
        st.write(prompt)
    with en.connect() as con:
        res = con.execute(text(prompt))
        
        if prompt.lower().find('select') == 0: # is a select statement            
            colnames_arr = list(res.keys())
            res_ls = [row for row in res]      
            pretty_dict = [ {colnames_arr[i] : res_ls[j][i] for i in range(len(colnames_arr))} for j in range(len(res_ls)) ]
            return pretty_dict
        else:
            con.commit()

