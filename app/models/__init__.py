from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.config import get_secret, MYSQL_DB_URL
from sqlalchemy.ext.declarative import declarative_base

class MySQLDB:

    MYSQL_URL = MYSQL_DB_URL  # MySQL Connection URL
    MYSQL_MAX_CONNECTIONS = int(get_secret("MYSQL_MAX_CONNECTIONS", "10"))  # Max connections
    MYSQL_POOL_SIZE = int(get_secret("MYSQL_POOL_SIZE", "5"))  # Pool size

    def __init__(self) -> None:
        self.__engine = None  # Database engine
        self.__session_local = None  # Session maker

    @property
    def engine(self):
        return self.__engine

    @property
    def session_local(self):
        return self.__session_local

    def connect(self):
        """
        Connect to MySQL
        """
        # Create the database engine with pooling and connection limits
        self.__engine = create_async_engine(
            self.MYSQL_URL,
            echo=True,  # Print SQL queries (useful for debugging)
            future=True,  # Use the latest SQLAlchemy API
            pool_size=self.MYSQL_POOL_SIZE,  # Connection pool size
            max_overflow=self.MYSQL_MAX_CONNECTIONS - self.MYSQL_POOL_SIZE,  # Extra connections beyond pool size
        )

        # Create a session maker for database operations
        self.__session_local = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.__engine,
            class_=AsyncSession,  # Use asynchronous sessions
        )

    async def close(self):
        """
        Close MySQL connection
        """
        if self.__engine:
            await self.__engine.dispose()

Base = declarative_base()
mysql_db = MySQLDB()
