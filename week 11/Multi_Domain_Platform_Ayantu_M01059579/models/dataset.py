class Dataset:
    def __init__(self, dataset_id: int, name: str, size_bytes: int, rows: int, source: str):
        self.__id = dataset_id
        self.__name = name
        self.__size_bytes = size_bytes
        self.__rows = rows
        self.__source = source

    def calculate_size_mb(self) -> float:
        return self.__size_bytes / (1024 * 1024)

    def get_source(self) -> str:
        return self.__source

    def get_name(self) -> str:
        return self.__name

    def get_rows(self) -> int:
        return self.__rows

    def __str__(self):
        return f"Dataset {self.__id}: {self.__name}"
