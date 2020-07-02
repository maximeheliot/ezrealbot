from sqlalchemy.orm import relationship

from ezrealbot.utils import Base
from sqlalchemy import Column, Integer, String, Table, ForeignKey


class Guild(Base):
    __tablename__ = 'guilds'

    discord_id = Column(Integer, primary_key=True)
