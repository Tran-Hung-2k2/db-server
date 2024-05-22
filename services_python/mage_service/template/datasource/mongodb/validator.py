def validate_config(config):
    required_fields = [
        "MONGODB_CONNECTION_STRING",
        "MONGODB_USER",
        "MONGODB_PASSWORD",
        "MONGODB_HOST",
        "MONGODB_PORT",
        "MONGODB_DATABASE",
        "MONGODB_COLLECTION",
        "QUERY"
    ]

    optional_fields = [
        "MONGODB_CONNECTION_STRING"
    ]

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
        "MONGODB_CONNECTION_STRING": "mongodb://localhost:27017",
        "MONGODB_USER": "myuser",
        "MONGODB_PASSWORD": "mypassword",
        "MONGODB_HOST": "localhost",
        "MONGODB_PORT": 27017,
        "MONGODB_DATABASE": "mydatabase",
        "MONGODB_COLLECTION": "mycollection",
        "QUERY": "{}"
    }

    try:
        validated_config = validate_config(config)
        print("Configuration is valid:", validated_config)
    except ValueError as e:
        print("Configuration validation failed:", str(e))
