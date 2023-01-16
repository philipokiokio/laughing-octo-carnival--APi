"""Project rate limit and connection Orgs to projects

Revision ID: 255302eff303
Revises: 9d648bc9f85d
Create Date: 2023-01-16 16:16:07.903050

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "255302eff303"
down_revision = "9d648bc9f85d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("projects", sa.Column("org_id", sa.Integer(), nullable=True))

    op.add_column(
        "projects",
        sa.Column(
            "is_premium", sa.Boolean(), nullable=False, server_default=sa.text("false")
        ),
    )

    op.add_column(
        "projects",
        sa.Column("created_by", sa.Integer(), nullable=True),
    )

    op.create_foreign_key(
        "projects_org_id_fkey",
        "projects",
        "organization",
        ["org_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.create_foreign_key(
        "projects_created_by_fkey",
        "projects",
        "users",
        ["created_by"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_table(
        "project_rate_limit",
        sa.Column("id", sa.Integer),
        sa.Column("project_id", sa.Integer, nullable=False),
        sa.Column("count", sa.Integer, nullable=False),
        sa.Column(
            "date_created", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")
        ),
        sa.Column(
            "date_updated", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
    )
    pass


def downgrade() -> None:
    op.drop_constraint("projects_org_id_fkey", table_name="projects")
    op.drop_constraint("projects_created_by_fkey", table_name="projects")

    op.drop_column("projects", "org_id")
    op.drop_column("projects", "created_by")
    op.drop_column("projects", "is_premium")

    op.drop_constraint(
        "project_rate_limit_project_id_fkey", table_name="project_rate_limit"
    )
    op.drop_table("project_rate_limit")

    pass
