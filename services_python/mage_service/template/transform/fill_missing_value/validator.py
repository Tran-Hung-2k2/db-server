def validate_config(config):
    required_fields = [
        "COLUMNS",
        "STRATEGY"
    ]

    optional_fields = [
        # List any optional fields if there are any
    ]

    allowed_strategies = {'average', 'column', 'constant', 'median', 'mode', 'no_action', 'random', 'remove_rows', 'sequential'}

    errors = []

    # Check for required fields
    for field in required_fields:
        if field not in config:
            errors.append(f"Missing required field: {field}")
        elif not config[field]:
            errors.append(f"Empty value for required field: {field}")

    # Check if STRATEGY is one of the allowed values
    if 'STRATEGY' in config and config['STRATEGY'] not in allowed_strategies:
        errors.append(f"Invalid value for STRATEGY: {config['STRATEGY']}. Must be one of {allowed_strategies}.")

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
        "COLUMNS": ["column1", "column2"],
        "STRATEGY": "mean"  # Ensure this is one of the allowed strategies
    }

    try:
        validated_config = validate_config(config)
        print("Configuration is valid:", validated_config)
    except ValueError as e:
        print("Configuration validation failed:", str(e))
