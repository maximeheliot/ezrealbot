from sqlalchemy.orm import relationship

from ezrealbot.utils import Base
from sqlalchemy import Column, Integer, DateTime


class Guild(Base):
    __tablename__ = 'guilds'

    discord_id = Column(Integer, primary_key=True)
    registration_date = Column(DateTime)
    members = relationship("Member", cascade="save-update, merge, delete")
