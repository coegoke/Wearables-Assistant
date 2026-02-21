"""Tools for querying wearables database."""
import sqlite3
from datetime import datetime
from typing import Optional
from pathlib import Path


def get_db_connection():
    """Create a database connection."""
    # Get the absolute path to wearables.db in project root
    current_dir = Path(__file__).resolve().parent
    db_path = current_dir / 'wearables.db'
    return sqlite3.connect(str(db_path))


def get_daily_steps(date: Optional[str] = None, days: int = 7) -> str:
    """
    Get daily step counts for a user.
    
    Args:
        date: Specific date in YYYY-MM-DD format. If None, uses today.
        days: Number of days to look back (default 7)
    
    Returns:
        String with step data
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if date:
        cursor.execute('''
            SELECT date, steps, distance_km, calories_burned, active_minutes
            FROM daily_metrics
            WHERE user_id = 1 AND date = ?
        ''', (date,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return f"On {result[0]}: {result[1]:,} steps, {result[2]} km distance, {result[3]} calories burned, {result[4]} active minutes"
        else:
            return f"No data found for {date}"
    else:
        cursor.execute('''
            SELECT date, steps, distance_km, calories_burned, active_minutes
            FROM daily_metrics
            WHERE user_id = 1
            ORDER BY date DESC
            LIMIT ?
        ''', (days,))
        results = cursor.fetchall()
        conn.close()
        
        if results:
            output = f"Step data for the last {days} days:\n"
            total_steps = 0
            for row in results:
                output += f"- {row[0]}: {row[1]:,} steps, {row[2]} km, {row[3]} calories, {row[4]} active min\n"
                total_steps += row[1]
            avg_steps = total_steps // len(results)
            output += f"\nAverage: {avg_steps:,} steps/day"
            return output
        else:
            return "No step data found"


def get_sleep_data(date: Optional[str] = None, days: int = 7) -> str:
    """
    Get sleep data for a user.
    
    Args:
        date: Specific date in YYYY-MM-DD format. If None, uses recent data.
        days: Number of days to look back (default 7)
    
    Returns:
        String with sleep data
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if date:
        cursor.execute('''
            SELECT date, total_sleep_hours, deep_sleep_hours, light_sleep_hours, 
                   rem_sleep_hours, awake_hours, sleep_score
            FROM sleep_data
            WHERE user_id = 1 AND date = ?
        ''', (date,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return (f"Sleep data for {result[0]}:\n"
                   f"- Total sleep: {result[1]:.1f} hours\n"
                   f"- Deep sleep: {result[2]:.1f} hours\n"
                   f"- Light sleep: {result[3]:.1f} hours\n"
                   f"- REM sleep: {result[4]:.1f} hours\n"
                   f"- Awake time: {result[5]:.1f} hours\n"
                   f"- Sleep score: {result[6]}/100")
        else:
            return f"No sleep data found for {date}"
    else:
        cursor.execute('''
            SELECT date, total_sleep_hours, deep_sleep_hours, rem_sleep_hours, sleep_score
            FROM sleep_data
            WHERE user_id = 1
            ORDER BY date DESC
            LIMIT ?
        ''', (days,))
        results = cursor.fetchall()
        conn.close()
        
        if results:
            output = f"Sleep data for the last {days} days:\n"
            total_sleep = 0
            total_deep = 0
            total_rem = 0
            total_score = 0
            
            for row in results:
                output += f"- {row[0]}: {row[1]:.1f}h total (Deep: {row[2]:.1f}h, REM: {row[3]:.1f}h) - Score: {row[4]}\n"
                total_sleep += row[1]
                total_deep += row[2]
                total_rem += row[3]
                total_score += row[4]
            
            avg_sleep = total_sleep / len(results)
            avg_score = total_score // len(results)
            output += f"\nAverages: {avg_sleep:.1f}h sleep/night, Score: {avg_score}/100"
            return output
        else:
            return "No sleep data found"


def get_heart_rate_data(date: Optional[str] = None) -> str:
    """
    Get heart rate data for a user.
    
    Args:
        date: Specific date in YYYY-MM-DD format. If None, uses today.
    
    Returns:
        String with heart rate data
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')
    
    cursor.execute('''
        SELECT timestamp, heart_rate, resting_heart_rate
        FROM heart_rate
        WHERE user_id = 1 AND date(timestamp) = ?
        ORDER BY timestamp
    ''', (date,))
    results = cursor.fetchall()
    conn.close()
    
    if results:
        heart_rates = [row[1] for row in results]
        avg_hr = sum(heart_rates) // len(heart_rates)
        max_hr = max(heart_rates)
        min_hr = min(heart_rates)
        resting_hr = results[0][2]
        
        output = f"Heart rate data for {date}:\n"
        output += f"- Resting heart rate: {resting_hr} bpm\n"
        output += f"- Average: {avg_hr} bpm\n"
        output += f"- Max: {max_hr} bpm\n"
        output += f"- Min: {min_hr} bpm\n"
        output += "\nReadings throughout the day:\n"
        for row in results[:8]:  # Show first 8 readings
            time = row[0].split()[1][:5]
            output += f"  {time}: {row[1]} bpm\n"
        
        return output
    else:
        return f"No heart rate data found for {date}"


def get_activity_history(days: int = 14, activity_type: Optional[str] = None) -> str:
    """
    Get activity/workout history for a user.
    
    Args:
        days: Number of days to look back (default 14)
        activity_type: Filter by specific activity type (e.g., 'Running', 'Cycling')
    
    Returns:
        String with activity data
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if activity_type:
        cursor.execute('''
            SELECT date, activity_type, duration_minutes, calories, 
                   average_heart_rate, max_heart_rate, distance_km
            FROM activities
            WHERE user_id = 1 AND activity_type LIKE ?
            ORDER BY date DESC
            LIMIT 20
        ''', (f'%{activity_type}%',))
    else:
        cursor.execute('''
            SELECT date, activity_type, duration_minutes, calories, 
                   average_heart_rate, max_heart_rate, distance_km
            FROM activities
            WHERE user_id = 1 AND date >= date('now', ?)
            ORDER BY date DESC
        ''', (f'-{days} days',))
    
    results = cursor.fetchall()
    conn.close()
    
    if results:
        output = f"Activity history (last {days} days):\n\n"
        total_duration = 0
        total_calories = 0
        
        for row in results:
            distance_str = f", {row[6]} km" if row[6] > 0 else ""
            output += (f"- {row[0]}: {row[1]}\n"
                      f"  Duration: {row[2]} min, Calories: {row[3]}, "
                      f"Avg HR: {row[4]} bpm, Max HR: {row[5]} bpm{distance_str}\n")
            total_duration += row[2]
            total_calories += row[3]
        
        output += f"\nTotal: {len(results)} activities, {total_duration} minutes, {total_calories} calories"
        return output
    else:
        filter_msg = f" for {activity_type}" if activity_type else ""
        return f"No activities found{filter_msg}"


def get_weekly_summary() -> str:
    """
    Get a comprehensive weekly summary of all metrics.
    
    Returns:
        String with weekly summary
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Steps summary
    cursor.execute('''
        SELECT AVG(steps), SUM(steps), AVG(calories_burned), AVG(active_minutes)
        FROM daily_metrics
        WHERE user_id = 1 AND date >= date('now', '-7 days')
    ''')
    steps_data = cursor.fetchone()
    
    # Sleep summary
    cursor.execute('''
        SELECT AVG(total_sleep_hours), AVG(deep_sleep_hours), 
               AVG(rem_sleep_hours), AVG(sleep_score)
        FROM sleep_data
        WHERE user_id = 1 AND date >= date('now', '-7 days')
    ''')
    sleep_data = cursor.fetchone()
    
    # Activity summary
    cursor.execute('''
        SELECT COUNT(*), SUM(duration_minutes), SUM(calories)
        FROM activities
        WHERE user_id = 1 AND date >= date('now', '-7 days')
    ''')
    activity_data = cursor.fetchone()
    
    conn.close()
    
    output = "📊 WEEKLY SUMMARY (Last 7 Days)\n"
    output += "=" * 50 + "\n\n"
    
    output += "🚶 ACTIVITY:\n"
    if steps_data[0]:
        output += f"  • Average steps: {int(steps_data[0]):,} steps/day\n"
        output += f"  • Total steps: {int(steps_data[1]):,} steps\n"
        output += f"  • Average calories: {int(steps_data[2])} cal/day\n"
        output += f"  • Average active time: {int(steps_data[3])} min/day\n\n"
    
    output += "😴 SLEEP:\n"
    if sleep_data[0]:
        output += f"  • Average sleep: {sleep_data[0]:.1f} hours/night\n"
        output += f"  • Average deep sleep: {sleep_data[1]:.1f} hours\n"
        output += f"  • Average REM sleep: {sleep_data[2]:.1f} hours\n"
        output += f"  • Average sleep score: {int(sleep_data[3])}/100\n\n"
    
    output += "💪 WORKOUTS:\n"
    if activity_data[0] and activity_data[0] > 0:
        output += f"  • Total workouts: {activity_data[0]}\n"
        output += f"  • Total workout time: {activity_data[1]} minutes\n"
        output += f"  • Total calories burned: {activity_data[2]}\n"
    else:
        output += "  • No recorded workouts this week\n"
    
    return output


def get_device_info() -> str:
    """
    Get information about the user's wearable device.
    
    Returns:
        String with device information
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT d.device_type, d.brand, d.model, d.purchase_date,
               u.name, u.age, u.gender, u.height_cm, u.weight_kg
        FROM devices d
        JOIN users u ON d.user_id = u.user_id
        WHERE d.user_id = 1
    ''')
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return (f"👤 User: {result[4]} ({result[5]} years old, {result[6]})\n"
                f"📏 Height: {result[7]} cm, Weight: {result[8]} kg\n\n"
                f"⌚ Device Information:\n"
                f"  • Type: {result[0]}\n"
                f"  • Brand: {result[1]}\n"
                f"  • Model: {result[2]}\n"
                f"  • Purchase Date: {result[3]}")
    else:
        return "No device information found"


def search_data_by_date_range(start_date: str, end_date: str, metric_type: str = "steps") -> str:
    """
    Search for data within a specific date range.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        metric_type: Type of metric to retrieve (steps, sleep, activities)
    
    Returns:
        String with requested data
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if metric_type.lower() == "steps":
        cursor.execute('''
            SELECT date, steps, distance_km, calories_burned
            FROM daily_metrics
            WHERE user_id = 1 AND date BETWEEN ? AND ?
            ORDER BY date
        ''', (start_date, end_date))
        results = cursor.fetchall()
        
        if results:
            output = f"Steps data from {start_date} to {end_date}:\n"
            total_steps = 0
            for row in results:
                output += f"- {row[0]}: {row[1]:,} steps, {row[2]} km, {row[3]} cal\n"
                total_steps += row[1]
            output += f"\nTotal steps: {total_steps:,}"
            return output
    
    elif metric_type.lower() == "sleep":
        cursor.execute('''
            SELECT date, total_sleep_hours, sleep_score
            FROM sleep_data
            WHERE user_id = 1 AND date BETWEEN ? AND ?
            ORDER BY date
        ''', (start_date, end_date))
        results = cursor.fetchall()
        
        if results:
            output = f"Sleep data from {start_date} to {end_date}:\n"
            for row in results:
                output += f"- {row[0]}: {row[1]:.1f} hours, Score: {row[2]}/100\n"
            return output
    
    conn.close()
    return f"No {metric_type} data found for the specified date range"
