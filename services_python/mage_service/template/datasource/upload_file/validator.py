def validate_config(config):
    required_fields = [
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "AWS_REGION",
        "AWS_ENDPOINT",
        "BUCKET_NAME",
        "OBJECT_KEY"
    ]

    optional_fields = [
        "LIMIT"
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

# Example usage
if __name__ == "__main__":
    config = {
        "AWS_ACCESS_KEY_ID": "your_access_key",
        "AWS_SECRET_ACCESS_KEY": "your_secret_key",
        "AWS_REGION": "your_region",
        "AWS_ENDPOINT": "your_endpoint",
        "BUCKET_NAME": "your_bucket_name",
        "OBJECT_KEY": "your_object_key",
        # Optionally, include optional fields as needed
        # "LIMIT": "your_limit" defautl is 10,000,000
    }

    try:
        validated_config = validate_config(config)
        print("Configuration is valid:", validated_config)
    except ValueError as e:
        print("Configuration validation failed:", str(e))
