
from pathlib import Path

# Корневая папка проекта
BASE_DIR = Path(__file__).resolve().parent

# Папки проекта
DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "reports"
LOG_DIR = BASE_DIR / "logs"

# Создаем папки автоматически
REPORT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Файлы проекта
REPORT_FILE = REPORT_DIR / "summary_report.csv"
LOG_FILE = LOG_DIR / "errors.log"

# Настройки анализа
STATUS_COLUMN = "status"
DELIVERED_STATUS = "Delivered"

# Обязательные столбцы
REQUIRED_COLUMNS = [
    "order_id",
    "status",
    "total_amount"
]
