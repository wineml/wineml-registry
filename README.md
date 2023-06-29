# WineML Registry
WineML Registry is a model management tool that helps your data science team to manage machine learning models in a proper and scalable way. It is still in early development stage so expect more features to come in the future.

# Features
- Custom Versioning Semantic
- Custom Model Status
- Models tagging
- Namespace Isolcation

# How it works?
WineML uses a backend store and database to store all the information about your models.

## Supported backend store
- [AWS S3](https://aws.amazon.com/s3/)
- [Google GCS](https://cloud.google.com/storage)
- [Azure Blob Storage](https://azure.microsoft.com/en-us/products/storage/blobs)

## Supported database
- [sqlite](https://www.sqlite.org/index.html)

# Features and enhancements in roadmap
- Python client library to submit models in arbitrary model development pipeline
- RBAC
- Custom Metrics loggings for models

# More database support
- [PostgreSQL](https://www.postgresql.org/)
