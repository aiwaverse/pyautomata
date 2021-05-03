# pylint: disable-all
from pyautomata import MinimizedAutomata


class TestMinimizedAutomata:
    def setup_method(self):
        self.info = {
            "name": "AUTÔMATO",
            "states": ["q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7"],
            "alphabet": ["a", "b"],
            "initial_state": "q0",
            "final_states": ["q2"],
        }
        self.program_function = {
            ("q0", "a"): "q1",
            ("q0", "b"): "q5",
            ("q1", "a"): "q6",
            ("q1", "b"): "q2",
            ("q2", "a"): "q0",
            ("q2", "b"): "q2",
            ("q3", "a"): "q2",
            ("q4", "a"): "q7",
            ("q4", "b"): "q5",
            ("q5", "a"): "q2",
            ("q5", "b"): "q6",
            ("q6", "b"): "q4",
            ("q7", "a"): "q6",
            ("q7", "b"): "q2",
        }
        self.aut = MinimizedAutomata(self.program_function, **self.info)

    def test_unreachable_states(self):
        assert self.aut.unreacheable_states() == {"q3"}

    def test_remove_unreachable_states(self):
        self.aut.remove_states(self.aut.unreacheable_states())
        assert self.aut.program_function == {
            ("q0", "a"): "q1",
            ("q0", "b"): "q5",
            ("q1", "a"): "q6",
            ("q1", "b"): "q2",
            ("q2", "a"): "q0",
            ("q2", "b"): "q2",
            ("q4", "a"): "q7",
            ("q4", "b"): "q5",
            ("q5", "a"): "q2",
            ("q5", "b"): "q6",
            ("q6", "b"): "q4",
            ("q7", "a"): "q6",
            ("q7", "b"): "q2",
        }

    def test_hopcroft_alogrithm(self):
        # this does not test removal of unreachable states
        # hence the inclusion of q3
        sets = self.aut.hopcroft_alogrithm()
        assert sets == {
            frozenset({"q0", "q4"}),
            frozenset({"q1", "q7"}),
            frozenset({"q2"}),
            frozenset({"q3"}),
            frozenset({"q5"}),
            frozenset({"q6"}),
        }

    def test_unify_states(self):
        # this does not test removal of unreachable states
        # hence the inclusion of q3
        self.aut.unify_states()
        assert self.aut.program_function == {
            ("q0q4", "a"): "q1q7",
            ("q0q4", "b"): "q5",
            ("q1q7", "a"): "q6",
            ("q1q7", "b"): "q2",
            ("q2", "a"): "q0q4",
            ("q2", "b"): "q2",
            ("q3", "a"): "q2",
            ("q5", "a"): "q2",
            ("q5", "b"): "q6",
            ("q6", "b"): "q0q4",
        }

    def test_minimize(self):
        self.aut.minimize()
        assert self.aut.program_function == {
            ("q0q4", "a"): "q1q7",
            ("q0q4", "b"): "q5",
            ("q1q7", "a"): "q6",
            ("q1q7", "b"): "q2",
            ("q2", "a"): "q0q4",
            ("q2", "b"): "q2",
            ("q5", "a"): "q2",
            ("q5", "b"): "q6",
            ("q6", "b"): "q0q4",
        }
