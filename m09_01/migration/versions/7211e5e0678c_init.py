"""Init

Revision ID: 7211e5e0678c
Revises: 
Create Date: 2022-09-11 16:05:24.456507

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7211e5e0678c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contacts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=120), nullable=False),
    sa.Column('last_name', sa.String(length=120), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('cell_phone', sa.String(length=100), nullable=False),
    sa.Column('address', sa.String(length=100), nullable=True),
    sa.Column('creation_date', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('note', sa.String(length=340), nullable=False),
    sa.Column('tag', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('contacts_to_notes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('contact_tag', sa.String(length=100), nullable=True),
    sa.Column('contact_id', sa.Integer(), nullable=True),
    sa.Column('note_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['contact_id'], ['contacts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['note_id'], ['notes.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('contacts_to_notes')
    op.drop_table('notes')
    op.drop_table('contacts')
    # ### end Alembic commands ###