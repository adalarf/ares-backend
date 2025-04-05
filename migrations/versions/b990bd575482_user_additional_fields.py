"""user additional fields

Revision ID: b990bd575482
Revises: 9d6623d45ffd
Create Date: 2025-04-05 12:49:35.128146

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b990bd575482'
down_revision: Union[str, None] = '9d6623d45ffd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    gender_enum = sa.Enum('male', 'female', name='genderenum')
    goal_enum = sa.Enum('weight_loss', 'muscle_gain', 'increase_activity', name='goalenum')
    activity_enum = sa.Enum('low', 'middle', 'high', name='activityenum')
    training_place_enum = sa.Enum('home', 'outside', 'mixed', name='trainingplaceenum')
    load_enum = sa.Enum('physical', 'intellegentive', name='loadenum')

    gender_enum.create(op.get_bind(), checkfirst=True)
    goal_enum.create(op.get_bind(), checkfirst=True)
    activity_enum.create(op.get_bind(), checkfirst=True)
    training_place_enum.create(op.get_bind(), checkfirst=True)
    load_enum.create(op.get_bind(), checkfirst=True)
    
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('gender', sa.Enum('male', 'female', name='genderenum'), nullable=True))
    op.add_column('users', sa.Column('goal', sa.Enum('weight_loss', 'muscle_gain', 'increase_activity', name='goalenum'), nullable=True))
    op.add_column('users', sa.Column('activity', sa.Enum('low', 'middle', 'high', name='activityenum'), nullable=True))
    op.add_column('users', sa.Column('weight', sa.Float(), nullable=True))
    op.add_column('users', sa.Column('height', sa.Float(), nullable=True))
    op.add_column('users', sa.Column('training_place', sa.Enum('home', 'outside', 'mixed', name='trainingplaceenum'), nullable=True))
    op.add_column('users', sa.Column('load', sa.Enum('physical', 'intellegentive', name='loadenum'), nullable=True))
    op.add_column('users', sa.Column('gems', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('expirience', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'expirience')
    op.drop_column('users', 'gems')
    op.drop_column('users', 'load')
    op.drop_column('users', 'training_place')
    op.drop_column('users', 'height')
    op.drop_column('users', 'weight')
    op.drop_column('users', 'activity')
    op.drop_column('users', 'goal')
    op.drop_column('users', 'gender')
    # ### end Alembic commands ###
