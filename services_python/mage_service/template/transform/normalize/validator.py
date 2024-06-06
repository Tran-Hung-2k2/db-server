def validate_config(config):
    required_fields = [
        "COLUMNS"
    ]

    optional_fields = [
        # Add any optional fields here if needed
    ]

    errors = []

    # Check for required fields
    for field in required_fields:
        if field not in config:
            errors.append(f"Missing required field: {field}")
        elif not config[field]:
            errors.append(f"Empty value for required field: {field}")
        elif field == "COLUMNS" and not isinstance(config[field], list):
            errors.append(f"The field {field} must be a list.")

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
        "COLUMNS": ["column1", "column2", "column3"]
    }

    try:
        validated_config = validate_config(config)
        print("Configuration is valid:", validated_config)
    except ValueError as e:
        print("Configuration validation failed:", str(e))
