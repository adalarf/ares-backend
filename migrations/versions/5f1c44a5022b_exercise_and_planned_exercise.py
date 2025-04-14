"""exercise and planned exercise

Revision ID: 5f1c44a5022b
Revises: 82ce7c268edd
Create Date: 2025-04-14 16:52:54.125887

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f1c44a5022b'
down_revision: Union[str, None] = '82ce7c268edd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('exercises', sa.Column('sets_number_default', sa.Integer(), nullable=False))
    op.add_column('exercises', sa.Column('repetitions_default', sa.Integer(), nullable=False))
    op.add_column('exercises', sa.Column('gems_default', sa.Integer(), nullable=False))
    op.add_column('exercises', sa.Column('expirience_level_default', sa.String(), nullable=False))
    op.drop_column('exercises', 'gems')
    op.drop_column('exercises', 'expirience_level')
    op.drop_column('exercises', 'repetitions')
    op.drop_column('exercises', 'sets_number')
    op.add_column('planned_exercises', sa.Column('sets_number', sa.Integer(), nullable=False))
    op.add_column('planned_exercises', sa.Column('repetitions', sa.Integer(), nullable=False))
    op.add_column('planned_exercises', sa.Column('gems', sa.Integer(), nullable=False))
    op.add_column('planned_exercises', sa.Column('expirience_level', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('planned_exercises', 'expirience_level')
    op.drop_column('planned_exercises', 'gems')
    op.drop_column('planned_exercises', 'repetitions')
    op.drop_column('planned_exercises', 'sets_number')
    op.add_column('exercises', sa.Column('sets_number', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('exercises', sa.Column('repetitions', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('exercises', sa.Column('expirience_level', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('exercises', sa.Column('gems', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('exercises', 'expirience_level_default')
    op.drop_column('exercises', 'gems_default')
    op.drop_column('exercises', 'repetitions_default')
    op.drop_column('exercises', 'sets_number_default')
    # ### end Alembic commands ###
