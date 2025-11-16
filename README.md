# flask-application---sportive-stats
 A python server that will handle a series of requests starting from a data set in *csv* (comma separated values) format. The server will provide statistics based on the data in the csv.
# Multi-threaded Flask Server for US Health Statistics

This project implements a multi-threaded Flask server that provides statistical analysis on a dataset of nutrition, physical activity, and obesity in the United States between 2011 and 2022. The server handles concurrent requests using a thread pool and a job queue system, storing results on disk to simulate a lightweight database.

## Features
- Multi-threaded request handling using `threading.Thread`, `Lock`, and `Event`.
- Graceful shutdown support: stops accepting new requests while completing pending jobs.
- Computes various statistics on the dataset: `states_mean`, `state_mean`, `best5`, `worst5`, `global_mean`, `diff_from_mean`, `state_diff_from_mean`, `mean_by_category`, `state_mean_by_category`.
- Results stored in `results/` folder as JSON files, simulating database storage.
- Logging with `RotatingFileHandler`, UTC timestamps, and INFO level to track requests and results.
- Unit tests validate request handling, job queue behavior, and graceful shutdown functionality.


### Module Description
- **DataIngestor**: Parses the CSV file and creates a list of dictionaries for each row in the dataset.
- **TaskRunner**: Manages the thread pool and job queue. Each thread runs a `run` method that executes jobs according to their ID and parameters.
- **Logger**: Records all incoming requests and results in `webserver.log` using `RotatingFileHandler` with UTC timestamps.
- **Unit Tests**: Simulate requests, perform graceful shutdown, and verify the state of job completion and queue length.





for running: python3 TestWebserver.py
