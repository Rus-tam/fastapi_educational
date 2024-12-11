"""Second migration

Revision ID: fc39014756d2
Revises: 9da1568008d8
Create Date: 2024-12-11 17:54:53.619348

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fc39014756d2'
down_revision: Union[str, None] = '9da1568008d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    op.create_unique_constraint(None, 'users', ['phone_number'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'phone_number')
    # ### end Alembic commands ###
