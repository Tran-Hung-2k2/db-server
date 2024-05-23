def validate_config(config):
    required_fields = [
        "MINIO_ACCESS_KEY_ID",
        "MINIO_SECRET_ACCESS_KEY",
        "MINIO_ENDPOINT_URL",
        "USER_ID",
        "DATA_MART_ID",
        "MODE"
    ]

    optional_fields = []

    errors = []

    # Check for required fields
    for field in required_fields:
        if field not in config:
            errors.append(f"Missing required field: {field}")
        elif not config[field]:
            errors.append(f"Empty value for required field: {field}")

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
        "MINIO_ACCESS_KEY_ID": "your_access_key_id",
        "MINIO_SECRET_ACCESS_KEY": "your_secret_access_key",
        "MINIO_ENDPOINT_URL": "your_endpoint_url",
        "USER_ID": "your_user_id",
        "DATA_MART_ID": "your_data_mart_id",
        "MODE": "your_mode"  # e.g., "append" or "overwrite"
        # Optionally, include optional fields as needed
    }

    try:
        validated_config = validate_config(config)
        print("Configuration is valid:", validated_config)
    except ValueError as e:
        print("Configuration validation failed:", str(e))
