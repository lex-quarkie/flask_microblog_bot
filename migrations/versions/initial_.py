"""empty message

Revision ID: initial
Create Date: 2020-12-18 14:34:24.643328

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
        sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('users_id_seq'::regclass)"), autoincrement=True, nullable=False),
        sa.Column('username', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
        sa.Column('hash', postgresql.BYTEA(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint('id', name='users_pkey'),
        postgresql_ignore_search_path=False
        )
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    op.create_table('posts',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('body', sa.VARCHAR(length=1000), autoincrement=False, nullable=False),
        sa.Column('timestamp', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
        sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='posts_user_id_fkey'),
        sa.PrimaryKeyConstraint('id', name='posts_pkey')
        )
    op.create_index('ix_posts_timestamp', 'posts', ['timestamp'], unique=False)
    op.create_table('user_log_entries',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('timestamp', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
        sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column('method', sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column('url', sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='user_log_entries_user_id_fkey'),
        sa.PrimaryKeyConstraint('id', name='user_log_entries_pkey')
        )
    op.create_index('ix_user_log_entries_url', 'user_log_entries', ['url'], unique=False)
    op.create_index('ix_user_log_entries_timestamp', 'user_log_entries', ['timestamp'], unique=False)
    op.create_table('likes',
                    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column('post_id', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column('timestamp', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
                    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name='likes_post_id_fkey'),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='likes_user_id_fkey'),
                    sa.PrimaryKeyConstraint('id', name='likes_pkey'),
                    )
    op.create_index('ix_likes_timestamp', 'likes', ['timestamp'], unique=False)

def downgrade():
    op.drop_index('ix_user_log_entries_timestamp', table_name='user_log_entries')
    op.drop_index('ix_user_log_entries_url', table_name='user_log_entries')
    op.drop_table('user_log_entries')
    op.drop_index('ix_posts_timestamp', table_name='posts')
    op.drop_table('posts')
    op.drop_index('ix_users_username', table_name='users')
    op.drop_table('users')
    op.drop_index('ix_likes_timestamp', table_name='likes')
    op.drop_table('likes')
    # ### end Alembic commands ###
