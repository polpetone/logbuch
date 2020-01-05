from src.service.TastService import TaskService

if __name__ == "__main__":
    task_service = TaskService()

    task0 = task_service.create_task("Some Task")
    task1 = task_service.create_task("Some Task2")
    task0.change_status(status="CLOSED")
    task_service.save_tasks()

    tasks = task_service.get_tasks()
    print(tasks)
