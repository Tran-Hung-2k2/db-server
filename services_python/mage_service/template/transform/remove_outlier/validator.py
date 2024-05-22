def validate_config(config):
    required_fields = [
        "COLUMNS"

    ]

    optional_fields = [
        "METHOD"
    ]
    allowed_method = {'itree', 'lof', 'auto'}

    # 'itree'	Uses the Isolation Tree algorithm. Number of trees is set to 100.
    # 'lof'	Uses the Local Outlier Factor algorithm. Number of neighbors for computing local density scales with amount of data and contamination rate.
    # 'auto'	Automatically determines from above methods based on number of data points and dimensionality of the data.

    errors = []

    # Check for required fields
    for field in required_fields:
        if field not in config:
            errors.append(f"Missing required field: {field}")
        elif not config[field]:
            errors.append(f"Empty value for required field: {field}")

    # Check if STRATEGY is one of the allowed values
    if 'METHOD' in config and config['METHOD'] not in allowed_method:
        errors.append(f"Invalid value for METHOD: {config['METHOD']}. Must be one of {allowed_method}.")

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
        "METHOD": "auto"  # Ensure this is one of the allowed method
    }

    try:
        validated_config = validate_config(config)
        print("Configuration is valid:", validated_config)
    except ValueError as e:
        print("Configuration validation failed:", str(e))
