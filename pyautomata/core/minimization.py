# %%
from pyautomata import Automata  # pylint: disable=import-error
from typing import Dict, Set, Tuple, List
import itertools
import copy


class MinimizationTable:
    def __init__(self, states: Tuple[str, str]) -> None:
        self.state1 = states[0]
        self.state2 = states[1]
        self.distinguishable = False
        self.dependencies: List[Tuple[str, str]] = []


class MinimizedAutomata(Automata):
    def __init__(
        self, program_function: Dict[Tuple[str, str], str], **kwargs
    ) -> None:
        super().__init__(program_function, **kwargs)
        self.remove_unreachable_states()

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

    def hopcroft_alogrithm(self):
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
                x = set(
                    [
                        state
                        for (
                            state,
                            character,
                        ), result_state in self.program_function.items()
                        if result_state in a and character == c
                    ]
                )
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
