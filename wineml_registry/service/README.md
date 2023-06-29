# WineML Registry Rest API
This is the core backend of wineml to communicate with backend artifact storages and managing all the metadata. It uses FastAPI to communicate with the client or UI to fetch the information from backend store and database.

# How to use?
Steps to start using it locally:
1. Install required libraries, there are different versions of `requirements.txt` based on your backend store setup, will be using AWS S3 for this example:
```
pip install -r docker/aws/requirements.txt
```
2. Start the FastAPI server
```
python src/main.py
```
3. Visit http://localhost:8081/documentation to view the swagger documentation page.
