
from src.analyzer import OrderAnalyzer


def main():
    """
    Точка входа в программу.
    """

    analyzer = OrderAnalyzer()

    processed_files, error_files = analyzer.process_all_files()

    print()
    print("Обработка завершена.")
    print(f"Успешно обработано файлов: {processed_files}")
    print(f"Файлов с ошибками: {error_files}")


if __name__ == "__main__":
    main()
