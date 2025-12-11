"""
Fancy task managers with slick user interfaces are slow and cumbersome.
Now that you have the power of the command line at your disposal, you
would like be able to access all your tasks without having to burden
yourself with tedious pointing and clicking. For your final project,
you will design an object oriented task manager application that will
allow you to enter tasks, save them to a file, and retrieve them...all
without moving your hands from the keyboard.
"""

import argparse
import sys
from Task import Tasks


def main():
    parser = argparse.ArgumentParser(
        description="Task Manager - Manage your tasks from the command line"
    )
    parser.add_argument(
        "--add",
        type=str,
        required=False,
        help="Add a new task with the given description"
    )
    parser.add_argument(
        "--due",
        type=str,
        required=False,
        help="Due date for the task in format MM/DD/YYYY"
    )
    parser.add_argument(
        "--priority",
        type=int,
        required=False,
        default=1,
        help="Priority level: 1, 2, or 3 (default: 1)"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Display all incomplete tasks"
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Display all tasks (completed and incomplete)"
    )
    parser.add_argument(
        "--query",
        type=str,
        nargs="+",
        required=False,
        help="Search for tasks matching the given terms"
    )
    parser.add_argument(
        "--done",
        type=int,
        required=False,
        help="Mark a task as complete by its ID"
    )
    parser.add_argument(
        "--delete",
        type=int,
        required=False,
        help="Delete a task by its ID"
    )
    args = parser.parse_args()
    tasks = Tasks()
    
    try:
        if args.add:
            tasks.add(args.add, args.priority, args.due)
            tasks.pickle_tasks()
        elif args.list:
            tasks.list()
        elif args.report:
            tasks.report()
        elif args.query:
            search_terms = " ".join(args.query)
            tasks.query(search_terms)
        elif args.done:
            tasks.done(args.done)
            tasks.pickle_tasks()
        elif args.delete:
            tasks.delete(args.delete)
            tasks.pickle_tasks()
        else:
            parser.print_help()
    except ValueError as e:
        print("There was an error in creating your task. Run \"main.py -h\" for usage instructions.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
