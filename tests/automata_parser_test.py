import os
import pytest

from pyautomata import AutomataParser  # pylint: disable=import-error


class TestAutomataParser:
    """
    AutomataParser test class
    Run with python3.9 -m pytest
    """

    test_string = "AUTÔMATO=({q0,q1,q2,q3},{a,b},Prog,q0,{q1,q3})\n\
                   Prog\n\
                   (q0,a)=q1\n\
                   (q0,b)=q2\n\
                   (q1,b)=q2\n\
                   (q2,a)=q3\n\
                   (q2,b)=q2\n\
                   (q3,a)=q3\n\
                   (q3,b)=q2"
    p = AutomataParser(test_string)
    description_dict, function_dict = p.parse()

    def test_name(self):
        assert TestAutomataParser.description_dict["name"] == "AUTÔMATO"

    def test_states(self):
        assert TestAutomataParser.description_dict["states"] == [
            "q0",
            "q1",
            "q2",
            "q3",
        ]

    def test_alphabet(self):
        assert TestAutomataParser.description_dict["alphabet"] == ["a", "b"]

    def test_initial_state(self):
        assert TestAutomataParser.description_dict["initial_state"] == "q0"

    def test_final_states(self):
        assert TestAutomataParser.description_dict["final_states"], [
            "q1",
            "q3",
        ]

    def test_transitions(self):
        assert TestAutomataParser.function_dict[("q0", "a")] == "q1"
        assert TestAutomataParser.function_dict[("q0", "b")] == "q2"
        assert TestAutomataParser.function_dict[("q1", "b")] == "q2"
        assert TestAutomataParser.function_dict[("q2", "a")] == "q3"
        assert TestAutomataParser.function_dict[("q2", "b")] == "q2"
        assert TestAutomataParser.function_dict[("q3", "a")] == "q3"
        assert TestAutomataParser.function_dict[("q3", "b")] == "q2"
