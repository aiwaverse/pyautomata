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

    def test_break_word(self):
        word = "aaabbbbaaa"
        assert TestAutomata.aut.break_word(word) == list(word)

    def test_check_word_accept(self):
        assert TestAutomata.aut.check_word("baaaa")[0]
        assert TestAutomata.aut.check_word("baabbababaaa")[0]
        assert TestAutomata.aut.check_word("a")[0]
        assert TestAutomata.aut.check_word("baabaaa")[0]
        assert TestAutomata.aut.check_word("bbaaaaaaaaabaa")[0]

    def test_check_word_reject(self):
        assert not TestAutomata.aut.check_word("aabbb")[0]
        assert not TestAutomata.aut.check_word("abab")[0]
        assert not TestAutomata.aut.check_word("aab")[0]
        assert not TestAutomata.aut.check_word("bab")[0]
        assert not TestAutomata.aut.check_word("")[0]

    def test_check_word_accept_path(self):
        word = "baaaa"
        path = ["q0", "b", "q2", "a", "q3", "a", "q3", "a", "q3", "a", "q3"]
        assert TestAutomata.aut.check_word(word)[1] == path

    def test_check_word_reject_non_final(self):
        assert (
            TestAutomata.aut.check_word("ab")[1]
            == "Program ended on non-final state q2."
        )

    def test_check_word_reject_undefined(self):
        assert (
            TestAutomata.aut.check_word("aaa")[1]
            == "Program ended with undefined state at state q1 with element a."
        )
