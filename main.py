"""
The main module of the program
To run the program, simply run this file,
after installing the dependencies
"""
import PySimpleGUI as sg

from pyautomata.gui.automata_gui import (create_automata, read_word_file,
                                         setup, test_word, test_word_pairs)


def main():
    """
    The main function, basically handles everything
    """
    aut_window = setup()
    automata = None
    while True:
        event, values = aut_window.read()
        if event in (sg.WIN_CLOSED, "Close"):
            break
        if event == "-AUTOMATA-SUBMIT-":
            automata = create_automata(aut_window, values["-AUTOMATA-FILE-"])
        elif event == "-WORD-FILE-SUBMIT-" and automata:
            word_pairs = read_word_file(values["-WORD-FILE-"])
            test_word_pairs(automata, word_pairs)
        elif event == "-WORD-BUT-" and automata:
            test_word(aut_window, values["-WORD-INPUT-"], automata)
    aut_window.close()


if __name__ == "__main__":
    main()
