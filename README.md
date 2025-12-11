# Task Manager

A command-line task manager application that allows you to manage your tasks from anywhere on your computer.

## Installation

To make the task manager executable from anywhere, follow these steps:

### Step 1: Make the script executable

```bash
chmod +x task_manager.py
```

This changes the file permissions to allow the script to be executed as a program.

### Step 2: Copy to a location in your PATH

On macOS and Linux, command-line applications are typically stored in directories that are included in your `$PATH` environment variable. Common locations include:

- **macOS/Linux**: `/usr/local/bin` (recommended for user-installed programs)
- **macOS/Linux**: `/opt/local/bin` (if using MacPorts)
- **Linux**: `/usr/bin` (system-wide, requires sudo)

Copy the task manager to `/usr/local/bin`:

```bash
cp task_manager.py /usr/local/bin/task_manager
```

**Note**: You may need to use `sudo` if you don't have write permissions:

```bash
sudo cp task_manager.py /usr/local/bin/task_manager
```

Alternatively, you can create a symbolic link (recommended):

```bash
ln -s $(pwd)/task_manager.py /usr/local/bin/task_manager
```

### Step 3: Verify installation

Test that the task manager is accessible from anywhere:

```bash
task_manager --help
```

If this works, you're all set!

## Data Storage

The task manager stores your tasks in an invisible file located in your home directory:

```
~/.tasks.pkl
```

This allows your tasks to be accessible from any location on your computer. The file is automatically created the first time you add a task.

## Usage

### Add a task

```bash
task_manager --add "Task description" --priority 1 --due 3/20/2025
```

- `--add`: Task description (required)
- `--priority`: Priority level 1-3 (optional, default: 1)
- `--due`: Due date in M/D/YYYY format (optional)

### List incomplete tasks

```bash
task_manager --list
```

### View all tasks (completed and incomplete)

```bash
task_manager --report
```

### Search for tasks

```bash
task_manager --query "search term"
```

Multiple search terms are supported:

```bash
task_manager --query eggs dog milk
```

### Mark a task as complete

```bash
task_manager --done 1
```

### Delete a task

```bash
task_manager --delete 1
```

## Troubleshooting

### Command not found

If you get "command not found" when running `task_manager`:

1. Verify the file is executable: `ls -l task_manager.py`
2. Verify `/usr/local/bin` is in your PATH: `echo $PATH`
3. Try running with the full path: `/usr/local/bin/task_manager --help`

### Permission denied

If you get "permission denied", ensure the file is executable:

```bash
chmod +x task_manager.py
```

### Python not found

Ensure Python 3 is installed and accessible. The shebang line `#!/usr/bin/env python3` looks for `python3` in your PATH.
