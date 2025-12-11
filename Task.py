"""
Each task should be able to be uniquely identified from all other tasks
by a numeric identifier. Tasks should be assigned a priority level of 1,
2 or 3 to indicate the importance (3 is the highest priority).

A Task object should store the date they were created and completed. In
addition, the task manager should allows for different types of tasks: a
task with no due date and a task with a due date.
"""

from datetime import datetime


class Task:
    """Representation of a task

    Attributes:
                - created - date
                - completed - date
                - name - string
                - unique id - number
                - priority - int value of 1, 2, or 3; 1 is default
                - due date - date, this is optional
    """

    _id_counter = 1

    def __init__(self, name, priority=1, due=None):
        self.created = datetime.now()
        self.completed = None
        self.name = name
        self.unique_id = Task._id_counter 
        Task._id_counter += 1
        self.priority = priority
        self.due_date = due

    def mark_complete(self):
        """Mark the task as completed with current date/time"""
        self.completed = datetime.now()

    def __repr__(self):
        return (f"Task(id={self.unique_id}, name='{self.name}', priority={self.priority}, "
                f"created={self.created}, due={self.due_date}, completed={self.completed})")

    def __str__(self):
        status = "Completed" if self.completed else "Incomplete"
        due_str = f", Due: {self.due_date}" if self.due_date else ""
        return f"[{self.unique_id}] {self.name} (Priority: {self.priority}) - {status}{due_str}"

class Tasks:
   """A list of `Task` objects."""
   
    def __init__(self):
        """Read pickled tasks file into a list"""
        # List of Task objects
        self.tasks = [] 
        # your code here

    def pickle_tasks(self):
        """Picle your task list to a file"""
        # your code here

    # Complete the rest of the methods, change the method definitions as needed
    def list(self):
        pass

    def report(self):
        pass

    def done(self):
        pass

    def query(self):
        pass

    def add(self):
        pass