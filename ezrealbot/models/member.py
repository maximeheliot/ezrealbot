from sqlalchemy.orm import relationship

from ezrealbot.utils import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime


class Member(Base):
    __tablename__ = 'members'

    id = Column(Integer, primary_key=True, nullable=False)
    discord_id = Column(Integer, nullable=False)
    region = Column(Integer)
    summoner_id = Column(String)
    guild_id = Column(Integer, ForeignKey('guilds.discord_id'), nullable=False)
    guild = relationship("Guild", back_populates="members")
    registration_date = Column(DateTime)
