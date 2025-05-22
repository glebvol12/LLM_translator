import subprocess
import threading
import time
import os
from pathlib import Path


#Запуск FastAPI сервера
def run_backend():
    backend_path = Path(__file__).parent 
    os.chdir(backend_path)
    subprocess.run(["python", "backend.py"], shell=True)
    
#Запуск Streamlit интерфейса
def run_frontend():
    time.sleep(2)
    frontend_path = Path(__file__).parent 
    os.chdir(frontend_path)
    subprocess.run(["streamlit", "run", "frontend.py"], shell=True)


if __name__ == "__main__":
    backend_thread = threading.Thread(target=run_backend)
    backend_thread.daemon = True
    backend_thread.start()
    run_frontend()