# =============================================================================#
# -------------------------------- Database ----------------------------------#
# =============================================================================#

import uuid
from datetime import datetime
from typing import List, Dict, Any

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    select,
)

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)

from sqlalchemy.orm import (
    declarative_base,
    relationship,
)


# ============================================================
# Database Configuration
# ============================================================

DATABASE_FILE = "chatbot_production_memory.db"

DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_FILE}"


engine = create_async_engine(
    DATABASE_URL,
    echo=False,
)


SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


Base = declarative_base()


# ============================================================
# User Table
# ============================================================

class User(Base):

    __tablename__ = "users"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    username = Column(
        String,
        nullable=False,
        unique=True
    )

    email = Column(
        String,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    threads = relationship(
        "UserThread",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    memories = relationship(
        "LongTermMemory",
        back_populates="user",
        cascade="all, delete-orphan"
    )


# ============================================================
# User Threads Table
# ============================================================

class UserThread(Base):

    __tablename__ = "user_threads"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id = Column(
        String,
        ForeignKey("users.id"),
        nullable=False
    )

    thread_id = Column(
        String,
        nullable=False,
        unique=True,
        default=lambda: str(uuid.uuid4())
    )

    chat_title = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    user = relationship(
        "User",
        back_populates="threads"
    )


# ============================================================
# Long Term Memory Table
# ============================================================

class LongTermMemory(Base):

    __tablename__ = "long_term_memories"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id = Column(
        String,
        ForeignKey("users.id"),
        nullable=False
    )

    memory_key = Column(
        String,
        nullable=False
    )

    memory_value = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    user = relationship(
        "User",
        back_populates="memories"
    )


# ============================================================
# Initialize Database
# ============================================================

async def init_database():

    async with engine.begin() as conn:

        await conn.run_sync(
            Base.metadata.create_all
        )

    print("Database initialized successfully.")


# ============================================================
# Create User
# ============================================================

async def create_user(
    username: str,
    email: str | None = None
):

    async with SessionLocal() as db:

        user = User(
            username=username,
            email=email
        )

        db.add(user)

        await db.commit()
        await db.refresh(user)

        return user.id

# ============================================================
# Get Or Create User
# ============================================================

async def get_or_create_user(
    username: str,
    email: str | None = None
):

    async with SessionLocal() as db:

        result = await db.execute(
            select(User)
            .where(
                User.username == username
            )
        )

        user = result.scalar_one_or_none()

        if user:
            return user.id

        user = User(
            username=username,
            email=email
        )

        db.add(user)

        await db.commit()
        await db.refresh(user)

        return user.id

        
# ============================================================
# Create New Thread
# ============================================================

async def create_new_sidebar_thread(
    user_id: str,
    title: str
):

    async with SessionLocal() as db:

        thread = UserThread(
            user_id=user_id,
            chat_title=title
        )

        db.add(thread)

        await db.commit()
        await db.refresh(thread)

        return thread.thread_id


# ============================================================
# Update Thread Title
# ============================================================

async def update_thread_title(
    thread_id: str,
    title: str
):

    async with SessionLocal() as db:

        result = await db.execute(
            select(UserThread)
            .where(
                UserThread.thread_id == thread_id
            )
        )

        thread = result.scalar_one_or_none()

        if thread:

            thread.chat_title = title

            await db.commit()

            return True

        return False


# ============================================================
# Get User Sidebar History
# ============================================================

async def get_user_sidebar_history(
    user_id: str
) -> List[Dict[str, Any]]:

    async with SessionLocal() as db:

        result = await db.execute(
            select(UserThread)
            .where(UserThread.user_id == user_id)
            .order_by(UserThread.created_at.desc())
        )

        threads = result.scalars().all()

        return [
            {
                "thread_id": thread.thread_id,
                "title": thread.chat_title,
                "created_at": thread.created_at
            }
            for thread in threads
        ]


# ============================================================
# Save / Update User Preference
# ============================================================

async def save_user_preference(
    user_id: str,
    key: str,
    value: str
):

    async with SessionLocal() as db:

        result = await db.execute(
            select(LongTermMemory)
            .where(
                LongTermMemory.user_id == user_id,
                LongTermMemory.memory_key == key
            )
        )

        memory = result.scalar_one_or_none()

        if memory:

            memory.memory_value = value

        else:

            memory = LongTermMemory(
                user_id=user_id,
                memory_key=key,
                memory_value=value
            )

            db.add(memory)

        await db.commit()

        return True


# ============================================================
# Recall User Preference
# ============================================================

async def recall_user_preference(
    user_id: str,
    query_key: str
):

    async with SessionLocal() as db:

        result = await db.execute(
            select(LongTermMemory)
            .where(
                LongTermMemory.user_id == user_id,
                LongTermMemory.memory_key.like(
                    f"%{query_key}%"
                )
            )
        )

        memory = result.scalar_one_or_none()

        if memory:

            return (
                f"{memory.memory_key} -> "
                f"{memory.memory_value}"
            )

        return None