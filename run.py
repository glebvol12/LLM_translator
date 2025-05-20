import subprocess
import threading
import time
import os
from pathlib import Path

def run_backend():
    """Запуск FastAPI сервера"""
    backend_path = Path(__file__).parent 
    os.chdir(backend_path)
    subprocess.run(["python", "backend.py"], shell=True)
    

def run_frontend():
    """Запуск Streamlit интерфейса"""
    # Даем бэкенду время на запуск
    time.sleep(2)
    
    frontend_path = Path(__file__).parent 
    os.chdir(frontend_path)
    subprocess.run(["streamlit", "run", "frontend.py"], shell=True)

if __name__ == "__main__":
    # Запускаем бэкенд в отдельном потоке
    backend_thread = threading.Thread(target=run_backend)
    backend_thread.daemon = True
    backend_thread.start()

    # Запускаем фронтенд в основном потоке
    run_frontend()