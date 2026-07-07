"""baseline seller and shipment tables

Revision ID: 6f2b8a4d91e0
Revises:
Create Date: 2026-07-07 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = "6f2b8a4d91e0"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "seller",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("email", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("password_hash", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "shipment",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("content", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("weight", sa.Float(), nullable=False),
        sa.Column("destination", sa.Integer(), nullable=False),
        sa.Column("estimated_delivery", sa.DateTime(), nullable=False),
        sa.Column(
            "status",
            postgresql.ENUM(
                "placed",
                "in_transit",
                "out_for_delivery",
                "delivered",
                "cancelled",
                name="shipmentstatus",
            ),
            nullable=False,
        ),
        sa.Column("seller_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["seller_id"], ["seller.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("shipment")
    op.drop_table("seller")
