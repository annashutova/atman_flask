import json
from psycopg2 import connect
from psycopg2.sql import Literal, SQL
from psycopg2.extras import RealDictCursor
from os import getenv
from dotenv import load_dotenv
from datetime import datetime
import uuid

load_dotenv()

db_connection = {
    'password': getenv('PG_PASSWORD'),
    'database': getenv('PG_DBNAME'),
    'user': getenv('PG_USER'),
    'host': '127.0.0.1',
    'port': getenv('PG_PORT')
}


def create_db_connection():
    conn = connect(**db_connection, cursor_factory=RealDictCursor)
    conn.autocommit = True
    return conn

def insert_white_paper_products():
    with open('mock_white_paper.json', 'r') as file:
        data = json.load(file)

    with create_db_connection() as conn, conn.cursor() as cur:
        for entry in data:
            id_ = str(uuid.uuid4())
            title = entry['title']
            desc = entry['desc']
            price = entry['price']
            stock = entry['stock']
            category_id = '08b7bdab-0c4a-4289-bc60-d7077732d228' # использовать uuid категории <Белая бумага>
            created_at = datetime.utcnow()
            modified_at = datetime.utcnow()

            insert_query = SQL("""
                INSERT INTO product (id, title, "desc", price, stock, category_id, created_at, modified_at)
                VALUES ({}, {}, {}, {}, {}, {}, {}, {});
                """)

            cur.execute(insert_query.format(
                Literal(id_),
                Literal(title),
                Literal(desc),
                Literal(price),
                Literal(stock),
                Literal(category_id),
                Literal(created_at),
                Literal(modified_at),)
            )


if __name__ == '__main__':
    insert_white_paper_products()
