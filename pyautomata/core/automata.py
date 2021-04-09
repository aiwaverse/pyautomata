from typing import List, Dict, Tuple, Union
import re


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
        self.alphabet: List[str] = kwargs["alphabet"]
        self.initial_state: str = kwargs["initial_state"]
        self.final_states: List[str] = kwargs["final_states"]
        self.program_function: Dict[Tuple[str, str], str] = program_function

    def break_word(self, word: str) -> List[str]:
        """
        Breaks a word into it's alphabet elements
        """
        re_pattern = "|".join(self.alphabet)
        return re.findall(re_pattern, word)

    def check_word(self, word: str) -> Tuple[bool, Union[str, List[str]]]:
        """
        Checks if a word is part of the language.
        Returns True or False, in case of True, with the second element of
        the tuple representing the path it took to reach the final state
        In case of False, the second element is the reason why it was rejected
        """
        curr_state = self.initial_state
        path = [curr_state]
        for elem in self.break_word(word):
            path.append(elem)
            try:
                curr_state = self.program_function[(curr_state, elem)]
            except KeyError:
                return_string = "Program ended with undefined state at state"
                return (
                    False,
                    f"{return_string} {curr_state} with element {elem}.",
                )
            path.append(curr_state)
        if curr_state not in self.final_states:
            return (False, f"Program ended on non-final state {curr_state}.")
        return (True, path)
