import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.data.models import MarketData

engine = create_engine("sqlite:///fx_data.db", echo=False)
SessionLocal = sessionmaker(bind=engine)

def get_eurusd_history(days: int = 300) -> pd.DataFrame:
    """Récupère l'historique EUR/USD depuis la base."""
    session = SessionLocal()
    rows = session.query(MarketData).filter(MarketData.pair == "EURUSD").order_by(MarketData.date).all()
    session.close()
    
    df = pd.DataFrame([{
        "date": r.date,
        "open": r.open,
        "high": r.high,
        "low": r.low,
        "close": r.close,
        "volume": r.volume
    } for r in rows])
    
    df = df.tail(days).reset_index(drop=True)
    return df

def calculate_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Calcule SMA, RSI, Bollinger Bands, ATR."""
    # SMA
    df["sma_50"] = df["close"].rolling(window=50).mean()
    df["sma_100"] = df["close"].rolling(window=100).mean()
    df["sma_200"] = df["close"].rolling(window=200).mean()
    
    # RSI 14
    delta = df["close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df["rsi_14"] = 100 - (100 / (1 + rs))
    
    # Bollinger Bands 20,2
    df["bb_middle"] = df["close"].rolling(window=20).mean()
    bb_std = df["close"].rolling(window=20).std()
    df["bb_upper"] = df["bb_middle"] + (bb_std * 2)
    df["bb_lower"] = df["bb_middle"] - (bb_std * 2)
    
    # ATR 14
    high_low = df["high"] - df["low"]
    high_close = np.abs(df["high"] - df["close"].shift())
    low_close = np.abs(df["low"] - df["close"].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    df["atr_14"] = true_range.rolling(window=14).mean()
    
    return df

def generate_technical_signal(df: pd.DataFrame) -> dict:
    """
    Règle de combinaison du CDC :
    - Tendance haussière (SMA50 > SMA100) + RSI entre 50-70 + pas suracheté → Fort Haussier
    - Tendance baissière (SMA50 < SMA100) + RSI entre 30-50 → Fort Baissier
    - Signaux contradictoires → Neutre
    """
    last = df.iloc[-1]
    
    # Vérifier qu'on a assez d'historique
    if pd.isna(last["sma_200"]):
        return {"signal": "INSUFFICIENT_DATA", "score": 0, "details": "Pas assez d'historique"}
    
    sma50 = last["sma_50"]
    sma100 = last["sma_100"]
    sma200 = last["sma_200"]
    rsi = last["rsi_14"]
    close = last["close"]
    
    # Déterminer la tendance
    trend_up = sma50 > sma100 > sma200
    trend_down = sma50 < sma100 < sma200
    
    # Déterminer le momentum
    momentum_bull = 50 < rsi < 70  # Haussier mais pas suracheté
    momentum_bear = 30 < rsi < 50  # Baissier mais pas survendu
    momentum_neutral = not (momentum_bull or momentum_bear)
    
    # Logique de combinaison
    if trend_up and momentum_bull:
        signal = "STRONG_BUY"
        score = +2
    elif trend_up and momentum_neutral:
        signal = "BUY"
        score = +1
    elif trend_down and momentum_bear:
        signal = "STRONG_SELL"
        score = -2
    elif trend_down and momentum_neutral:
        signal = "SELL"
        score = -1
    else:
        signal = "NEUTRAL"
        score = 0
    
    return {
        "signal": signal,
        "score": score,
        "details": {
            "sma_50": round(sma50, 4),
            "sma_100": round(sma100, 4),
            "sma_200": round(sma200, 4),
            "rsi_14": round(rsi, 2),
            "close": round(close, 4),
            "trend": "UP" if trend_up else "DOWN" if trend_down else "MIXED",
            "momentum": "BULL" if momentum_bull else "BEAR" if momentum_bear else "NEUTRAL"
        }
    }

def get_latest_technical_signal() -> dict:
    """Point d'entrée principal."""
    df = get_eurusd_history(days=300)
    df = calculate_technical_indicators(df)
    return generate_technical_signal(df)

if __name__ == "__main__":
    result = get_latest_technical_signal()
    print("📊 SIGNAL TECHNIQUE EUR/USD")
    print(f"Signal : {result['signal']}")
    print(f"Score  : {result['score']}")
    print(f"Détails : {result['details']}")