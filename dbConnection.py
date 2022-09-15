from getpass import getpass
from mysql.connector import connect, Error
import PySimpleGUI as sg

try:
    connection = connect(
        host="34.148.97.227",
        user=input("Enter username: "),
        password=getpass("Enter password: "),
        database="siem",
    )
    print(connection)

except Error as e:
    print(e)
mainLayout = [
    [sg.Text("Actions")],
    [sg.Button("Add entry"), sg.Button("Get entry")]
]

margin = (100, 50)


def spawnMain():
    return sg.Window("DB Interface", mainLayout, margins=margin)


def spawnAddEntry():
    return sg.Window("Add entry", layout=generateEntryLayout(), margins=margin, return_keyboard_events=True, default_element_size=(8, 10))


def generateEntryLayout():
    textBoxWidth = 8
    return [
        [sg.Text("Host_id"), sg.Text("Severity"), sg.Text(
            "Assigned_id"), sg.Text("Short_desc"), sg.Text("Long_desc")],
        [sg.InputText(""), sg.InputText(
            ""), sg.InputText(""), sg.InputText(""), sg.InputText("")]
    ]


window = spawnMain()
while True:
    event, values = window.read()
    if event == "Add entry":
        window.close()
        window = spawnAddEntry()
    if event == "Return":
        window.close()
        window = spawnMain()
    if event == "Return:36":
        print(values)
        window.close()
        window = spawnMain()
    if event == sg.WIN_CLOSED:
        print("Closing")
        break
    else:
        print(event)
