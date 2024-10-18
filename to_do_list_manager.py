import json
import os
from datetime import datetime, timedelta

# File to store tasks
TASKS_FILE = "tasks.json"

# Load tasks from file
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as file:
            return json.load(file)
    return []

# Save tasks to file
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

# Add a new task with priority
def add_task(tasks):
    description = input("Enter the task description: ")
    due_date = input("Enter the due date (YYYY-MM-DD) or leave blank: ")
    if due_date:
        try:
            due_date = datetime.strptime(due_date, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Task not added.")
            return
    else:
        due_date = None

    # Ask for task priority
    priority = input("Enter task priority (low, medium, high): ").lower()
    if priority not in ['low', 'medium', 'high']:
        print("Invalid priority. Setting priority to 'low' by default.")
        priority = 'low'

    task = {
        "description": description,
        "due_date": due_date,
        "completed": False,
        "priority": priority
    }
    tasks.append(task)
    save_tasks(tasks)
    print("Task added successfully!")

# Check for tasks that are due soon
def check_due_soon(tasks):
    today = datetime.now().date()
    due_soon_tasks = [task for task in tasks if task['due_date'] and today <= datetime.strptime(task['due_date'], "%Y-%m-%d").date() <= today + timedelta(days=3)]
    return due_soon_tasks

# View all tasks, with optional filter for completed/pending/due soon/priority
def view_tasks(tasks, filter_type=None):
    if not tasks:
        print("No tasks found.")
        return

    if filter_type == "completed":
        filtered_tasks = [task for task in tasks if task['completed']]
        print("\nCompleted Tasks:")
    elif filter_type == "pending":
        filtered_tasks = [task for task in tasks if not task['completed']]
        print("\nPending Tasks:")
    elif filter_type == "due_soon":
        filtered_tasks = [task for task in tasks if task['due_date'] and datetime.now().date() <= datetime.strptime(task['due_date'], "%Y-%m-%d").date() <= datetime.now().date() + timedelta(days=3)]
        print("\nTasks Due Soon:")
    elif filter_type == "priority":
        priority = input("Enter priority to filter (low, medium, high): ").lower()
        filtered_tasks = [task for task in tasks if task['priority'] == priority]
        print(f"\nTasks with Priority '{priority.capitalize()}':")
    else:
        filtered_tasks = tasks
        print("\nAll Tasks:")

    if filtered_tasks:
        for idx, task in enumerate(filtered_tasks, 1):
            due = f" (Due: {task['due_date']})" if task['due_date'] else ""
            status = "[X]" if task['completed'] else "[ ]"
            priority = f" (Priority: {task['priority'].capitalize()})"
            print(f"{idx}. {status} {task['description']}{due}{priority}")
    else:
        print("No tasks found for this category.")

    # Check and remind about tasks due soon
    due_soon_tasks = check_due_soon(tasks)
    if due_soon_tasks:
        print("\n*** Reminder: You have tasks due soon! ***")
        for task in due_soon_tasks:
            print(f"- {task['description']} (Due: {task['due_date']})")

# Mark a task as complete
def mark_task_completed(tasks):
    view_tasks(tasks, filter_type="pending")
    if not tasks:
        return
    task_num = int(input("Enter the task number to mark as complete: ")) - 1
    if 0 <= task_num < len(tasks):
        tasks[task_num]['completed'] = True
        save_tasks(tasks)
        print("Task marked as completed!")
    else:
        print("Invalid task number.")

# Edit a task
def edit_task(tasks):
    view_tasks(tasks)
    if not tasks:
        return
    task_num = int(input("Enter the task number to edit: ")) - 1
    if 0 <= task_num < len(tasks):
        task = tasks[task_num]
        new_description = input(f"Enter new description (leave blank to keep '{task['description']}'): ")
        new_due_date = input(f"Enter new due date (YYYY-MM-DD) or leave blank (current: {task['due_date']}): ")
        new_priority = input(f"Enter new priority (low, medium, high) or leave blank (current: {task['priority']}): ").lower()

        if new_description:
            task['description'] = new_description
        if new_due_date:
            try:
                task['due_date'] = datetime.strptime(new_due_date, "%Y-%m-%d").strftime("%Y-%m-%d")
            except ValueError:
                print("Invalid date format. Task not updated.")
                return
        if new_priority in ['low', 'medium', 'high']:
            task['priority'] = new_priority
        save_tasks(tasks)
        print("Task updated successfully!")
    else:
        print("Invalid task number.")

# Delete a task
def delete_task(tasks):
    view_tasks(tasks)
    if not tasks:
        return
    task_num = int(input("Enter the task number to delete: ")) - 1
    if 0 <= task_num < len(tasks):
        tasks.pop(task_num)
        save_tasks(tasks)
        print("Task deleted successfully!")
    else:
        print("Invalid task number.")

# User menu
def show_menu():
    print("\nTo-Do List Manager")
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. View Completed Tasks")
    print("4. View Pending Tasks")
    print("5. View Tasks Due Soon")
    print("6. View Tasks by Priority")
    print("7. Mark Task as Completed")
    print("8. Edit Task")
    print("9. Delete Task")
    print("10. Exit")

def main():
    tasks = load_tasks()

    while True:
        show_menu()
        choice = input("Choose an option: ")

        if choice == '1':
            add_task(tasks)
        elif choice == '2':
            view_tasks(tasks)
        elif choice == '3':
            view_tasks(tasks, filter_type="completed")
        elif choice == '4':
            view_tasks(tasks, filter_type="pending")
        elif choice == '5':
            view_tasks(tasks, filter_type="due_soon")
        elif choice == '6':
            view_tasks(tasks, filter_type="priority")
        elif choice == '7':
            mark_task_completed(tasks)
        elif choice == '8':
            edit_task(tasks)
        elif choice == '9':
            delete_task(tasks)
        elif choice == '10':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
