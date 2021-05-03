"""
The Minimization module contains the MinimizedAutomata class.
This class is responsible for handling the DFA minimization,
with removal of unreachable states and the unification
of non-distinguishable states.
"""
import copy
from typing import List, Set

from pyautomata import Automata  # pylint: disable=import-error


class MinimizedAutomata(Automata):
    """
    Class that does the DFA minimization.
    Opted for a method that minimizes, to faciliate tests.
    """

    def remove_unreachable_states(self) -> None:
        """
        Removes the unreachable states of the Automata
        """
        states = self.unreacheable_states()
        for state in states:
            for c in self.alphabet:
                if (state, c) in self.program_function:
                    self.program_function.pop((state, c))

    def minimize(self):
        """
        Does the minimization by doing all the steps
        """
        self.remove_unreachable_states()
        self.unify_states()

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

    @staticmethod
    def make_state_name(states: frozenset[str]) -> str:
        """
        Makes the new name for the set of states, possibly with just one state
        This is made to guarantee the name are always in the same order
        """
        seen = {}
        new_list = [seen.setdefault(x, x) for x in states if x not in seen]
        new_list.sort()
        return "".join(new_list)

    def unify_states(self) -> None:
        """
        Using the equivalency classes of the hopcroft
        algorithm, unifies non-distinguishable states
        """
        # pylint: disable=attribute-defined-outside-init
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
        # the sets need to be frozen, because python
        # needs set elements to be hashable, and mutable
        # types can't be hashed for it
        final_states_set = frozenset(self.final_states)
        non_final_states_set = frozenset(self.states) - frozenset(
            self.final_states
        )
        p: Set[frozenset[str]] = set([final_states_set, non_final_states_set])
        # new_p is used because p needs to change, but
        # python can't have a collection being changed mid-iteration
        new_p = copy.deepcopy(p)
        w: Set[frozenset[str]] = set([final_states_set, non_final_states_set])
        while w:
            a = w.pop()
            # the original pseudocode just said "choose an a"
            # so, just popped one
            for c in self.alphabet:
                # this set comphrehesion basically means
                # let x = every state that a transiction with 'c'
                # that leads to a state in 'a'
                x = {
                    state
                    for (
                        state,
                        character,
                    ), result_state in self.program_function.items()
                    if result_state in a and character == c
                }
                # p needs to be new_p
                # due to shallow copy, this is the only way
                p = copy.deepcopy(new_p)
                for y in p:
                    # the comparation with empty set isn't pythonic
                    # but it seemed more on par with the pseudocode
                    if x & y == set() or y - x == set():
                        continue
                    new_p.remove(y)
                    # we used y ∩ x instead of x ∩ y because
                    # of how python handles sets x frozensets operations
                    new_p.add(y & x)
                    new_p.add(y - x)
                    if y in w:
                        w.remove(y)
                        w.add(y & x)
                        w.add(y - x)
                    else:
                        if len(x & y) <= len(y - x):
                            w.add(y & x)
                        else:
                            w.add(y - x)
        return p


# %%
