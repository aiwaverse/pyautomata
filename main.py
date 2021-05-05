"""
The main module of the program
To run the program, simply run this file,
after installing the dependencies
"""
import PySimpleGUI as sg

from pyautomata import AutomataGUI


def main():
    """
    The main function, basically handles everything
    """
    gui = AutomataGUI()
    while True:
        event, values = gui.read()
        if event in (sg.WIN_CLOSED, "Close"):
            break
        if event == "-AUTOMATA-SUBMIT-":
            gui.create_automata(values["-AUTOMATA-FILE-"])
        elif event == "-WORD-FILE-SUBMIT-" and gui.automata:
            gui.test_word_pairs(values["-WORD-FILE-"])
        elif event == "-WORD-BUT-" and gui.automata:
            gui.test_word(values["-WORD-INPUT-"])


if __name__ == "__main__":
    main()
