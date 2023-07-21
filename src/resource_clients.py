import os
import json
import boto3
import psycopg2
from src.utils import logger

class Wrapper:
    def __init__(self) -> None:
        self.region = os.environ["REGION"]

class SecretsManager(Wrapper):
    def __init__(self) -> None:
        super().__init__()
        logger(f"Initialized: SecretsManager")
        self.secret_arn=os.environ["SECRET_ARN"]
        self.secrets_client = boto3.client('secretsmanager', region_name=self.region)

    def get_db_secrets(self):
        """
        Used to retrive secrets stored in AWS Secrets Manager
        """
        logger(f"Getting Secrets")
        secret_response = self.secrets_client.get_secret_value(SecretId=self.secret_arn)
        logger(f"Got secrets")
        secret_data = secret_response['SecretString']
        secrets = json.loads(secret_data)
        return secrets

class PSQLClient(Wrapper):
    def __init__(self) -> None:
        super().__init__()
        logger(f"Running PSQLClient")
        self.sensordb = os.environ["DB_IDENTIFIER"]
        self.resourceArn = os.environ["DB_RESOURCE_ARN"]
        self.db_name = os.environ["DB_NAME"]
        secrets = SecretsManager().get_db_secrets()
        self.username = secrets["username"]
        self.password = secrets["password"]
        self.host = secrets["host"]
        self.port = secrets["port"]
        self.rds_client = boto3.client('rds-data', region_name=self.region)
        logger(f"host={self.host}, user={self.username}, password={self.password}, port={self.port}, dbname={self.db_name}")
        logger(f"Connecting to DB . . .")
    
    def build_connection(self):
        """
        Used to build connection with RDS: PSQL Database using psycopg2 client
        """
        self.conn = psycopg2.connect(host=self.host, user=self.username, password=self.password, port=self.port, dbname=self.db_name)
        self.cur = self.conn.cursor()
    
    def close_connection(self):
        """
        Used to close the connection already built with RDS: PSQL Database
        """
        self.conn.commit()
        self.cur.close()
        self.conn.close()
    
    def run_query(self, sql, values):
        """
        Used to run query on RDS: PSQL Database
        sql: SQL query used by psycopg2 client
        values: Substitue values of SQL query
        """
        self.build_connection()
        logger(f"Executing Query: {(sql, values)}")
        self.cur.execute(sql, values)
        logger(f"Executing Success!!!")
        self.close_connection()
        logger(f"Connection closed")

    def data_exists(self, sql, values):
        """
        Used to check if data exists in a table
        sql: SQL query used by psycopg2 client
        values: Substitue values of SQL query
        """

        self.build_connection()
        logger(f"Executing Query: {(sql, values)}")
        self.cur.execute(sql, values)
        logger(f"Executing Success!!!")
        exists = self.cur.fetchone()[0]
        self.close_connection()
        logger(f"Connection closed")
        return exists
    
    def select_query(self, sql, values):
        """
        Used to retrieve table records from the RDS: PSQL database
        sql: SQL query used by psycopg2 client
        values: Substitue values of SQL query
        """
        self.build_connection()
        logger(f"Executing Query: {(sql, values)}")
        logger(f"Executing Success!!!")
        self.cur.execute(sql, values)
        rows = self.cur.fetchall()
        self.close_connection()
        return rows



        
