import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime


def safe_parse_datetime(timestamp_str):
    if timestamp_str is None:
        return None
    try:
        return datetime.strptime(timestamp_str, '%d-%m-%Y %H:%M:%S')
    except ValueError:
        return None


def parse_glucose_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    glucose_events = []
    glucose_node = root.find('glucose_level')
    
    if glucose_node is not None:
        for event in glucose_node.findall('event'):
            ts = event.get('ts')
            value = event.get('value')
            
            if ts is None or value is None:
                continue
                
            dt = safe_parse_datetime(ts)
            if dt is None:
                continue
            
            glucose_events.append({
                'timestamp': dt,
                'glucose': float(value)
            })
    
    df = pd.DataFrame(glucose_events)
    return df.sort_values('timestamp').reset_index(drop=True) if not df.empty else df


def parse_meal_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    meal_events = []
    meal_node = root.find('meal')
    
    if meal_node is not None:
        for event in meal_node.findall('event'):
            ts = event.get('ts')
            meal_type = event.get('type')
            carbs = event.get('carbs')
            
            if ts is None or carbs is None:
                continue
            
            dt = safe_parse_datetime(ts)
            if dt is None:
                continue
            
            meal_events.append({
                'timestamp': dt,
                'meal_type': meal_type if meal_type else 'unknown',
                'carbs': float(carbs)
            })
    
    df = pd.DataFrame(meal_events)
    return df.sort_values('timestamp').reset_index(drop=True) if not df.empty else df


def parse_bolus_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    bolus_events = []
    bolus_node = root.find('bolus')
    
    if bolus_node is not None:
        for event in bolus_node.findall('event'):
            ts = event.get('ts_begin')
            dose = event.get('dose')
            
            if ts is None or dose is None:
                continue
            
            dt = safe_parse_datetime(ts)
            if dt is None:
                continue
            
            bolus_events.append({
                'timestamp': dt,
                'bolus_dose': float(dose),
                'bolus_type': event.get('type', 'unknown'),
                'carb_input': float(event.get('bwz_carb_input', 0))
            })
    
    df = pd.DataFrame(bolus_events)
    return df.sort_values('timestamp').reset_index(drop=True) if not df.empty else df


def parse_basal_xml(file_path):
    """Extract basal insulin rate events from XML"""
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    basal_events = []
    basal_node = root.find('basal')
    
    if basal_node is not None:
        for event in basal_node.findall('event'):
            ts = event.get('ts')
            value = event.get('value')
            
            if ts is None or value is None:
                continue
            
            dt = safe_parse_datetime(ts)
            if dt is None:
                continue
            
            basal_events.append({
                'timestamp': dt,
                'basal_rate': float(value)
            })
    
    df = pd.DataFrame(basal_events)
    return df.sort_values('timestamp').reset_index(drop=True) if not df.empty else df


def parse_exercise_xml(file_path):
    """Extract exercise events from XML"""
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    exercise_events = []
    exercise_node = root.find('exercise')
    
    if exercise_node is not None:
        for event in exercise_node.findall('event'):
            ts = event.get('ts')
            
            if ts is None:
                continue
            
            dt = safe_parse_datetime(ts)
            if dt is None:
                continue
            
            exercise_events.append({
                'timestamp': dt,
                'exercise_intensity': event.get('intensity', 'unknown'),
                'exercise_duration': float(event.get('duration', 0))
            })
    
    df = pd.DataFrame(exercise_events)
    return df.sort_values('timestamp').reset_index(drop=True) if not df.empty else df


def parse_sleep_xml(file_path):
    """Extract sleep events from XML"""
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    sleep_events = []
    sleep_node = root.find('sleep')
    
    if sleep_node is not None:
        for event in sleep_node.findall('event'):
            ts = event.get('ts')
            
            if ts is None:
                continue
            
            dt = safe_parse_datetime(ts)
            if dt is None:
                continue
            
            sleep_events.append({
                'timestamp': dt,
                'sleep_quality': event.get('quality', 'unknown')
            })
    
    df = pd.DataFrame(sleep_events)
    return df.sort_values('timestamp').reset_index(drop=True) if not df.empty else df


def parse_single_xml(file_path):
    """
    Parse a single XML file and extract all data types.
    Returns a dictionary with DataFrames for each data type.
    """
    return {
        'glucose': parse_glucose_xml(file_path),
        'meals': parse_meal_xml(file_path),
        'bolus': parse_bolus_xml(file_path),
        'basal': parse_basal_xml(file_path),
        'exercise': parse_exercise_xml(file_path),
        'sleep': parse_sleep_xml(file_path)
    }
