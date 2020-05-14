from _datetime import datetime

from alembic import op
import sqlalchemy as sa

revision = "initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("body", sa.String(140), nullable=False),
        sa.Column("timestamp", sa.DateTime, index=True, default=datetime.utcnow),
        sa.Column("user_id", sa.Integer()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(64), nullable=False),
        sa.Column("posts", sa.String(64)),
        sa.Column("hash", sa.Binary(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["posts"], ["posts.id"]),
    )
    op.create_table(
        "likes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("timestamp", sa.DateTime, index=True, default=datetime.utcnow),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["post_id"], ["posts.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
    )
    op.create_table(
        "user_log_entries",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("timestamp", sa.DateTime, index=True, default=datetime.utcnow),
        sa.Column("user_id", sa.Integer(), nullable=False, index=True),
        sa.Column("url", sa.String),
        sa.Column("method", sa.String),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
    )


def downgrade():
    op.drop_table("posts")
    op.drop_table("users")
    op.drop_table("likes")
    op.drop_table("user_log_entries")
