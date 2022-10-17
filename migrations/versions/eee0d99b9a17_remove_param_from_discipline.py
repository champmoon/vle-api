"""remove param from discipline

Revision ID: eee0d99b9a17
Revises: 51585717d351
Create Date: 2022-10-17 10:51:04.350365

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "eee0d99b9a17"
down_revision = "51585717d351"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("discipline", "param")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "discipline",
        sa.Column("param", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    # ### end Alembic commands ###