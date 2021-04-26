# %%
import PySimpleGUI as sg


def setup() -> sg.Window:
    sg.theme("DarkGrey8")
    layout = [
        [
            sg.Text("Automata: "),
            sg.Text("Not loaded", key="-AUTOMATA-LOADED-"),
        ],
        [
            sg.Text("Word:"),
            sg.Text("No word loaded", key="-WORD-TO-TEST-"),
        ],
        [
            sg.InputText(
                default_text="Write here the word to be tested",
                key="-WORD-INPUT-",
                do_not_clear=False,
            ),
            sg.Button(button_text="Test", key="-WORD-BUT-", disabled=True),
        ],
        [
            sg.Text("Automata File", size=(16, 1)),
            sg.Input(key="-AUTOMATA-FILE-"),
            sg.FileBrowse(),
            sg.Submit(key="-AUTOMATA-SUBMIT-"),
        ],
        [
            sg.Text("Words File", size=(16, 1)),
            sg.Input(key="-WORD-FILE-"),
            sg.FileBrowse(),
            sg.Submit(key="-WORD-FILE-SUBMIT-", disabled=True),
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
