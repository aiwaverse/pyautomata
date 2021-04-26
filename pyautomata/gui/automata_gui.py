from typing import List, Tuple, Union

import pyautomata  # pylint: disable=import-error
import PySimpleGUI as sg
from more_itertools import grouper


def create_automata(window: sg.Window, file: str) -> pyautomata.Automata:
    """
    Creates the automata via the Parser
    Updates the text and buttons on screen
    """
    p = pyautomata.AutomataParser(file_name=file)
    description, function_program = p.parse()
    window["-AUTOMATA-LOADED-"].update("Loaded")
    window["-WORD-BUT-"].update(disabled=False)
    window["-WORD-FILE-SUBMIT-"].update(disabled=False)
    return pyautomata.Automata(function_program, **description)


def create_pair_result_window(pairs: List[Tuple[str, str]]) -> None:
    """
    Creates a window to display the accepted pairs
    """
    pair_string = ""
    for word1, word2 in pairs:
        pair_string += f"{word1}, {word2}\n"
    layout = [
            [sg.Text(f"Accepted pairs:")],
            [sg.Text(pair_string)],
            [sg.Button("Ok")],
        ]
    window = sg.Window("Pyautomata", layout)
    while True:
        event, _ = window.read()
        if event == sg.WIN_CLOSED or event == "Ok":
            break
    window.close()


def test_word_pairs(
    aut: pyautomata.Automata, pairs: List[Tuple[str, str]]
) -> None:
    """
    Tests the pairs, and then creates a window with the valid pairs
    """
    result_pairs = []
    for word1, word2 in pairs:
        if aut.check_word(word1)[0] and aut.check_word(word2)[0]:
            result_pairs.append((word1, word2))
    create_pair_result_window(result_pairs)


def read_word_file(file: str) -> List[Tuple[str, str]]:
    """
    Uses the parser to read the word file
    """
    p = pyautomata.WordFileParser(file_name=file)
    return p.parse()


def create_result_path_string(result_path: Union[str, List[str]]) -> str:
    """
    Creates the path string, or, if it's the rejected message
    Returns the string unchanged
    """
    result = ""
    if isinstance(result_path, str):
        return result_path
    for state, element in grouper(result_path, 2):
        if element:
            result += f"{state}, {element} ->\n"
        else:
            result += str(state)
    return result


def make_result_window(
    result: bool, reason_or_path: Union[str, List[str]]
) -> None:
    """
    Makes a Window to say if the word
    Was rejected or accepted
    """
    layout = []
    result_string = create_result_path_string(reason_or_path)
    if result:
        layout = [
            [sg.Text(f"Word accepted.")],
            [sg.Text(f"Path:\n{result_string}")],
            [sg.Button("Ok")],
        ]
    else:
        layout = [
            [sg.Text(f"Word rejected.")],
            [sg.Text(f"Reason:\n{result_string}")],
            [sg.Button("Ok")],
        ]

    result_window = sg.Window("Pyautomata", layout)
    while True:
        event, _ = result_window.read()
        if event == sg.WIN_CLOSED or event == "Ok":
            break
    result_window.close()


def test_word(window: sg.Window, word: str, aut: pyautomata.Automata) -> None:
    """
    Tests a word on the automata
    And draws a window with the results
    """
    window["-WORD-TO-TEST-"].update(word)
    result, reason_or_path = aut.check_word(word)
    make_result_window(result, reason_or_path)


def setup() -> sg.Window:
    sg.theme("DarkGrey8")
    layout = [
        [
            sg.Text("Automata: "),
            sg.Text("Not loaded", key="-AUTOMATA-LOADED-"),
        ],
        [
            sg.Text("Last word:"),
            sg.Text("No word loaded", key="-WORD-TO-TEST-"),
        ],
        [
            sg.Text("Word:"),
            sg.InputText(
                key="-WORD-INPUT-",
                do_not_clear=False
                
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
        [sg.CloseButton("Close")],
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
