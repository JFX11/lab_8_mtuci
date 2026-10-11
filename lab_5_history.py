import json
import os


class History:
    """История вычислений."""

    def __init__(self, filename):
        self.filename = filename
        self.records = []
        self._load()

    def _load(self):
        """Читает записи из файла (если файл существует)."""
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as file:
                self.records = json.load(file)

    def _save(self):
        """Записывает все записи в файл."""
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(self.records, file, ensure_ascii=False, indent=2)

    def add(self, expression, result):
        """Добавляет запись и сразу сохраняет файл."""
        self.records.append({"expression": expression, "result": result})
        self._save()

    def get_all(self):
        """Возвращает копию списка записей."""
        return list(self.records)

    def clear(self):
        """Удаляет все записи."""
        self.records = []
        self._save()

