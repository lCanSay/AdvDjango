"""Create quizzes and questions tables

Revision ID: e31727e36bae
Revises: 7aa9b484026f
Create Date: 2025-02-19 22:29:14.200922

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e31727e36bae'
down_revision: Union[str, None] = '7aa9b484026f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'quizzes',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('title', sa.String(255), nullable=False),
    )

    op.create_table(
        'questions',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('question_text', sa.String(500), nullable=False),
        sa.Column('quiz_id', sa.Integer, sa.ForeignKey('quizzes.id')),
    )

def downgrade() -> None:
    op.drop_table('questions')

    op.drop_table('quizzes')