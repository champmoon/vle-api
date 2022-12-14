"""create theme_complex table

Revision ID: 6e0c011647df
Revises: d1ee67a1305d
Create Date: 2022-10-17 14:53:34.379646

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "6e0c011647df"
down_revision = "d1ee67a1305d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "themecomplex",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("theme_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("complex_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(["complex_id"], ["complex.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["theme_id"], ["theme.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("themecomplex")
    # ### end Alembic commands ###
