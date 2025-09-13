from flask import Flask, render_template, request, redirect, url_for
from config import Config
from models import db, Task
from datetime import datetime

# --- App Initialization ---
app = Flask(__name__)
app.config.from_object(Config)

# --- Database Initialization ---
db.init_app(app)

# --- Routes ---
@app.route('/')
def index():
    # READ all tasks from the database
    tasks = Task.query.order_by(Task.due_date).all()
    # Your list of subjects
    subjects = [
        "Software Engineering", "Mobile Applications", "Data Structure", 
        "Mathematics", "Information Security", "Frontend Development", 
        "Basic Indian Language", "Information Security lab", "Frontend Development lab", 
        "Mobile Applications lab", "Data Structure lab", "Integral Yoga"
    ]
    return render_template('index.html', tasks=tasks, subjects=subjects)

@app.route('/add', methods=['POST'])
def add_task():
    # CREATE a new task
    title = request.form.get('title')
    subject = request.form.get('subject')
    due_date_str = request.form.get('due_date')
    
    # Convert date string to a date object
    due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None

    if title and subject:
        new_task = Task(title=title, subject=subject, due_date=due_date)
        db.session.add(new_task)
        db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/update/<int:task_id>')
def update_task_status(task_id):
    # UPDATE a task's status
    task = Task.query.get_or_404(task_id)
    
    if task.status == 'To Do':
        task.status = 'In Progress'
    elif task.status == 'In Progress':
        task.status = 'Completed'
    
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    # DELETE a task
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

# --- Main Execution ---
if __name__ == '__main__':
    with app.app_context():
        # This will create the database tables if they don't exist
        db.create_all() 
    app.run(debug=True)