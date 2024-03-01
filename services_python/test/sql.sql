CREATE TABLE dataset_db (
    state_id SERIAL PRIMARY KEY,
    state_name VARCHAR(255),
    datasource_id VARCHAR(50),
    dataset_id VARCHAR(50),
    dataset_name VARCHAR(255),
    dataset_version VARCHAR(50),
    dataset_schema JSON
    user_id VARCHAR(50),
    created_date TIMESTAMP,
);
