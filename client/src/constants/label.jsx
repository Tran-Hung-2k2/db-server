import { batch } from 'react-redux';

const label = {
    role: {
        ADMIN: 'Admin',
        USER: 'User',
    },
    pipeline_type: {
        batch: 'batch',
        stream: 'stream',
    },
    channel_type: {
        PostgreSQL: 'PostgreSQL',
        MySQL: 'MySQL',
        MongoDB: 'MongoDB',
        MinIO: 'MinIO',
        AmazonS3: 'Amazon S3',
        Snowflake: 'Snowflake',
        OracleDB: 'Oracle DB',
        AzureBlobStorage: 'Azure Blob Storage',
        GoogleBigQuery: 'Google Big Query',
        API: 'API',
        UploadFile: 'Upload File',
    },
};

export default label;
