"""change specialty type to number

Revision ID: d4c1f2ae2a16
Revises: cd1ad9946317
Create Date: 2023-01-28 11:10:55.791964

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d4c1f2ae2a16"
down_revision = "cd1ad9946317"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("specialty", sa.Column("number", sa.String(), nullable=False))
    op.drop_column("specialty", "type")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "specialty",
        sa.Column("type", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.drop_column("specialty", "number")
    # ### end Alembic commands ###