"""
Each task should be able to be uniquely identified from all other tasks
by a numeric identifier. Tasks should be assigned a priority level of 1,
2 or 3 to indicate the importance (3 is the highest priority).

A Task object should store the date they were created and completed. In
addition, the task manager should allows for different types of tasks: a
task with no due date and a task with a due date.
"""

from datetime import datetime
import re
import pickle
import os


class Task:
    """Representation of a task

    Attributes:
                - created - date
                - completed - date
                - name - string
                - unique_id - number
                - priority - int value of 1, 2, or 3; 1 is default
                - due_date - date, this is optional
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

    @classmethod
    def set_id_counter(cls, value):
        """Set the ID counter to a specific value.
        
        Args:
            value (int): The new ID counter value
            
        Raises:
            ValueError: If value is not a positive integer
        """
        if not isinstance(value, int) or value < 1:
            raise ValueError("ID must be a positive integer")
        cls._id_counter = value

    def __repr__(self):
        return (f"Task(id={self.unique_id}, name='{self.name}', priority={self.priority}, "
                f"created={self.created}, due={self.due_date}, completed={self.completed})")

    def __str__(self):
        status = "Completed" if self.completed else "Incomplete"
        due_str = f", Due: {self.due_date}" if self.due_date else ""
        return f"[{self.unique_id}] {self.name} (Priority: {self.priority}) - {status}{due_str}"

class Tasks:
    """A list of `Task` objects."""
    
    TASKS_FILE = ".tasks.pkl"
    
    def __init__(self):
        self.tasks = []
        self._load_tasks()
    
    def _load_tasks(self):
        """Load tasks from pickle file if it exists."""
        if os.path.exists(self.TASKS_FILE):
            try:
                with open(self.TASKS_FILE, 'rb') as f:
                    loaded_data = pickle.load(f)
                    self.tasks = loaded_data.get('tasks', [])
                    if self.tasks:
                        max_id = max(task.unique_id for task in self.tasks)
                        Task.set_id_counter(max_id + 1)
            except (pickle.PickleError, IOError) as e:
                print(f"Warning: Could not load tasks from {self.TASKS_FILE}: {e}")
                self.tasks = []

    def pickle_tasks(self):
        """Pickle your task list to a file"""
        try:
            data = {'tasks': self.tasks}
            with open(self.TASKS_FILE, 'wb') as f:
                pickle.dump(data, f)
            print(f"Tasks saved to {self.TASKS_FILE}")
        except IOError as e:
            print(f"Error: Could not save tasks to {self.TASKS_FILE}: {e}")

    def _format_id(self, task_id):
        """Format task ID as 4-digit string with leading zeros.
        
        Args:
            task_id (int): The task ID to format
            
        Returns:
            str: Formatted ID as 4-digit string (e.g., "0001")
        """
        return f"{task_id:04d}"

    def _sort_tasks(self, tasks):
        """Sort tasks by due date and priority.
        
        Sorting rules:
        - Tasks with due dates come first, sorted by due date
        - Tasks without due dates come last
        - Within each group, sort by decreasing priority (3, 2, 1)
        
        Args:
            tasks: List of Task objects to sort
            
        Returns:
            Sorted list of Task objects
        """
        return sorted(
            tasks,
            key=lambda t: (
                t.due_date is None,
                t.due_date if t.due_date is not None else None,
                -t.priority
            )
        )

    def _display_tasks(self, tasks, report=False):
        """Display a list of tasks in formatted table.
        
        Args:
            tasks: List of Task objects to display
            report: If True, show report format with created/completed dates;
                   if False, show standard list format (default: False)
        """
        if not tasks:
            print("No tasks found.")
            return
        
        if report:
            print(f"{'ID':<5} {'Age':<5} {'Due Date':<11} {'Priority':<10} {'Task':<20} {'Created':<30} {'Completed'}")
            print("-" * 120)
            
            for task in tasks:
                task_id = self._format_id(task.unique_id)
                age = (datetime.now().date() - task.created.date()).days
                age_str = f"{age}d"
                due_date_str = task.due_date.strftime("%m/%d/%Y") if task.due_date else "-"
                priority = task.priority
                name = task.name[:17] + ".." if len(task.name) > 19 else task.name
                created_str = task.created.strftime("%a %b %d %H:%M:%S %Z %Y")
                completed_str = task.completed.strftime("%a %b %d %H:%M:%S %Z %Y") if task.completed else "-"
                
                print(f"{task_id:<5} {age_str:<5} {due_date_str:<11} {priority:<10} {name:<20} {created_str:<30} {completed_str}")
        else:
            print(f"{'ID':<5} {'Age':<5} {'Due Date':<11} {'Priority':<10} {'Task'}")
            print("-" * 70)
            
            for task in tasks:
                task_id = self._format_id(task.unique_id)
                age = (datetime.now().date() - task.created.date()).days
                age_str = f"{age}d"
                due_date_str = task.due_date.strftime("%m/%d/%Y") if task.due_date else "-"
                priority = task.priority
                name = task.name
                print(f"{task_id:<5} {age_str:<5} {due_date_str:<11} {priority:<10} {name}")

    def list(self):
        """Display a list of incomplete tasks sorted by due date and priority."""
        incomplete_tasks = [task for task in self.tasks if task.completed is None]
        if not incomplete_tasks:
            print("No incomplete tasks.")
            return
        sorted_tasks = self._sort_tasks(incomplete_tasks)

        self._display_tasks(sorted_tasks)

    def report(self):
        """Display a report of all tasks (completed and incomplete).
        
        Follows the same sorting order as --list command.
        Shows created and completed dates for each task.
        """
        if not self.tasks:
            print("No tasks found.")
            return
        
        sorted_tasks = self._sort_tasks(self.tasks)
        self._display_tasks(sorted_tasks, report=True)

    def delete(self, task_id):
        """Delete a task by its unique ID.
        
        Args:
            task_id (int): The unique ID of the task to delete
            
        Raises:
            ValueError: If task ID is not found or is invalid
        """
        if not isinstance(task_id, int):
            raise ValueError("Task ID must be an integer")

        for i, task in enumerate(self.tasks):
            if task.unique_id == task_id:
                self.tasks.pop(i)
                formatted_id = self._format_id(task_id)
                print(f"Deleted task {formatted_id}")
                return
        raise ValueError(f"Task ID {task_id} not found")

    def done(self, task_id):
        """Mark a task as complete by its unique ID.
        
        Args:
            task_id (int): The unique ID of the task to mark as complete
            
        Raises:
            ValueError: If task ID is not found or is invalid
        """
        if not isinstance(task_id, int):
            raise ValueError("Task ID must be an integer")

        for task in self.tasks:
            if task.unique_id == task_id:
                task.mark_complete()
                formatted_id = self._format_id(task_id)
                print(f"Completed task {formatted_id}")
                return
        raise ValueError(f"Task ID {task_id} not found")

    def query(self, search_terms):
        """Search for tasks matching any of the search terms (case-insensitive).
        
        Args:
            search_terms: String of search terms separated by spaces
            Only incomplete tasks are returned.
        """
        search_terms = search_terms.split()

        incomplete_tasks = [task for task in self.tasks if task.completed is None]
        matching_tasks = []
        for task in incomplete_tasks:
            for term in search_terms:
                if re.search(re.escape(term), task.name, re.IGNORECASE):
                    matching_tasks.append(task)
                    break

        sorted_tasks = self._sort_tasks(matching_tasks)
        
        self._display_tasks(sorted_tasks)

    def add(self, name, priority=1, due=None):
        """Add a new task to the task list.
        
        Args:
            name (str): The task description
            priority (int): Priority level (1, 2, or 3; default is 1)
            due (str or None): Optional due date in format MM/DD/YYYY
            
        Returns:
            int: The unique ID of the newly created task
            
        Raises:
            ValueError: If data validation fails
        """
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Task name must be a non-empty string")

        if not isinstance(priority, int) or priority not in [1, 2, 3]:
            raise ValueError("Priority must be an integer value of 1, 2, or 3")
        parsed_due = None
        if due is not None:
            try:
                parsed_due = datetime.strptime(due, "%m/%d/%Y").date()
            except (ValueError, TypeError):
                raise ValueError("Due date must be in format MM/DD/YYYY")
        
        new_task = Task(name.strip(), priority, parsed_due)
        self.tasks.append(new_task)
        task_id = new_task.unique_id
        formatted_id = self._format_id(task_id)
        print(f"Created Task {formatted_id}")