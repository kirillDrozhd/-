#подключение библиотек
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import json

#создание элементов интерфейса
app = QApplication([])
win = QWidget()
win.setWindowTitle("Умные заметки") 
win.resize(800,450)
note_edit = QTextEdit()
note_text = QLabel("Список заметок")
notes_list  =  QListWidget()
create_butt = QPushButton("Создать заметку")
delete_butt = QPushButton("Удатить заметку")
save_butt = QPushButton("Сохранить заметку")
tag_text = QLabel("Список тегов")
tags_list  =  QListWidget()
input_tag = QLineEdit()
input_tag.setPlaceholderText("Введите тег...")
add_butt = QPushButton("Добавить к заметке")
unf_butt = QPushButton("Открепить от заметки")
find_butt = QPushButton("Искать заметку по тегу")

#расстановка по линиям
layout_main = QHBoxLayout()
layout_V1 = QVBoxLayout()
layout_V2 = QVBoxLayout()
layout_butt1 = QHBoxLayout()
layout_butt2 = QHBoxLayout()

layout_V1.addWidget(note_edit)
layout_V2.addWidget(note_text)
layout_V2.addWidget(notes_list)
layout_butt1.addWidget(create_butt)
layout_butt1.addWidget(delete_butt)
layout_V2.addLayout(layout_butt1)

layout_V2.addWidget(save_butt)
layout_V2.addWidget(tag_text)
layout_V2.addWidget(input_tag)
layout_V2.addWidget(tags_list)
layout_butt2.addWidget(add_butt)
layout_butt2.addWidget(unf_butt)
layout_V2.addLayout(layout_butt2)
layout_V2.addWidget(find_butt)



layout_main.addLayout(layout_V1, stretch = 2)
layout_main.addLayout(layout_V2, stretch = 1)

win.setLayout(layout_main)

#функции
def show_note():
    key = notes_list.selectedItems()[0].text()
    note_edit.setText(note[key]["текст"])
    tags_list.clear()
    tags_list.addItems(note[key]["теги"])

def new_note():
    note_name, ok = QInputDialog.getText(win,"Добавить заметку","Название заметки: ")
    if ok and note_name != "":
        note[note_name] = {"текст": '', 'теги': []}
        notes_list.addItem(note_name)
        tags_list.addItems(note[note_name]["теги"])

def del_note():
    if notes_list.selectedItems():
        key = notes_list.selectedItems()[0].text()
        del note[key]
        notes_list.clear()
        tags_list.clear()
        note_edit.clear()
        notes_list.addItems(note)
        with open("notes.json","w", encoding = "UTF-8") as file:
            json.dump(note, file, ensure_ascii = False)
    else:
        print("Заметка не выбрана")


def save_note():
    if notes_list.selectedItems():
        key = notes_list.selectedItems()[0].text()
        note[key]["текст"] = note_edit.toPlainText()
        with open("notes.json","w", encoding = "UTF-8") as file:
            json.dump(note, file,ensure_ascii = False)
    else:
        print("Заметка не выбрана")


def add_tag():
    if notes_list.selectedItems():
        key = notes_list.selectedItems()[0].text()
        tag = input_tag.text()
        if not tag in note[key]["теги"]:
            note[key]["теги"].append(tag)
            tags_list.addItem(tag)
            input_tag.clear()
            with open("notes.json","w", encoding = "UTF-8") as file:
                json.dump(note, file, ensure_ascii = False)
    else:
        print("Заметка не выбрана")
    

def unf_tag():
    if tags_list.selectedItems():
        key = notes_list.selectedItems()[0].text()
        tag = tags_list.selectedItems()[0].text()
        note[key]["теги"].remove(tag)
        tags_list.clear()
        tags_list.addItems(note[key]["теги"])
        with open("notes.json","w", encoding = "UTF-8") as file:
            json.dump(note, file,ensure_ascii = False)
    else:
        print("Тег не выбран!")

def find_tag():
    tag = input_tag.text()
    if find_butt.text() == "Искать заметку по тегу" and tag:
        notes_filtered = dict()
        for note1 in note:
            if tag in note[note1]["теги"]:
                notes_filtered[note1] = note[note1]
        find_butt.setText("Сбросить поиск")
        notes_list.clear()
        tags_list.clear()
        notes_list.addItems(notes_filtered)
    elif find_butt.text() == "Сбросить поиск":
        input_tag.clear()
        notes_list.clear()
        tags_list.clear()
        notes_list.addItems(note)
        find_butt.setText("Искать заметку по тегу")

#читаем json
try:  
    with open("notes.json","r", encoding = "UTF-8") as file:
        note = json.load(file)
    notes_list.addItems(note)
except:
    #словарь
    note = {
        "Добро пожаловать!":{
            "текст":"Привет",
            "теги":["Приветствие","привет"]
        }
    }
    # записываем в json
    with open("notes.json","w", encoding = "UTF-8") as file:
        json.dump(note, file)
    


#обработка нажатий
notes_list.itemClicked.connect(show_note)
create_butt.clicked.connect(new_note)
delete_butt.clicked.connect(del_note)
save_butt.clicked.connect(save_note)
add_butt.clicked.connect(add_tag)
unf_butt.clicked.connect(unf_tag)
find_butt.clicked.connect(find_tag)
#запуск приложения
win.show()
app.exec_()