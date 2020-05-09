import json
import uuid
from scipy import spatial
from ui import *

DATABASE_NAME = 'vectors.json'  # Название файла со списком векторов


# Главный класс окна приложения
class Main(QtWidgets.QMainWindow, GuiMainWindow):

    # Инициализация окна
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setup(self)    # Построение элементов интерфейса (в ui.py)

        # Прикрепление к кнопкам функций, которые будут вызываться по нажатию
        self.add_push.clicked.connect(self.add_vector)
        self.remove_push.clicked.connect(self.remove_vector)
        self.target_push.clicked.connect(self.find_closest)

        # Загрузка списка векторов и их названий из файла-списка
        self.uuids, self.vectors = self.load_json()
        # в self.uuids хранятся названия векторов, а в self.vectors - координаты
        # данные одного вектора лежат под одним индексом

        # добавляем все загруженные вектора в список в интерфейсе
        for i in range(len(self.uuids)):
            self.itemList.addItem(str(self.vectors[i]) + " (" + str(self.uuids[i]) + ")")

    # Метод добавляет новый вектор в список векторов
    def add_vector(self):
        try:    # Проверяем на то, что в полня ввода введены именно числа и вообще что там что-то есть
            x = float(self.add_x.text())
            y = float(self.add_y.text())
            z = float(self.add_z.text())
        except:     # Иначе выкидываем диалоговое окно с уведомлением ошибки
            message("Unnable to parse coordinates!")
            return

        index = len(self.vectors)   # Получаем текущий размер списка векторов
        self.vectors.append([x, y, z])  # Добавляем координаты нового вектора в массив координат векторов
        self.uuids.append(str(index))   # Добавляем название нового вектора в массив названий
        self.itemList.addItem(str(self.vectors[index]) + " (" + str(index) + ")")   # Добавляем вектор в список в UI
        self.save_json()    # Сохраняем изменения в файл сразу

    # Метод удаляет вектор из списка
    def remove_vector(self):
        uuid = self.remove_id.text()
        if len(uuid) == 0:  # Проверяем, не пуста ли строка ввода названия вектора
            message("Type name before remove!!11")
            return

        # Ищем индекс вектора по его названию
        i = 0
        found = False
        for id in self.uuids:
            if id == uuid:
                found = True
                break
            i = i + 1

        # Если название не найдено, то выкидываем уведомление
        if not found:
            message("Unnable to find vector named '" + uuid + "'!")
            return

        # В ином случае удаляем по индексу вектор из обоих массивов
        del self.uuids[i]
        del self.vectors[i]

        # Так же очищаем весь список в интерфейсе и добавляем элементы заново
        self.itemList.clear()
        for i in range(len(self.uuids)):
            self.itemList.addItem(str(self.vectors[i]) + " (" + str(self.uuids[i]) + ")")

        # Сохраняем произошедшее
        self.save_json()

    # Метод поиска ближайшего вектора
    def find_closest(self):
        if len(self.vectors) == 0:  # Проверяем есть ли вообще векторы в списке и кидаем ошибку есичо
            message("There is no vectors in database")
            return

        try:    # Проверяем введенные данные на действительность (числа ли это)
            x = float(self.target_x.text())
            y = float(self.target_y.text())
            z = float(self.target_z.text())
        except: # Иначе кидаем уведомление
            message("Unnable to parse coordinates!")
            return

        # Ищем ближайший вектор модов k-d дерева
        tree = spatial.KDTree(self.vectors)
        result = tree.query([x, y, z]) # Получаем результат в формате  [дистанция до ближайшего, его индекс]

        # Делаем список названий ближайших векторов (на случай одинаковых векторов с одними координатами)
        nearest_vectors = ''
        for i in range(len(self.vectors)):
            if self.vectors[i] == self.vectors[result[1]]:
                nearest_vectors = nearest_vectors + str(self.uuids[i]) + ', '

        # Выводим сообщение со все информацией
        message("Nearest coordinates: " + str(self.vectors[result[1]]) + "\nNearest IDs: " + nearest_vectors[:-2] + "\nDistance: " + str(result[0]))

    # Метод сохранения списка векторов в JSON-файл
    def load_json(self):
        with open(DATABASE_NAME) as json_file:  # Открываем файл по его названию
            data = json.load(json_file)     # Загружаем файл в переменную
            length = len(data['vectors'])   # Высчитываем кол-во загруженных векторов
            vectors = [[None] * 3] * length     # Создаем будущий массив координат
            uuids = ['empty'] * length      # Создаем массив названий

            print(data)     # Информация для отладки

            # Переносим информацию, загруженную из файла в массив координат
            i = 0
            for vec in data['vectors']:
                vectors[i] = [float(vec['x']), float(vec['y']), float(vec['z'])]
                i = i + 1

            # Переносим информацию, загруженную из файла в массив названий
            i = 0
            for p in data['vectors']:
                uuids[i] = p['uuid']
                i = i + 1

            # Возвращаем оба массива с данными
            return uuids, vectors

    # Сохраняем данные в JSON-файл
    def save_json(self):
        with open(DATABASE_NAME, 'w') as outfile:   # Открываем файл с функций записи в него
            data = {'vectors': []}  # Создаем будущий словарь для записи
            length = len(self.vectors)  # Считаем кол-во векторов

            # Помещаем все данные о векторах в словарь для записи
            for i in range(length):
                data['vectors'].append({
                    'uuid': self.uuids[i],
                    'x': self.vectors[i][0],
                    'y': self.vectors[i][1],
                    'z': self.vectors[i][2]
                })

            # Записываем все данные в файл
            json.dump(data, outfile)


# Функция вывода информации в уведомлениии
def message(text):
    msg = QtWidgets.QMessageBox()
    msg.setWindowTitle('Message')
    msg.setText(text)
    msg.exec()


# Главная функция, которая открывает окно и запускает приложение
if __name__ == '__main__':
    import sys

    sys._excepthook = sys.excepthook
    def exception_hook(exctype, value, traceback):
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)
    sys.excepthook = exception_hook

    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())



