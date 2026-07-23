from sqlalchemy import create_engine, Column, Integer, String, Float, Date, DateTime, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class MarketData(Base):
    __tablename__ = "market_data"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    pair = Column(String(10), nullable=False)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    
    __table_args__ = (UniqueConstraint('date', 'pair', name='uix_market_date_pair'),)

class FXFixingTND(Base):
    __tablename__ = "fx_fixing_tnd"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True, nullable=False)
    eur_tnd = Column(Float, nullable=False)
    usd_tnd = Column(Float, nullable=False)
    source = Column(String(20), default="scraping")

class MacroIndicator(Base):
    __tablename__ = "macro_indicators"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    country = Column(String(10), nullable=False)
    indicator = Column(String(50), nullable=False)
    value = Column(Float, nullable=False)
    frequency = Column(String(20))
    
    __table_args__ = (UniqueConstraint('date', 'country', 'indicator', name='uix_macro'),)

class ClientExposure(Base):
    __tablename__ = "client_exposures"
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), nullable=False)
    maturity_months = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False)
    budget_rate = Column(Float, nullable=False)
    flow_type = Column(String(20), nullable=False)
    coverage_result = Column(String(500), nullable=True)

class CoverageBand(Base):
    __tablename__ = "coverage_bands"
    
    id = Column(Integer, primary_key=True, index=True)
    pair = Column(String(10), nullable=False)
    min_months = Column(Integer, nullable=False)
    max_months = Column(Integer, nullable=False)
    coverage_pct = Column(Float, nullable=False)
    band_lower = Column(Float, nullable=False)
    band_upper = Column(Float, nullable=False)

class TraderPosition(Base):
    __tablename__ = "trader_positions"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    currency = Column(String(10), nullable=False)
    net_amount = Column(Float, nullable=False)
    var_amount = Column(Float, nullable=True)
    limit_amount = Column(Float, nullable=False)