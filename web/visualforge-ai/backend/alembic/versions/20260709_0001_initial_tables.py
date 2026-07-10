"""initial tables

Revision ID: 20260709_0001
Revises: 
Create Date: 2026-07-09
"""
from alembic import op
import sqlalchemy as sa


revision = "20260709_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "generations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("mode", sa.String(length=50), nullable=False),
        sa.Column("domain", sa.String(length=80), nullable=False),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("negative_prompt", sa.Text(), nullable=True),
        sa.Column("image_path", sa.Text(), nullable=True),
        sa.Column("image_url", sa.Text(), nullable=True),
        sa.Column("input_image_path", sa.Text(), nullable=True),
        sa.Column("mask_image_path", sa.Text(), nullable=True),
        sa.Column("seed", sa.Integer(), nullable=True),
        sa.Column("steps", sa.Integer(), nullable=True),
        sa.Column("guidance_scale", sa.Float(), nullable=True),
        sa.Column("strength", sa.Float(), nullable=True),
        sa.Column("width", sa.Integer(), nullable=True),
        sa.Column("height", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(length=40), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_generations_id"), "generations", ["id"], unique=False)
    op.create_index(op.f("ix_generations_mode"), "generations", ["mode"], unique=False)
    op.create_index(op.f("ix_generations_domain"), "generations", ["domain"], unique=False)
    op.create_index(op.f("ix_generations_status"), "generations", ["status"], unique=False)

    op.create_table(
        "uploaded_files",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("original_name", sa.String(length=255), nullable=False),
        sa.Column("file_path", sa.Text(), nullable=False),
        sa.Column("file_url", sa.Text(), nullable=False),
        sa.Column("file_type", sa.String(length=80), nullable=False),
        sa.Column("mime_type", sa.String(length=120), nullable=True),
        sa.Column("size_bytes", sa.BigInteger(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_uploaded_files_id"), "uploaded_files", ["id"], unique=False)

    op.create_table(
        "chat_messages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("session_id", sa.String(length=120), nullable=False),
        sa.Column("sender", sa.String(length=40), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("response", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_chat_messages_id"), "chat_messages", ["id"], unique=False)
    op.create_index(
        op.f("ix_chat_messages_session_id"),
        "chat_messages",
        ["session_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_chat_messages_session_id"), table_name="chat_messages")
    op.drop_index(op.f("ix_chat_messages_id"), table_name="chat_messages")
    op.drop_table("chat_messages")
    op.drop_index(op.f("ix_uploaded_files_id"), table_name="uploaded_files")
    op.drop_table("uploaded_files")
    op.drop_index(op.f("ix_generations_status"), table_name="generations")
    op.drop_index(op.f("ix_generations_domain"), table_name="generations")
    op.drop_index(op.f("ix_generations_mode"), table_name="generations")
    op.drop_index(op.f("ix_generations_id"), table_name="generations")
    op.drop_table("generations")
