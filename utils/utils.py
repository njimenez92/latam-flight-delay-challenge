from datetime import datetime
import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def get_period_day(date: str) -> str:
    """
    Classify the time of day into 'mañana', 'tarde', or 'noche'.
    """
    if isinstance(date, pd.Timestamp):
        date = date.strftime('%Y-%m-%d %H:%M:%S')
    try:
        date_time = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').time()
        morning_min = datetime.strptime("05:00", '%H:%M').time()
        morning_max = datetime.strptime("11:59", '%H:%M').time()
        afternoon_min = datetime.strptime("12:00", '%H:%M').time()
        afternoon_max = datetime.strptime("18:59", '%H:%M').time()
        evening_min = datetime.strptime("19:00", '%H:%M').time()
        evening_max = datetime.strptime("23:59", '%H:%M').time()
        night_min = datetime.strptime("00:00", '%H:%M').time()
        night_max = datetime.strptime("04:59", '%H:%M').time()
        
        if morning_min <= date_time <= morning_max:
            return 'mañana'
        elif afternoon_min <= date_time <= afternoon_max:
            return 'tarde'
        elif evening_min <= date_time <= evening_max or night_min <= date_time <= night_max:
            return 'noche'
        return 'desconocido'
    except Exception as e:
        logger.error(f"Error in get_period_day with date: {date} - {e}")
        return 'error'

def is_high_season(fecha: str) -> int:
    """
    Determine if a date is in the high season.
    """
    try:
        fecha_año = int(fecha.split('-')[0])
        fecha = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
        range1_min = datetime.strptime('15-Dec', '%d-%b').replace(year=fecha_año)
        range1_max = datetime.strptime('31-Dec', '%d-%b').replace(year=fecha_año)
        range2_min = datetime.strptime('1-Jan', '%d-%b').replace(year=fecha_año)
        range2_max = datetime.strptime('3-Mar', '%d-%b').replace(year=fecha_año)
        range3_min = datetime.strptime('15-Jul', '%d-%b').replace(year=fecha_año)
        range3_max = datetime.strptime('31-Jul', '%d-%b').replace(year=fecha_año)
        range4_min = datetime.strptime('11-Sep', '%d-%b').replace(year=fecha_año)
        range4_max = datetime.strptime('30-Sep', '%d-%b').replace(year=fecha_año)
        
        if ((range1_min <= fecha <= range1_max) or 
            (range2_min <= fecha <= range2_max) or 
            (range3_min <= fecha <= range3_max) or
            (range4_min <= fecha <= range4_max)):
            return 1
        return 0
    except Exception as e:
        logger.error(f"Error in is_high_season with date: {fecha} - {e}")
        return 0

def get_min_diff(row: pd.Series) -> float:
    """
    Calculate the difference in minutes between two datetime columns.
    """
    try:
        fecha_o = datetime.strptime(row['Fecha-O'], '%Y-%m-%d %H:%M:%S')
        fecha_i = datetime.strptime(row['Fecha-I'], '%Y-%m-%d %H:%M:%S')
        return (fecha_o - fecha_i).total_seconds() / 60
    except Exception as e:
        logger.error(f"Error in get_min_diff with row: {row.to_dict()} - {e}")
        return 0.0

def delay(min_diff: float, threshold: int = 15) -> int:
    """
    Determine if a flight is delayed based on a time threshold.
    """
    try:
        return 1 if min_diff > threshold else 0
    except Exception as e:
        logger.error(f"Error in delay with min_diff: {min_diff}, threshold: {threshold} - {e}")
        return 0
