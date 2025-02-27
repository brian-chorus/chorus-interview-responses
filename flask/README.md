# Flask Application for Task Management

## Overview

This Flask application provides APIs for managing workers, tasks, occurrences, and occurrence assignments. The application uses SQLAlchemy for ORM and PostgreSQL as the database.


## Installation

1. Tilt will install and run Flask using the command below. Navigate to the root of the repo and run the command below 
    ```bash
   tilt up
    ```

## API Endpoints

### Worker

- **Create a Worker**
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"name": "John Doe"}' http://localhost:5000/worker | jq .
    ```

- **Get All Workers**
    ```bash
    curl -X GET http://localhost:5000/workers | jq .
    ```

- **Update a Worker**
    ```bash
    curl -X PUT -H "Content-Type: application/json" -d '{"name": "Jane Doe", "active": false}' http://localhost:5000/worker/<worker_id> | jq .
    ```

- **Delete a Worker**
    ```bash
    curl -X DELETE http://localhost:5000/worker/<worker_id> | jq .
    ```

### Task

- **Create a Task**
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"name": "Daily Task", "cadence": "DAILY", "occurrences": 10}' http://localhost:5000/task | jq .
    ```

- **Get All Tasks**
    ```bash
    curl -X GET http://localhost:5000/tasks | jq .
    ```

- **Update a Task**
    ```bash
    curl -X PUT -H "Content-Type: application/json" -d '{"name": "Updated Task", "cadence": "WEEKLY", "occurrences": 5}' http://localhost:5000/task/<task_id> | jq .
    ```

- **Delete a Task**
    ```bash
    curl -X DELETE http://localhost:5000/task/<task_id> | jq .
    ```

### Occurrence

- **Create an Occurrence**
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"task_id": 1, "occurrence_timestamp": "2025-02-27T10:00:00", "occurrence_status": "NOT_STARTED"}' http://localhost:5000/occurrence | jq .
    ```

- **Get All Occurrences**
    ```bash
    curl -X GET http://localhost:5000/occurrences | jq .
    ```

- **Get All Occurrences for a Task**
    ```bash
    curl -X GET http://localhost:5000/task/<task_id>/occurrences | jq .
    ```

- **Update an Occurrence**
    ```bash
    curl -X PUT -H "Content-Type: application/json" -d '{"occurrence_timestamp": "2025-02-28T10:00:00", "occurrence_status": "IN_PROGRESS"}' http://localhost:5000/occurrence/<occurrence_id> | jq .
    ```

- **Delete an Occurrence**
    ```bash
    curl -X DELETE http://localhost:5000/occurrence/<occurrence_id> | jq .
    ```

### Occurrence Assignment

- **Create an Occurrence Assignment**
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"task_worker_id": "<worker_id>", "occurrence_id": 1}' http://localhost:5000/occurrence_assignment | jq .
    ```

- **Get All Occurrence Assignments**
    ```bash
    curl -X GET http://localhost:5000/occurrence_assignments | jq .
    ```

- **Update an Occurrence Assignment**
    ```bash
    curl -X PUT -H "Content-Type: application/json" -d '{"task_worker_id": "<new_worker_id>", "occurrence_id": 2}' http://localhost:5000/occurrence_assignment/<occurrence_assignment_id> | jq .
    ```

- **Delete an Occurrence Assignment**
    ```bash
    curl -X DELETE http://localhost:5000/occurrence_assignment/<occurrence_assignment_id> | jq .
    ```
