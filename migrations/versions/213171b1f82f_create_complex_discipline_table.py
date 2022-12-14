"""create complex_discipline table

Revision ID: 213171b1f82f
Revises: 5a98fe4d7ec5
Create Date: 2022-10-17 11:06:40.586482

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "213171b1f82f"
down_revision = "5a98fe4d7ec5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "complexdiscipline",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("complex_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("discipline_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(["complex_id"], ["complex.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["discipline_id"], ["discipline.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("complexdiscipline")
    # ### end Alembic commands ###
