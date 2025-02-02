import matplotlib.pyplot as plt
import pandas as pd

"""Операции:
1. Вставка (insert) — добавление новой пары "ключ-значение" в массив.
2. Поиск (get) — поиск значения по ключу.
3. Удаление (remove) — удаление пары по ключу.
4. Проверка существования (contains) — проверка, существует ли пара с данным ключом.
5. Обновление (update) — изменение значения по ключу.

Хэш-таблица является эффективной структурой данных для ассоциативного массива, так как операции вставки, поиска и
удаления могут быть выполнены за время O(1) в среднем, если выбрана хорошая хеш-функция, которая минимизирует количество коллизий."""


def is_prime(a):
    if a % 2 == 0:
        return a == 2
    d = 3
    while d * d <= a and a % d != 0:
        d += 2
    return d * d > a


def next_prime(num):
    while True:
        if is_prime(num):
            return num
        num += 1


class HashTable:
    def __init__(self, size=11):
        self.size = size
        self.table = [None] * self.size
        self.element_count = 0

    def _hash(self, key):
        return hash(key) % self.size

    def add(self, key, value):
        index = self._hash(key)
        if self.table[index] is None:
            self.table[index] = []
        # Проверяем на наличие ключа в списке по этому индексу
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)  # Обновление значения
                return
        # Если ключа нет, добавляем пару (ключ, значение)
        self.table[index].append((key, value))

        self.element_count += 1

        if self.element_count / self.size > 0.75:
            self.resize()

    def get(self, key):
        index = self._hash(key)
        if self.table[index] is None:
            return None
        for k, v in self.table[index]:
            if k == key:
                return v
        return None

    def remove(self, key):
        index = self._hash(key)
        if self.table[index] is None:
            return
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                del self.table[index][i]  # Удаляем пару
                return

    def contains(self, key):
        index = self._hash(key)
        if self.table[index] is None:
            return False
        for k, v in self.table[index]:
            if k == key:
                return True
        return False

    def resize(self):
        old_table = self.table
        self.size = next_prime(self.size * 2)
        self.table = [None for i in range(self.size)]
        self.element_count = 0

        for entry in old_table:
            if entry is not None:
                key, value = entry
                self.add(key, value)

    def __str__(self):
        result = []
        for elem in self.table:
            if elem is not None:
                for k, v in elem:
                    result.append(f"Key: {k}, Value: {v}")
        return "\n".join(result)


"""Визуализация хэш-таблицы в виде таблицы с помощью matplotlib."""
def visualize_hash_table(hash_table):
    data = []

    # Сбор данных из хэш-таблицы
    for i, bucket in enumerate(hash_table.table):
        if bucket is None or len(bucket) == 0:
            data.append([f"Slot {i}", "Пусто", "—"])
        else:
            for key, value in bucket:
                data.append([f"Slot {i}", key, value])

    # Создание DataFrame для визуализации
    df = pd.DataFrame(data, columns=["Слот", "Ключ", "Значение"])

    # Автоматическая настройка размера таблицы
    fig, ax = plt.subplots(figsize=(15, min(len(df) * 0.5, 10)))
    ax.axis("tight")
    ax.axis("off")
    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        cellLoc="center",
        loc="center",
        colColours=["#f5f3c9", "#c2efff", "#e4c2ff"],
    )

    # Настройка шрифта и ширины колонок
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(df.columns))))

    # Увеличение высоты ячеек
    for key, cell in table.get_celld().items():
        cell.set_height(0.035)

    plt.show()


if __name__ == "__main__":
    # Инициализация хэш-таблицы
    students_grades = HashTable()

    # Добавление студентов и их оценок
    students_grades.add("Alice", 85)
    students_grades.add("Bob", 90)
    students_grades.add("Charlie", 78)

    # Получение оценок студентов
    print(f"Alice's grade: {students_grades.get('Alice')}")
    print(f"Bob's grade: {students_grades.get('Bob')}")
    print(f"Charlie's grade: {students_grades.get('Charlie')}")

    # Проверка, существует ли студент с такой оценкой
    print(f"Does Alice exist? {students_grades.contains('Alice')}")
    print(f"Does David exist? {students_grades.contains('David')}")

    # Обновление оценки студента
    students_grades.add("Alice", 92)  # Обновление оценки Alice

    # Проверка обновленной оценки
    print(f"Alice's updated grade: {students_grades.get('Alice')}")

    # Удаление студента из хэш-таблицы
    students_grades.remove("Bob")
    print(f"Does Bob exist after removal? {students_grades.contains('Bob')}")

    # Вывод таблицы в консоль
    print()
    print(students_grades)

    visualize_hash_table(students_grades)
