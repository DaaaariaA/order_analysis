
import logging

import pandas as pd

from config import (
    DATA_DIR,
    REPORT_FILE,
    LOG_FILE,
    STATUS_COLUMN,
    DELIVERED_STATUS,
    REQUIRED_COLUMNS
)


class OrderAnalyzer:
    """
    Класс для анализа CSV-файлов с заказами.
    """

    def __init__(self):
        """
        Инициализация объекта.
        """

        self.data_dir = DATA_DIR
        self.report_file = REPORT_FILE
        self.results = []

        self.setup_logger()

    def setup_logger(self):
        """
        Настраивает логирование ошибок.
        """

        logging.basicConfig(
            filename=LOG_FILE,
            level=logging.ERROR,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def load_data(self, filepath):
        """
        Загружает данные из CSV-файла.
        """

        try:
            df = pd.read_csv(filepath)
            return df

        except Exception as error:
            logging.error(f"{filepath.name}: {error}")
            return None

    def validate_data(self, df):
        """
        Проверяет корректность данных.
        """

        # Проверка на пустой файл
        if df.empty:
            raise ValueError("Файл пуст.")

        # Проверка обязательных столбцов
        for column in REQUIRED_COLUMNS:
            if column not in df.columns:
                raise ValueError(f"Отсутствует столбец '{column}'.")

        # Проверка числового столбца
        df["total_amount"] = pd.to_numeric(
            df["total_amount"],
            errors="raise"
        )

        return df

    def filter_orders(self, df):
        """
        Оставляет только доставленные заказы.
        """

        delivered_orders = df[df[STATUS_COLUMN] == DELIVERED_STATUS]

        return delivered_orders

    def calculate_metrics(self, df):
        """
        Рассчитывает основные метрики.
        """

        metrics = {
            "total_revenue": df["total_amount"].sum(),
            "average_order": df["total_amount"].mean(),
            "orders_count": len(df)
        }

        return metrics

    def process_file(self, filepath):
        """
        Обрабатывает один CSV-файл.
        """

        try:
            df = self.load_data(filepath)
            if df is None:
                return None

            df = self.validate_data(df)

            delivered_orders = self.filter_orders(df)

            metrics = self.calculate_metrics(delivered_orders)

            metrics["file_name"] = filepath.name

            return metrics

        except Exception as error:
            logging.error(f"{filepath.name}: {error}")
            return None

    def save_report(self):
        """
        Сохраняет итоговый отчет в CSV-файл.
        """

        report = pd.DataFrame(self.results)
        report.to_csv(self.report_file, index=False)

    def process_all_files(self):
        """
        Обрабатывает все CSV-файлы из папки data.
        """

        processed_files = 0
        error_files = 0

        csv_files = sorted(self.data_dir.glob("*.csv"))

        for filepath in csv_files:
            result = self.process_file(filepath)
            if result is not None:
                self.results.append(result)
                processed_files += 1
            else:
                error_files += 1

        self.save_report()

        return processed_files, error_files       
