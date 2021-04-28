from pyautomata import MinimizedAutomata  # pylint: disable=import-error


class TestMinimizedAutomata:
    def setup_method(self):
        self.info = {
            "name": "AUTÔMATO",
            "states": ["q0", "q1", "q2", "q3"],
            "alphabet": ["a", "b"],
            "initial_state": "q0",
            "final_states": ["q1"],
        }
        self.program_function = {
            ("q0", "a"): "q1",
            ("q0", "b"): "q3",
            ("q1", "a"): "q1",
            ("q1", "b"): "q1",
            ("q2", "a"): "q0",
            ("q2", "b"): "q1",
            ("q3", "a"): "q3",
            ("q3", "b"): "q3",
        }
        self.aut = MinimizedAutomata(self.program_function, **self.info)

    def test_unreachable_states(self):
        assert self.aut.unreacheable_states() == ["q2"]

    def test_remove_unreachable_states(self):
        self.aut.remove_unreachable_states()
        assert self.aut.program_function == {
            ("q0", "a"): "q1",
            ("q0", "b"): "q3",
            ("q1", "a"): "q1",
            ("q1", "b"): "q1",
            ("q3", "a"): "q3",
            ("q3", "b"): "q3",
        }
