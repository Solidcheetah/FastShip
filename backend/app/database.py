import sqlite3
from typing import Any

from app.api.schemas.shipment import ShipmentCreate, ShipmentUpdate


class Database:
    def connect_to_db(self):
        self.conn = sqlite3.connect("sqlite.db", check_same_thread=False)
        self.cur = self.conn.cursor()

    def create_table(self):
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS shipment (
                id INTEGER PRIMARY KEY,
                content TEXT,
                weight REAL,
                status TEXT
            )
        """
        )

    def create(self, shipment: ShipmentCreate) -> int:
        self.cur.execute("SELECT MAX(id) from shipment")
        result = self.cur.fetchone()

        new_id = result[0] + 1

        self.cur.execute(
            """
            INSERT INTO shipment
                        VALUES (:id, :content, :weight, :status)
        """,
            {"id": new_id, **shipment.model_dump(), "status": "placed"},
        )
        self.conn.commit()
        return new_id

    def get(self, id: int) -> dict[str, Any] | None:
        self.cur.execute(
            """select * from shipment
                          where id = ?
                        """,
            (id,),
        )
        row = self.cur.fetchone()

        return (
            {
                "id": row[0],
                "content": row[1],
                "weight": row[2],
                "status": row[3],
            }
            if row
            else None
        )

    def update(self, id: int, shipment: ShipmentUpdate):
        self.cur.execute(
            """
            UPDATE shipment set status = :status
            where id = :id
        """,
            {"id": id, **shipment.model_dump()},
        )
        self.conn.commit()
        return self.get(id)

    def delete(self, id: int):
        self.cur.execute(
            """
            Delete from shipment
            where id = ?
        """,
            (id,),
        )

        self.conn.commit()

    def close(self):
        self.conn.close()

    def __enter__(self):
        self.connect_to_db()
        self.create_table()
        return self


# # cursor.execute("""
# #     drop table shipment
# # """)
# # connection.commit()

# # Close the connection


# import sqlite3

# connection = sqlite3.connect("sqlite.db")
# cursor = connection.cursor()

# cursor.execute("""
#     INSERT INTO shipment
#     VALUES (12701, 'Cheap Vase', 10, 'placed')
# """)
# connection.commit()

# connection.close()
