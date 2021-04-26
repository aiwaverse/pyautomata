# %%
import PySimpleGUI as sg


def setup() -> sg.Window:
    sg.theme("DarkGrey8")
    layout = [
        [
            sg.Text("Autômato: "),
            sg.Text("Não carregado", key="-AUTOMATA-LOADED-"),
        ],
        [sg.Text("Palavra:"), sg.Text("", key="-WORD-TO-TEST-")],
        [
            sg.InputText(default_text="Escreva aqui a palavra a ser testada."),
            sg.Button(button_text="Testar", key="-WORD-BUT-", disabled=True),
        ],
        [
            sg.Text("Arquivo Autômato", size=(16, 1)),
            sg.Input(key="-AUTOMATA-FILE-"),
            sg.FileBrowse(),
            sg.Submit(key="-AUTOMATA-SUBMIT-"),
        ],
        [
            sg.Text("Arquivo Palavras", size=(16, 1)),
            sg.Input(key="-WORD-FILE-"),
            sg.FileBrowse(),
            sg.Submit(key="-WORD-FILE-SUBMIT-"),
        ],
    ]
    return sg.Window("Pyautomata", layout)


# %%
if __name__ == "__main__":
    w = setup()
    while True:
        event, values = w.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == "AUTOMATA-SUBMIT":
            break
    w.close()
