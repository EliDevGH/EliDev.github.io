import re
from datetime import datetime


def transform_string(value):
    value = value.strip()  # Remove trailing and leading whitespace
    if re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$', value):
        # Transform RFC3339 formatted string to Unix Epoch
        dt = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
        value = int(dt.timestamp())
    return value


def transform_number(value):
    value = value.strip()  # Remove trailing and leading whitespace
    value = value.lstrip('0')  # Strip leading zeros
    if '.' in value or 'e' in value or 'E' in value:
        # Float or scientific notation
        try:
            value = float(value)
        except ValueError:
            return None  # Invalid numeric value
    else:
        # Integer
        try:
            value = int(value)
        except ValueError:
            return None  # Invalid numeric value
    return value


def transform_boolean(value):
    value = value.strip()  # Remove trailing and leading whitespace
    if value.lower() in ['1', 't', 'true']:
        return True
    elif value.lower() in ['0', 'f', 'false']:
        return False
    return None  # Invalid boolean value


def transform_null(value):
    value = value.strip()  # Remove trailing and leading whitespace
    if value.lower() in ['1', 't', 'true']:
        return None
    return None  # Field should be omitted for other values


def transform_list(value):
    if isinstance(value, list):
        transformed_list = []
        for item in value:
            transformed_item = transform_value(item)
            if transformed_item is not None:
                transformed_list.append(transformed_item)
        if transformed_list:
            return transformed_list
    return None  # Field should be omitted for empty list or unsupported types


def transform_map(value):
    if isinstance(value, dict):
        transformed_map = {}
        for key, val in sorted(value.items()):
            transformed_val = transform_value(val)
            if transformed_val is not None:
                transformed_map[key] = transformed_val
        if transformed_map:
            return transformed_map
    return None  # Field should be omitted for empty map


def transform_value(value):
    if isinstance(value, dict):
        for key, val in value.items():
            if isinstance(val, dict) and len(val) == 1:
                for data_type, data_value in val.items():
                    if data_type == 'S':
                        return transform_string(data_value)
                    elif data_type == 'N':
                        return transform_number(data_value)
                    elif data_type == 'BOOL':
                        return transform_boolean(data_value)
                    elif data_type == 'NULL':
                        return transform_null(data_value)
            elif isinstance(val, list) and len(val) > 0:
                return transform_list(val)
            elif isinstance(val, dict) and len(val) > 0:
                return transform_map(val)
    return None  # Unsupported data type or invalid field
