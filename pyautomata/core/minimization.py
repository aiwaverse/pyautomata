"""
The Minimization module contains the MinimizedAutomata class.
This class is responsible for handling the DFA minimization,
with removal of unreachable states and the unification
of non-distinguishable states.
"""
# This whole module uses the method version of set operations
# instead of the actual operators, end result is the same,
# this was made to facilitate understanding.
import copy
from typing import Dict, FrozenSet, Set, Tuple
from itertools import combinations

from pyautomata import Automata  # pylint: disable=import-error


class TablePair:
    """
    The class that represents one element of the table for the
    Table Filling Algorithm
    """

    def __init__(self, state1: str, state2: str) -> None:
        self.state1 = state1
        self.state2 = state2
        self.distinguishable = False
        self.dependicies: Set[TablePair] = set()

    def __iter__(self):
        return iter(sorted([self.state1, self.state2]))

    def has_undefined(self) -> bool:
        """
        Function to tell if undefined is a value in the pair
        """
        return self.state1 == "Undefined" or self.state2 == "Undefined"


class MinimizedAutomata(Automata):
    """
    Class that does the DFA minimization.
    Opted for a method that minimizes, to faciliate tests.
    """

    def remove_states(self, states: Set[str]) -> None:
        """
        Removes the states passed as argument from
        the automata
        """
        for state in states:
            for c in self.alphabet:
                if (
                    (state, c) in self.program_function
                    and state not in self.initial_state
                ):
                    self.program_function.pop((state, c))
            self.states.remove(state)

    def minimize(self):
        """
        Does the minimization by doing all the steps
        """
        self.remove_states(self.unreacheable_states())
        self.unify_states()
        self.remove_states(self.useless_states())

    def unreacheable_states(self) -> Set[str]:
        """
        Determines the unreachable states of the Automata
        """
        reacheable_states: Set[str] = set([self.initial_state])
        new_states: Set[str] = set([self.initial_state])
        while new_states:
            temp: Set[str] = set()
            for q in new_states:
                for c in self.alphabet:
                    # this uses the empty string to maintain p typing
                    # I didn't want to annoy Pyright
                    p = self.program_function.get((q, c), "")
                    # if p is the empty string (i.e no transition with (q,c))
                    # continues the iteration
                    if not p:
                        continue
                    temp.add(p)
            # if temp == reachable states
            # new_states will be empty, and fail the while
            # exactly what we want
            new_states = temp - reacheable_states
            reacheable_states = reacheable_states.union(new_states)
        unreachable_states = set(self.states).difference(reacheable_states)
        return unreachable_states

    @staticmethod
    def make_state_name(states: FrozenSet[str]) -> str:
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
        equivalency_classes = self.table_filling_algorithm()
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

    # ultimately not used in the program
    # But I decided to leave it here
    def hopcroft_alogrithm(self) -> Set[FrozenSet[str]]:
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
        p: Set[FrozenSet[str]] = set([final_states_set, non_final_states_set])
        # new_p is used because p needs to change, but
        # python can't have a collection being changed mid-iteration
        new_p = copy.deepcopy(p)
        w: Set[FrozenSet[str]] = set([final_states_set, non_final_states_set])
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

    def total_function(self) -> Dict[Tuple[str, str], str]:
        """
        Creates a total function for the DFA
        """
        total_fun = {}
        for state in self.states:
            for c in self.alphabet:
                # if the function is undefined, will return "Undefined"
                # This, obviously, cannot be a valid state in the DFA
                # This is not checked
                total_fun[(state, c)] = self.program_function.get(
                    (state, c), "Undefined"
                )
        for c in self.alphabet:
            total_fun[("Undefined", c)] = "Undefined"
        return total_fun

    def mark_as_distinguishable(self, pair: TablePair) -> None:
        """
        Marks a table pair as distinguishable, and recursively
        marks any pair in it's dependecies
        Hopefully Python's shallow copy method will help me
        """
        pair.distinguishable = True
        for dep in pair.dependicies:
            if not dep.distinguishable:
                self.mark_as_distinguishable(dep)
        pair.dependicies = set()

    def useless_states(self) -> Set[str]:
        """
        Find the useless tates of an automata
        """
        useful_states = set(self.final_states)
        changed = True
        while changed:
            changed = False
            for (state, _), result_state in self.program_function.items():
                if (
                    result_state in useful_states
                    and state not in useful_states
                ):
                    useful_states.add(state)
                    changed = True
        return set(self.states) - useful_states

    @staticmethod
    def create_undistinguishable_sets(
        table: Dict[FrozenSet[str], TablePair]
    ) -> Set[FrozenSet[str]]:
        """
        With the table created by the algorithm,
        creates a set of sets with the equivalency classes.
        Akin to the result of the hopcroft algorithm, though
        arguably, slower
        """
        undistuinguishables = set()
        to_return_set = set()
        for pair in table.values():
            if not pair.distinguishable:
                undistuinguishables.add(pair.state1)
                undistuinguishables.add(pair.state2)
        for pair in table.values():
            if pair.distinguishable:
                if pair.state1 not in undistuinguishables:
                    to_return_set.add(frozenset([pair.state1]))
                if pair.state2 not in undistuinguishables:
                    to_return_set.add(frozenset([pair.state2]))
            else:
                to_return_set.add(frozenset(pair))
        return to_return_set

    def mark_final_and_non_final_pairs(
        self, table: Dict[FrozenSet[str], TablePair]
    ) -> None:
        """
        Marks all table pairs that have a combination of final and
        non-final states
        """
        for table_pair in table.values():
            if (
                table_pair.state1 in self.final_states
                and table_pair.state2 not in self.final_states
                or table_pair.state1 not in self.final_states
                and table_pair.state2 in self.final_states
            ):
                table_pair.distinguishable = True

    def table_filling_algorithm(self) -> Set[FrozenSet[str]]:
        """
        The table filling algorithm, as seen in class
        Or at least the closest I could get
        """
        total_program_function = self.total_function()
        # all the possible pairs, including Undefined
        table_pairs = combinations(self.states + ["Undefined"], 2)
        # the table is a dictionary with pair: TablePair, with
        # the pair being a frozenset (order doesn't matter, and is hashable)
        table = {frozenset(pair): TablePair(*pair) for pair in table_pairs}
        self.mark_final_and_non_final_pairs(table)
        # searches the table
        for table_pair in table.values():
            for c in self.alphabet:
                result_state1 = total_program_function[table_pair.state1, c]
                result_state2 = total_program_function[table_pair.state2, c]
                # if they go to the same state, skip letter
                if result_state1 == result_state2:
                    continue
                results_set = frozenset([result_state1, result_state2])
                # if the result is distinguishable, recursively
                # mark the dependecies and the pair itself
                if table[results_set].distinguishable:
                    self.mark_as_distinguishable(table_pair)
                # otherwise, add pair to result dependecy list
                else:
                    table[results_set].dependicies.add(table_pair)
        states = self.create_undistinguishable_sets(table)
        return states
