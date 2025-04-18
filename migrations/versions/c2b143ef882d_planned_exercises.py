"""planned exercises

Revision ID: c2b143ef882d
Revises: f0fe8c35db83
Create Date: 2025-04-14 22:27:45.344206

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2b143ef882d'
down_revision: Union[str, None] = 'f0fe8c35db83'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planned_exercises',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sets_number', sa.Integer(), nullable=False),
    sa.Column('repetitions', sa.Integer(), nullable=False),
    sa.Column('gems', sa.Integer(), nullable=False),
    sa.Column('expirience', sa.Integer(), nullable=False),
    sa.Column('workout_day_id', sa.Integer(), nullable=False),
    sa.Column('exercise_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['exercise_id'], ['exercises.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['workout_day_id'], ['workout_days.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_planned_exercises_id'), 'planned_exercises', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_planned_exercises_id'), table_name='planned_exercises')
    op.drop_table('planned_exercises')
    # ### end Alembic commands ###
