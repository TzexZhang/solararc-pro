"""
Solar Position Calculation Service
"""
from datetime import datetime, date, timedelta
from typing import Optional, List, Dict, Any
import pytz
import numpy as np

try:
    import pvlib
    from pvlib import solarposition
    PVLIB_AVAILABLE = True
except ImportError:
    PVLIB_AVAILABLE = False
    print("Warning: pvlib not available. Using simplified calculations.")


try:
    from astral import LocationInfo
    from astral.sun import sun
    ASTRAL_AVAILABLE = True
except ImportError:
    ASTRAL_AVAILABLE = False
    print("Warning: astral not available. Sunrise/sunset times may be inaccurate.")


def calculate_solar_position(
    lat: float,
    lng: float,
    date: Optional[str] = None,
    hour: Optional[int] = None,
    minute: Optional[int] = 0,
    timezone: str = "Asia/Shanghai"
) -> Dict[str, Any]:
    """
    Calculate solar position (altitude and azimuth angles)

    Args:
        lat: Latitude in degrees
        lng: Longitude in degrees
        date: Date string in YYYY-MM-DD format (default: today)
        hour: Hour (0-23, default: current hour)
        minute: Minute (0-59, default: 0)
        timezone: Timezone string (default: Asia/Shanghai)

    Returns:
        Dictionary containing solar position data
    """
    # Parse date
    if date:
        analysis_date = datetime.strptime(date, "%Y-%m-%d").date()
    else:
        analysis_date = date.today()

    # Set time
    if hour is None:
        now = datetime.now(pytz.timezone(timezone))
        hour = now.hour
        minute = now.minute

    # Create datetime object
    tz = pytz.timezone(timezone)
    analysis_time = tz.localize(datetime.combine(analysis_date, datetime.min.time()))
    analysis_time = analysis_time.replace(hour=hour, minute=minute)

    # Convert to UTC
    analysis_time_utc = analysis_time.astimezone(pytz.UTC)

    # Calculate solar position using pvlib
    if PVLIB_AVAILABLE:
        solpos = solarposition.get_solarposition(
            analysis_time_utc,
            lat,
            lng,
            altitude=0,
            pressure=101325,
            temperature=12,
            delta_t=67.0
        )

        # Extract values
        solar_altitude = float(solpos['elevation'].iloc[0])
        solar_azimuth = float(solpos['azimuth'].iloc[0])
        apparent_elevation = float(solpos['apparent_elevation'].iloc[0])
    else:
        # Simplified calculation (less accurate)
        # This is a fallback when pvlib is not available
        solar_altitude = _calculate_simplified_altitude(analysis_time, lat, lng)
        solar_azimuth = _calculate_simplified_azimuth(analysis_time, lat, lng)
        apparent_elevation = solar_altitude

    # Calculate sunrise/sunset times
    sunrise_time, sunset_time, day_length = get_sunrise_sunset(lat, lng, analysis_date, timezone)

    return {
        "solar_altitude": round(solar_altitude, 6),
        "solar_azimuth": round(solar_azimuth, 6),
        "apparent_elevation": round(apparent_elevation, 6),
        "sunrise_time": sunrise_time,
        "sunset_time": sunset_time,
        "day_length": day_length,
        "timestamp": analysis_time.isoformat()
    }


def calculate_daily_solar_positions(
    lat: float,
    lng: float,
    date: Optional[str] = None,
    timezone: str = "Asia/Shanghai"
) -> Dict[str, Any]:
    """
    Calculate solar positions for all 24 hours of a day

    Args:
        lat: Latitude in degrees
        lng: Longitude in degrees
        date: Date string in YYYY-MM-DD format (default: today)
        timezone: Timezone string (default: Asia/Shanghai)

    Returns:
        Dictionary containing hourly solar positions
    """
    # Parse date
    if date:
        analysis_date = datetime.strptime(date, "%Y-%m-%d").date()
    else:
        analysis_date = date.today()

    positions = []

    # Calculate for each hour
    for hour in range(24):
        pos = calculate_solar_position(lat, lng, date, hour, 0, timezone)
        positions.append({
            "hour": hour,
            "altitude": pos["solar_altitude"],
            "azimuth": pos["solar_azimuth"]
        })

    return {
        "date": analysis_date.isoformat(),
        "positions": positions
    }


def get_sunrise_sunset(
    lat: float,
    lng: float,
    date: Optional[date] = None,
    timezone: str = "Asia/Shanghai"
) -> tuple[Optional[str], Optional[str], Optional[float]]:
    """
    Get sunrise and sunset times

    Args:
        lat: Latitude in degrees
        lng: Longitude in degrees
        date: Date object (default: today)
        timezone: Timezone string (default: Asia/Shanghai)

    Returns:
        Tuple of (sunrise_time, sunset_time, day_length_hours)
    """
    if date is None:
        date = date.today()

    if ASTRAL_AVAILABLE:
        try:
            # Use astral for accurate sunrise/sunset
            location = LocationInfo(latitude=lat, longitude=lng)
            s = sun(location.observer, date=date, tzinfo=timezone)

            sunrise = s["sunrise"].strftime("%H:%M:%S")
            sunset = s["sunset"].strftime("%H:%M:%S")

            # Calculate day length
            day_length = (s["sunset"] - s["sunrise"]).total_seconds() / 3600

            return sunrise, sunset, round(day_length, 2)
        except Exception as e:
            print(f"Error calculating sunrise/sunset with astral: {e}")

    # Fallback to pvlib or simplified calculation
    try:
        if PVLIB_AVAILABLE:
            tz = pytz.timezone(timezone)
            # Calculate for the entire day
            times = tz.localize(datetime.combine(date, datetime.min.time())) + timedelta(hours=12)
            times_utc = times.astimezone(pytz.UTC)

            solpos = solarposition.get_sun_rise_set_transit(
                times_utc,
                lat,
                lng
            )

            sunrise = solpos['sunrise'].iloc[0]
            sunset = solpos['sunset'].iloc[0]

            if pd.notna(sunrise) and pd.notna(sunset):
                sunrise_local = sunrise.astimezone(tz)
                sunset_local = sunset.astimezone(tz)

                sunrise_str = sunrise_local.strftime("%H:%M:%S")
                sunset_str = sunset_local.strftime("%H:%M:%S")
                day_length = (sunset_local - sunrise_local).total_seconds() / 3600

                return sunrise_str, sunset_str, round(day_length, 2)
    except Exception as e:
        print(f"Error calculating sunrise/sunset with pvlib: {e}")

    # Ultimate fallback
    return None, None, None


def _calculate_simplified_altitude(dt: datetime, lat: float, lng: float) -> float:
    """
    Simplified solar altitude calculation (fallback)

    Args:
        dt: Datetime object
        lat: Latitude
        lng: Longitude

    Returns:
        Solar altitude angle in degrees
    """
    # This is a very simplified approximation
    # For accurate results, use pvlib

    # Day of year
    day_of_year = dt.timetuple().tm_yday

    # Declination angle (approximate)
    declination = 23.45 * np.sin(np.radians(360 / 365 * (day_of_year - 81)))

    # Hour angle
    hour_angle = 15 * (dt.hour - 12)

    # Latitude in radians
    lat_rad = np.radians(lat)
    dec_rad = np.radians(declination)
    hour_rad = np.radians(hour_angle)

    # Altitude angle
    altitude = np.arcsin(
        np.sin(lat_rad) * np.sin(dec_rad) +
        np.cos(lat_rad) * np.cos(dec_rad) * np.cos(hour_rad)
    )

    return np.degrees(altitude)


def _calculate_simplified_azimuth(dt: datetime, lat: float, lng: float) -> float:
    """
    Simplified solar azimuth calculation (fallback)

    Args:
        dt: Datetime object
        lat: Latitude
        lng: Longitude

    Returns:
        Solar azimuth angle in degrees
    """
    # This is a very simplified approximation
    # For accurate results, use pvlib

    # Day of year
    day_of_year = dt.timetuple().tm_yday

    # Declination angle
    declination = 23.45 * np.sin(np.radians(360 / 365 * (day_of_year - 81)))

    # Hour angle
    hour_angle = 15 * (dt.hour - 12)

    # Get altitude first
    altitude = _calculate_simplified_altitude(dt, lat, lng)
    altitude_rad = np.radians(altitude)

    # Calculate azimuth
    lat_rad = np.radians(lat)
    dec_rad = np.radians(declination)
    hour_rad = np.radians(hour_angle)

    if np.cos(altitude_rad) == 0:
        return 180.0

    azimuth = np.arcsin(
        -np.sin(hour_rad) * np.cos(dec_rad) / np.cos(altitude_rad)
    )

    azimuth_deg = np.degrees(azimuth)

    # Adjust quadrant
    if hour_angle > 0:
        azimuth_deg = 360 - azimuth_deg

    return azimuth_deg


# Import pandas for pvlib operations
try:
    import pandas as pd
except ImportError:
    # Create a dummy pd.notna if pandas not available
    class DummyPd:
        @staticmethod
        def notna(val):
            return val is not None
    pd = DummyPd()
