import json

data = {
    "pipeline": {
        "cache_block_output_in_memory": False,
        "concurrency_config": {},
        "created_at": "2024-04-10 10:15:42.723852+00:00",
        "data_integration": None,
        "description": "Stream pipeline",
        "executor_config": {},
        "executor_count": 1,
        "executor_type": None,
        "name": "kafka_to_kafka",
        "notification_config": {},
        "remote_variables_dir": None,
        "retry_config": {},
        "run_pipeline_in_one_process": False,
        "settings": {
            "triggers": None
        },
        "tags": [
            "stream"
        ],
        "type": "streaming",
        "uuid": "kafka_to_kafka",
        "variables_dir": "/home/src/mage_data/default_repo",
        "spark_config": {},
        "blocks": [
            {
                "all_upstream_blocks_executed": True,
                "color": None,
                "configuration": {
                    "file_source": {
                        "path": "default_repo/data_loaders/kafka_source.yaml"
                    }
                },
                "downstream_blocks": [
                    "transforms"
                ],
                "executor_config": None,
                "executor_type": "local_python",
                "has_callback": False,
                "name": "kafka source",
                "language": "yaml",
                "retry_config": None,
                "status": "updated",
                "timeout": None,
                "type": "data_loader",
                "upstream_blocks": [],
                "uuid": "kafka_source",
                "callback_blocks": [],
                "conditional_blocks": [],
                "content": "connector_type: kafka\nbootstrap_server: \"172.17.0.1:9092\"\ntopic: test\nconsumer_group: unique_consumer_group\nbatch_size: 10\n\n# Uncomment the config below to use SSL config\n# security_protocol: \"SSL\"\n# ssl_config:\n#   cafile: \"CARoot.pem\"\n#   certfile: \"certificate.pem\"\n#   keyfile: \"key.pem\"\n#   password: password\n#   check_hostname: true\n\n# Uncomment the config below to use SASL_SSL config\n# security_protocol: \"SASL_SSL\"\n# sasl_config:\n#   mechanism: \"PLAIN\"\n#   username: username\n#   password: password\n\n# Uncomment the config below to use protobuf schema to deserialize message\n# serde_config:\n#   serialization_method: PROTOBUF\n#   schema_classpath: \"path.to.schema.SchemaClass\"\n",
                "metadata": {
                    "data_integration": {
                        "connector_type": "kafka",
                        "bootstrap_server": "172.17.0.1:9092",
                        "topic": "test",
                        "consumer_group": "unique_consumer_group",
                        "batch_size": 10,
                        "sql": False
                    }
                },
                "tags": []
            },
            {
                "all_upstream_blocks_executed": False,
                "color": None,
                "configuration": {
                    "file_source": {
                        "path": "default_repo/transformers/transforms.py"
                    }
                },
                "downstream_blocks": [],
                "executor_config": None,
                "executor_type": "local_python",
                "has_callback": False,
                "name": "transforms",
                "language": "python",
                "retry_config": None,
                "status": "updated",
                "timeout": None,
                "type": "transformer",
                "upstream_blocks": [
                    "kafka_source"
                ],
                "uuid": "transforms",
                "callback_blocks": [],
                "conditional_blocks": [],
                "content": "from typing import Dict, List\n\nif 'transformer' not in globals():\n    from mage_ai.data_preparation.decorators import transformer\n\n\n@transformer\ndef transform(messages: List[Dict], *args, **kwargs):\n    for msg in messages:\n        print(msg)\n    return messages",
                "metadata": {},
                "tags": []
            }
        ],
        "callbacks": [],
        "conditionals": [],
        "widgets": [],
        "extensions": {},
        "updated_at": "2024-05-01T03:01:16.144004+00:00"
    },
    "metadata": None
}



# Extract required information to form the new JSON structure
new_json = {
    "pipelines": {
        "created_at": data["pipeline"]["created_at"],
        "updated_at": data["pipeline"]["updated_at"],
        "description": data["pipeline"]["description"],
        "name": data["pipeline"]["name"],
        "settings": data["pipeline"]["settings"],
        "tags": data["pipeline"]["tags"],
        "type": data["pipeline"]["type"],
        "uuid": data["pipeline"]["uuid"],
        "blocks": [{
            "name": block["name"],
            "downstream_blocks": block["downstream_blocks"],
            "type": block["type"],
            "upstream_blocks": block["upstream_blocks"],
            "uuid": block["uuid"],
            "status": block["status"],
            "conditional_blocks": block["conditional_blocks"],
            "callback_blocks": block["callback_blocks"],
            "has_callback": block["has_callback"],
            "retry_config": block["retry_config"]
        } for block in data["pipeline"]["blocks"]]
    },
    "metadata": data["metadata"]
}

# Convert the new JSON structure to a string
new_json_str = json.dumps(new_json, indent=4)
print(new_json_str)
