from flask import Flask, request, jsonify
from db import db
from models import Worker, Task, Occurrence, OccurrenceAssignment, CadenceEnum, OccurrenceStatusEnum
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}:{os.environ['POSTGRES_PORT']}/{os.environ['POSTGRES_DB']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


# CRUD operations for Worker
@app.route('/worker', methods=['POST'])
def create_worker():
    data = request.json
    new_worker = Worker(name=data['name'])
    db.session.add(new_worker)
    db.session.commit()
    return jsonify({"message": "Worker created successfully!", "id": str(new_worker.id)}), 201


@app.route('/workers', methods=['GET'])
def get_workers():
    workers = Worker.query.all()
    results = [{"id": str(worker.id), "name": worker.name, "active": worker.active} for worker in workers]
    return jsonify(results), 200


@app.route('/worker/<worker_id>', methods=['PUT'])
def update_worker(worker_id):
    data = request.json
    worker = Worker.query.get(worker_id)
    if not worker:
        return jsonify({"message": "Worker not found"}), 404
    worker.name = data['name']
    worker.active = data.get('active', worker.active)
    db.session.commit()
    return jsonify({"message": "Worker updated successfully!"})


@app.route('/worker/<worker_id>', methods=['DELETE'])
def delete_worker(worker_id):
    worker = Worker.query.get(worker_id)
    if not worker:
        return jsonify({"message": "Worker not found"}), 404
    db.session.delete(worker)
    db.session.commit()
    return jsonify({"message": "Worker deleted successfully!"})


# Helper function to create occurrences
def create_occurrences(task):
    if task.cadence == CadenceEnum.daily:
        increment = timedelta(days=1)
    elif task.cadence == CadenceEnum.weekly:
        increment = timedelta(weeks=1)
    elif task.cadence == CadenceEnum.monthly:
        increment = timedelta(days=30)  # Approximation, adjust if needed

    current_time = datetime.now()

    for i in range(task.occurrences):
        occurrence_timestamp = current_time + (increment * i)
        new_occurrence = Occurrence(
            task_id=task.id,
            occurrence_timestamp=occurrence_timestamp,
            occurrence_status=OccurrenceStatusEnum.not_started
        )
        db.session.add(new_occurrence)
        db.session.commit()  # Commit changes after adding each occurrence


@app.route('/task', methods=['POST'])
def create_task():
    data = request.json
    cadence_value = CadenceEnum[data['cadence'].lower()]  # Convert the string to the enum value
    new_task = Task(
        name=data['name'],
        cadence=cadence_value,
        occurrences=data['occurrences']
    )
    db.session.add(new_task)
    db.session.commit()

    # Automatically create occurrences
    create_occurrences(new_task)

    return jsonify({"message": "Task created successfully!", "id": new_task.id}), 201


@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    results = [{"id": task.id, "name": task.name, "cadence": task.cadence.value, "occurrences": task.occurrences} for
               task in tasks]
    return jsonify(results), 200


@app.route('/task/<task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"message": "Task not found"}), 404
    task.name = data['name']
    task.cadence = data['cadence']
    task.occurrences = data['occurrences']
    db.session.commit()
    return jsonify({"message": "Task updated successfully!"})


@app.route('/task/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"message": "Task not found"}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully!"})


# CRUD operations for Occurrence
@app.route('/occurrence', methods=['POST'])
def create_occurrence():
    data = request.json
    new_occurrence = Occurrence(
        task_id=data['task_id'],
        occurrence_timestamp=data['occurrence_timestamp'],
        occurrence_status=data['occurrence_status']
    )
    db.session.add(new_occurrence)
    db.session.commit()
    return jsonify({"message": "Occurrence created successfully!", "id": new_occurrence.id}), 201


@app.route('/occurrences', methods=['GET'])
def get_occurrences():
    occurrences = Occurrence.query.all()
    results = [
        {"id": occurrence.id, "task_id": occurrence.task_id, "occurrence_timestamp": occurrence.occurrence_timestamp,
         "occurrence_status": occurrence.occurrence_status.value} for occurrence in occurrences]
    return jsonify(results), 200


@app.route('/occurrence/<occurrence_id>', methods=['PUT'])
def update_occurrence(occurrence_id):
    data = request.json
    occurrence = Occurrence.query.get(occurrence_id)
    if not occurrence:
        return jsonify({"message": "Occurrence not found"}), 404
    occurrence.occurrence_timestamp = data['occurrence_timestamp']
    occurrence.occurrence_status = data['occurrence_status']
    db.session.commit()
    return jsonify({"message": "Occurrence updated successfully!"})


@app.route('/occurrence/<occurrence_id>', methods=['DELETE'])
def delete_occurrence(occurrence_id):
    occurrence = Occurrence.query.get(occurrence_id)
    if not occurrence:
        return jsonify({"message": "Occurrence not found"}), 404
    db.session.delete(occurrence)
    db.session.commit()
    return jsonify({"message": "Occurrence deleted successfully!"})


@app.route('/task/<task_id>/occurrences', methods=['GET'])
def get_task_occurrences(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"message": "Task not found"}), 404
    occurrences = Occurrence.query.filter_by(task_id=task_id).all()
    results = [
        {"id": occurrence.id, "task_id": occurrence.task_id, "occurrence_timestamp": occurrence.occurrence_timestamp,
         "occurrence_status": occurrence.occurrence_status.value} for occurrence in occurrences]
    return jsonify(results), 200


# CRUD operations for OccurrenceAssignment
@app.route('/occurrence_assignment', methods=['POST'])
def create_occurrence_assignment():
    data = request.json
    new_occurrence_assignment = OccurrenceAssignment(
        task_worker_id=data['task_worker_id'],
        occurrence_id=data['occurrence_id']
    )
    db.session.add(new_occurrence_assignment)
    db.session.commit()
    return jsonify({"message": "OccurrenceAssignment created successfully!", "id": new_occurrence_assignment.id}), 201


@app.route('/occurrence_assignments', methods=['GET'])
def get_occurrence_assignments():
    occurrence_assignments = OccurrenceAssignment.query.all()
    results = [{"id": occurrence_assignment.id, "task_worker_id": str(occurrence_assignment.task_worker_id),
                "occurrence_id": occurrence_assignment.occurrence_id} for occurrence_assignment in
               occurrence_assignments]
    return jsonify(results), 200


@app.route('/occurrence_assignment/<occurrence_assignment_id>', methods=['PUT'])
def update_occurrence_assignment(occurrence_assignment_id):
    data = request.json
    occurrence_assignment = OccurrenceAssignment.query.get(occurrence_assignment_id)
    if not occurrence_assignment:
        return jsonify({"message": "OccurrenceAssignment not found"}), 404
    occurrence_assignment.task_worker_id = data['task_worker_id']
    occurrence_assignment.occurrence_id = data['occurrence_id']
    db.session.commit()
    return jsonify({"message": "OccurrenceAssignment updated successfully!"})


@app.route('/occurrence_assignment/<occurrence_assignment_id>', methods=['DELETE'])
def delete_occurrence_assignment(occurrence_assignment_id):
    occurrence_assignment = OccurrenceAssignment.query.get(occurrence_assignment_id)
    if not occurrence_assignment:
        return jsonify({"message": "OccurrenceAssignment not found"}), 404
    db.session.delete(occurrence_assignment)
    db.session.commit()
    return jsonify({"message": "OccurrenceAssignment deleted successfully!"})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables
    app.run(host='0.0.0.0', port=5000)
