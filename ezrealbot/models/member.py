from sqlalchemy.orm import relationship

from ezrealbot.utils import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime


class Member(Base):
    __tablename__ = 'members'

    discord_id = Column(Integer, primary_key=True)
    region = Column(Integer)
    summoner_id = Column(String)
    guild_id = Column(Integer, ForeignKey('guilds.discord_id'))
    registration_date = Column(DateTime)
