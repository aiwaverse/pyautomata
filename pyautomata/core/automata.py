from typing import List, Dict, Tuple


class Automata:
    """
    The class that represents an Automata
    """

    def __init__(self, program_function, **kwargs) -> None:
        """
        To initialize an Automata, pass the program function dictionary
        and the unpacked dictionary of info
        """
        self.name: str = kwargs["name"]
        self.states: List[str] = kwargs["states"]
        self.initial_state: str = kwargs["initial_state"]
        self.final_states: List[str] = kwargs["final_states"]
        self.program_function: Dict[Tuple[str, str], str] = program_function
