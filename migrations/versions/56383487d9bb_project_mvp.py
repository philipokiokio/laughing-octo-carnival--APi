"""Project MVP

Revision ID: 56383487d9bb
Revises: 
Create Date: 2023-01-15 19:40:15.777562

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "56383487d9bb"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "projects",
        sa.Column("id", sa.Integer, nullable=False),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("api_key", sa.String(), nullable=False),
        sa.Column("data_center", sa.String(), nullable=True),
        sa.Column("mixpanel_key", sa.String(), nullable=True),
        sa.Column(
            "date_created", sa.TIMESTAMP(timezone=True), server_default=sa.text("NOW()")
        ),
        sa.Column(
            "date_updated", sa.TIMESTAMP(timezone=True), server_default=sa.text("NOW()")
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    pass


def downgrade() -> None:
    op.drop_table("projects")
    pass
