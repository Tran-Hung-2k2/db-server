def validate_config(config):
    required_fields = [
        "COLUMN",
        "UUID"
    ]

    optional_fields = []

    errors = []

    # Check for required fields
    for field in required_fields:
        if field not in config:
            errors.append(f"Missing required field: {field}")
        elif not config[field]:
            errors.append(f"Empty value for required field: {field}")

    # Check that COLUMN is a list of exactly one element
    if 'COLUMN' in config and isinstance(config['COLUMN'], list):
        if len(config['COLUMN']) != 1:
            errors.append("Only one COLUMN at a time is supported")
    else:
        errors.append("COLUMN must be a list")

    # Check for optional fields
    for field in optional_fields:
        if field in config and not config[field]:
            errors.append(f"Empty value for optional field: {field}")

    # Raise an exception if there are any errors
    if errors:
        raise ValueError("Configuration validation errors: " + "; ".join(errors))

    # If no errors, return the validated config
    return config

if __name__ == "__main__":
    config = {
        "COLUMN": ["column_name"], # only support 1 column at a time
        "UUID": "uuid_value"
    }

    try:
        validated_config = validate_config(config)
        print("Configuration is valid:", validated_config)
    except ValueError as e:
        print("Configuration validation failed:", str(e))
