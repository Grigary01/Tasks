import json
import os
from datetime import datetime
import sys


def load_tasks():
    """Создает json файл при его отсуствии"""
    if not os.path.exists('tasks.json'):
        return []
    try:
        with open('tasks.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_tasks(tasks):
    """Сохраняет данный в json файл"""
    with open('tasks.json', 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def get_next_id(tasks):
    if not tasks:
        return 1
    return max(task['id'] for task in tasks) + 1


def create_task(description, task_id):
    """Создает задачу"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        "id": task_id,
        "description": description,
        "status": "todo",
        "createdAt": current_time,
        "updatedAt": current_time
    }


def add_task(description):
    """Добавляет новое описание"""
    tasks = load_tasks()
    next_id = get_next_id(tasks)
    new_task = create_task(description, next_id)
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Задача добавлена! (ID: {new_task['id']})")


def update_tasks(id, new_description):
    """Обновляет описание данной задачи"""
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == int(id):
            task['description'] = new_description
            task['updatedAt'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_tasks(tasks)
            print(f"Задача {id} обновлена")
            return
    print(f"Задача с ID {id} не найдена")


def delete_task(task_id):
    """Удаляет задачу"""
    tasks = load_tasks()
    for i, task in enumerate(tasks):
        if task['id'] == int(task_id):
            tasks.pop(i)
            save_tasks(tasks)
            print(f"Задача с ID {task_id} удалена")
            return
    print(f"Задача с ID {task_id} не найдена")


def mark_in_progress(task_id):
    """Меняет статус задачи на in_progress"""
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == int(task_id):
            task['status'] = 'in-progress'
            task['updatedAt'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_tasks(tasks)
            return
    print(f"Задача с ID {task_id} не найдена")


def mark_done(task_id):
    """Меняет статус задачи на done"""
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == int(task_id):
            task['status'] = 'done'
            task['updatedAt'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_tasks(tasks)
            return
    print(f"Задача с ID {task_id} не найдена")


def list_tasks(filter_status):
    """Выдает задчу по фильтру статусов"""
    tasks = load_tasks()
    if filter_status:
        tasks = [task for task in tasks if task['status'] == filter_status]
    return tasks


def main():
    command = sys.argv[1]

    if command == 'add':
        if len(sys.argv) < 3:
            print("Укажите описание задачи")
            return
        description = sys.argv[2]
        add_task(description)
    elif command == 'update':
        if len(sys.argv) < 4:
            print('Укажите новое описание задачи и ID задачи')
            return
        id = sys.argv[3]
        new_description = sys.argv[2]
        update_tasks(id, new_description)
    elif command == 'delete':
        if len(sys.argv) < 3:
            print('Укажите ID, которое хотите удалить')
            return
        id = sys.argv[2]
        delete_task(id)
    elif command == 'in_progress':
        if len(sys.argv) < 3:
            print('Укажите ID задачи')
            return
        id = sys.argv[2]
        mark_in_progress(id)
    elif command == 'done':
        if len(sys.argv) < 3:
            print('Укажите ID задачи')
            return
        id = sys.argv[2]
        mark_done(id)
    elif command == 'filter_tasks':
        if len(sys.argv) < 3:
            print('Укажите статус, по которому вы хотите фильровать задачи')
            return
        filter = sys.argv[2]
        print(list_tasks(filter))


if __name__ == "__main__":
    main()
