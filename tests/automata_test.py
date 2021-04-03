from pyautomata import Automata  # pylint: disable=import-error


class TestAutomata:
    info = {
        "name": "AUTÔMATO",
        "states": ["q0", "q1", "q2", "q3"],
        "alphabet": ["a", "b"],
        "initial_state": "q0",
        "final_states": ["q1", "q3"],
    }
    program_function = {
        ("q0", "a"): "q1",
        ("q0", "b"): "q2",
        ("q1", "b"): "q2",
        ("q2", "a"): "q3",
        ("q2", "b"): "q2",
        ("q3", "a"): "q3",
        ("q3", "b"): "q2",
    }
    aut = Automata(program_function, **info)

    def test_info(self):
        assert TestAutomata.info["name"] == TestAutomata.aut.name
        assert TestAutomata.info["states"] == TestAutomata.aut.states
        assert TestAutomata.info["alphabet"] == TestAutomata.aut.alphabet
        assert (
            TestAutomata.info["initial_state"]
            == TestAutomata.aut.initial_state
        )
        assert (
            TestAutomata.info["final_states"] == TestAutomata.aut.final_states
        )

    def test_funciton_program_creation(self):
        assert (
            TestAutomata.program_function == TestAutomata.aut.program_function
        )
