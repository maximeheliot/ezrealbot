from ezrealbot.utils import Base
from sqlalchemy import Column, Integer, String


class Guild(Base):
    __tablename__ = 'guilds'

    id = Column(Integer, primary_key=True)
    message = Column(String)