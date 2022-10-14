from apiflask import APIFlask, abort
from db import Task, session
from schemas import TaskOutputSchema, TaskInputSchema, TaskUpdateSchema
from flask import jsonify


app = APIFlask(__name__)
# -----------------------------------------------------------------

@app.get('/')
def index():
  return {'message':"Hello World"}

"""
  get    /task               |def->get_all_task
  get    /task/<task_id>     |def->get_task_by_id (for particular task)
  post   /tasks              |def->create_task
  put    /task/<task_id>     |def->update_task
  delete /task/<task_id>     |def->delete_task

"""
# -----------------------------------------------------------------
# Get_all_tasks
@app.get('/tasks')
def get_all_task():
  posts = session.query(Task).all()

  schema = TaskOutputSchema()
  result = schema.dump(posts, many=True)

  return jsonify(result)


# -----------------------------------------------------------------
# Create a new_task
@app.post('/tasks')
@app.input(TaskInputSchema)
@app.output(TaskOutputSchema)
def create_task(data):
  content = data.get("content")

  new_task = Task(content=content)

  session.add(new_task)
  session.commit()

  return new_task, 201


# -----------------------------------------------------------------
# Get a task my its id
@app.get('/tasks/<int:task_id>')
@app.output(TaskOutputSchema)
def get_task_by_id(task_id):
  task = session.query(Task).filter_by(id=task_id).first()

  if task is not None:
    return task, 200
  abort()


# -----------------------------------------------------------------
# Update_a_task
@app.put('/tasks/<int:task_id>')
@app.input(TaskUpdateSchema)
@app.output(TaskOutputSchema)
def update_task(task_id, data):
  content = data.get('content')
  is_completed = data.get('is_completed')

  task_to_update = session.query(Task).filter_by(id=task_id).first()
  task_to_update.content = content
  task_to_update.is_completed = is_completed

  session.commit()
  return task_to_update


# -----------------------------------------------------------------
# Delete_a_task
@app.delete('/tasks/<int:task_id>')
def delete_task(task_id):
  task_to_delete = session.query(Task).filter_by(id=task_id).first()

  session.delete(task_to_delete)
  session.commit()
  return {"message" : "deleted"}, 204


