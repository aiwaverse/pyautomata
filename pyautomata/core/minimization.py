"""
The Minimization module contains the MinimizedAutomata class.
This class is responsible for handling the DFA minimization,
with removal of unreachable states and the unification
of non-distinguishable states.
"""
import copy
from typing import Dict, List, Set, Tuple

from pyautomata import Automata  # pylint: disable=import-error


class MinimizedAutomata(Automata):
    """
    Class that does the DFA minimization.
    Done automatically on constructor, no further action needed.
    """
    def __init__(
        self, program_function: Dict[Tuple[str, str], str], **kwargs
    ) -> None:
        super().__init__(program_function, **kwargs)
        self.remove_unreachable_states()
        self.unify_states()

    def remove_unreachable_states(self) -> None:
        """
        Removes the unreachable states of the Automata
        """
        states = self.unreacheable_states()
        for state in states:
            for c in self.alphabet:
                if (state, c) in self.program_function:
                    self.program_function.pop((state, c))

    def unreacheable_states(self) -> List[str]:
        """
        Determines the unreachable states of the Automata
        | -> set union
        & -> set intersection
        - -> set difference
        """
        reacheable_states: Set[str] = set([self.initial_state])
        new_states: Set[str] = set([self.initial_state])
        while new_states:
            temp: Set[str] = set()
            for q in new_states:
                for c in self.alphabet:
                    p = self.program_function.get((q, c), "")
                    if not p:
                        continue
                    temp = temp | set([p])
            new_states = temp - reacheable_states
            reacheable_states = reacheable_states | new_states
        unreachable_states = set(self.states) - reacheable_states
        return list(unreachable_states)

    def make_state_name(self, states: frozenset[str]) -> str:
        """
        Makes the new name for the set of states, possibly with just one state
        This is made to guarantee the name are always in the same order
        """
        seen = {}
        new_list = [seen.setdefault(x, x) for x in states if x not in seen]
        return "".join(new_list)

    def unify_states(self) -> None:
        """
        Using the equivalency classes of the hopcroft
        algorithm, unifies non-distinguishable states
        """
        equivalency_classes = self.hopcroft_alogrithm()
        equivalency_dict = {}
        new_states = []
        new_final_states = set()
        for ec in equivalency_classes:
            # we make the new name, and add it to the new_states
            name = self.make_state_name(ec)
            new_states.append(name)
            for elem in ec:
                # to each element in the eq class
                # we add it to a dict with the right name
                equivalency_dict[elem] = name
                if elem in self.final_states:
                    # we also add it to the new list of final_states
                    # a set to make my life easier
                    new_final_states.add(name)
                if elem == self.initial_state:
                    # if that element is an initial state, so the new
                    # initial state changes name
                    self.initial_state = name
        new_program_function = {}
        for (state, c), result_state in self.program_function.items():
            new_program_function[
                (equivalency_dict[state], c)
            ] = equivalency_dict[result_state]
        self.final_states = list(new_final_states)
        self.states = new_states
        self.program_function = new_program_function

    def hopcroft_alogrithm(self) -> Set[frozenset[str]]:
        """
        The Hopcroft Algorithm, following the pseudocode
        found in:
        https://en.wikipedia.org/wiki/DFA_minimization#Hopcroft's_algorithm
        Adapted to Python (new variables, frozen sets)
        """
        final_states_set = frozenset(self.final_states)
        non_final_states_set = frozenset(self.states) - frozenset(
            self.final_states
        )
        p: Set[frozenset[str]] = set([final_states_set, non_final_states_set])
        new_p = copy.deepcopy(p)
        w: Set[frozenset[str]] = set([final_states_set, non_final_states_set])
        while w:
            a = w.pop()
            for c in self.alphabet:
                x = {
                    state
                    for (
                        state,
                        character,
                    ), result_state in self.program_function.items()
                    if result_state in a and character == c
                }
                p = copy.deepcopy(new_p)
                for y in p:
                    if x & y == set() or y - x == set():
                        continue
                    new_p.remove(y)
                    new_p.add(frozenset(x & y))
                    new_p.add(y - x)
                    if y in w:
                        w.remove(y)
                        w.add(frozenset(x & y))
                        w.add(y - x)
                    else:
                        if (x & y) <= (y - x):
                            w.add(frozenset(x & y))
                        else:
                            w.add(y - x)
        return p


# %%
