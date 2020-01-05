from src.service.TastService import TaskService

if __name__ == "__main__":
    task_service = TaskService()

    task_service.create_task("Some Task")
    task_service.create_task("Some Task2")
    task_service.save_tasks()

    tasks = task_service.get_tasks()
    print(tasks)
