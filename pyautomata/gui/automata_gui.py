"""
The GUI functions for the program.
"""
from typing import List, Optional, Tuple, Union

import PySimpleGUI as sg
from more_itertools import grouper
import pyautomata  # pylint: disable=import-error


class AutomataGUI:
    """
    The GUI class for the program
    """

    def __init__(self) -> None:
        sg.theme("DarkGrey8")
        layout = [
            [
                sg.Text("Automata: "),
                sg.Text("Not loaded", size=(50, 1), key="-AUTOMATA-LOADED-"),
            ],
            [
                sg.Text("Last word:"),
                sg.Text("No word loaded", key="-WORD-TO-TEST-"),
            ],
            [
                sg.Text("Word:"),
                sg.InputText(key="-WORD-INPUT-", do_not_clear=False),
                sg.Button(button_text="Test", key="-WORD-BUT-", disabled=True),
            ],
            [
                sg.Text("Automata File", size=(16, 1)),
                sg.Input(key="-AUTOMATA-FILE-"),
                sg.FileBrowse(file_types=(("Text Files", "*.txt"),)),
                sg.Submit(key="-AUTOMATA-SUBMIT-"),
            ],
            [
                sg.Text("Words File", size=(16, 1)),
                sg.Input(key="-WORD-FILE-"),
                sg.FileBrowse(
                    file_types=(("Text Files", "*.txt"),),
                    disabled=True,
                    key="-WORD-FILE-BROWSER-",
                ),
                sg.Submit(key="-WORD-FILE-SUBMIT-", disabled=True),
            ],
            [sg.CloseButton("Close")],
        ]
        self._window: sg.Window = sg.Window("Pyautomata", layout)
        self._aut: Optional[pyautomata.Automata] = None

    def close(self):
        """
        Closes the window (and then deletes it for safety)
        """
        self.window.close()
        del self._window

    def read(self):
        """
        Reads the Window
        Just to not need to write instance.window.read()
        """
        return self.window.read()

    @property
    def window(self):
        """
        Returns the program window
        """
        return self._window

    @property
    def automata(self):
        """
        Returns the created Automata
        """
        return self._aut

    def create_automata(self, file: str) -> None:
        """
        Creates the automata via the Parser
        Updates the text and buttons on screen
        """
        try:
            p = pyautomata.AutomataParser(file_name=file)
            description, function_program = p.parse()
            automata = pyautomata.MinimizedAutomata(
                function_program, **description
            )
            automata.minimize()
            self._aut = automata
            self.window["-AUTOMATA-LOADED-"].update(
                f"{automata.name} (Loaded)"
            )
            self.window["-WORD-BUT-"].update(disabled=False)
            self.window["-WORD-FILE-SUBMIT-"].update(disabled=False)
            self.window["-WORD-FILE-BROWSER-"].update(disabled=False)
        except KeyError as _:
            sg.popup_error("The file was incorrectly formatted.")

    @staticmethod
    def create_pair_result_window(pairs: List[Tuple[str, str]]) -> None:
        """
        Creates a window to display the accepted pairs
        """
        pair_string = ""
        for word1, word2 in pairs:
            pair_string += f"{word1}, {word2}\n"
        layout = [
            [sg.Text("Accepted pairs:")],
            [sg.Text(pair_string)],
            [sg.Button("Ok")],
        ]
        window = sg.Window("Pyautomata", layout)
        while True:
            event, _ = window.read()
            if event in (sg.WIN_CLOSED, "Ok"):
                break
        window.close()

    def test_word_pairs(self, file: str) -> None:
        """
        Given the file
        Creates the pairs, then test them
        Opens up a new window with the results
        """
        try:
            wfp = pyautomata.WordFileParser(file_name=file)
            result_pairs = []
            for word1, word2 in wfp.parse():
                if (
                    self.automata.check_word(word1)[0]
                    and self.automata.check_word(word2)[0]
                ):
                    result_pairs.append((word1, word2))
            self.create_pair_result_window(result_pairs)
        except ValueError as ve:
            sg.popup_error(ve)

    @staticmethod
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
        self, result: bool, reason_or_path: Union[str, List[str]]
    ) -> None:
        """
        Makes a Window to say if the word
        Was rejected or accepted
        """
        layout = []
        result_string = self.create_result_path_string(reason_or_path)
        if result:
            layout = [
                [sg.Text("Word accepted.")],
                [sg.Text(f"Path:\n{result_string}")],
                [sg.Button("Ok")],
            ]
        else:
            layout = [
                [sg.Text("Word rejected.")],
                [sg.Text(f"Reason:\n{result_string}")],
                [sg.Button("Ok")],
            ]

        result_window = sg.Window("Pyautomata", layout)
        while True:
            event, _ = result_window.read()
            if event in (sg.WIN_CLOSED, "Ok"):
                break
        result_window.close()

    def test_word(self, word: str) -> None:
        """
        Tests a word on the automata
        Updates gui and draws a window with the results
        """
        try:
            result, reason_or_path = self.automata.check_word(word)
        except ValueError:
            sg.popup_error("Word contained non-alphabet tokens")
        else:
            self.window["-WORD-TO-TEST-"].update(word)
            self.make_result_window(result, reason_or_path)
