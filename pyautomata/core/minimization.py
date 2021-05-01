from pyautomata.core.automata import Automata  # pylint: disable=import-error
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

    def create_total_function(self) -> Dict[Tuple[str, str], str]:
        total_program_function = copy.deepcopy(self.program_function)
        for state in self.states:
            for c in self.alphabet:
                if (state, c) in self.program_function:
                    continue
                total_program_function[(state, c)] = "Undefined"
        return total_program_function

    def check_identical_states(
        self, state_pairs: List[Tuple[str, str]]
    ) -> bool:
        for state_pair in state_pairs:
            if state_pair[0] != state_pair[1]:
                return False
        return True

    def minimize(self):
        # creates the total function
        total_program_function = self.create_total_function()
        # a dictionary of tuples to the actual pairs with properties
        table_pair = {
            pair: MinimizationTable(pair)
            for pair in itertools.combinations(self.states + ["Undefined"], 2)
        }
        # marking the pairs which one is final and the other non-final
        for pair in table_pair.values():
            if (
                pair.state1 in self.final_states
                and pair.state2 not in self.final_states
                or pair.state1 not in self.final_states
                and pair.state2 in self.final_states
            ):
                pair.distinguishable = True
        for pair, table_element in table_pair.items():
            results: List[Tuple[str, str]] = []
            for c in self.alphabet:
                results.append(
                    (
                        total_program_function[(table_element.state1, c)],
                        total_program_function[(table_element.state2, c)],
                    )
                )
            if self.check_identical_states(results):
                continue
            for result in results:
                # if one of the results is distinguishable
                # means the pair also needs to be distinguishable
                # TODO: this needs to be recurisve,
                # probably under a new function
                if table_pair[result].distinguishable:
                    self.make_distinguishable(table_pair, table_element)
                    table_element.distinguishable = True
                else:
                    table_pair[result].dependencies.append(pair)

    def unify_pairs(self, table: Dict[Tuple[str, str], MinimizationTable]):
        for tup, elem in table.items():
            if elem.distinguishable:
                continue
            new_name = tup[0] + tup[1]
            for (state, c), result_state in self.program_function.items():
                if result_state == tup[0] or result_state == tup[1]:
                    self.program_function[(state, c)] = new_name
            for c in self.alphabet:
                states0 = self.program_function[(tup[0], c)]
                states1 = self.program_function[(tup[1], c)]
                if states0 == states1:
                    self.program_function.pop((states0, c))
                    self.program_function.pop((states1, c))
                    self.program_function[(new_name, c)] = states0
                else:
                    self.program_function.pop((states0, c))
                    self.program_function.pop((states1, c))
                    self.program_function[(new_name, c)] = states0 + states1

    def make_distinguishable(
        self,
        full_table: Dict[Tuple[str, str], MinimizationTable],
        curr_table_element: MinimizationTable,
    ):
        curr_table_element.distinguishable = True
        for depedency in curr_table_element.dependencies:
            self.make_distinguishable(
                full_table, full_table[depedency]
            )
