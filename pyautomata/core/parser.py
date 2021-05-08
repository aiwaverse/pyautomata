"""
The Parser module contains the abstract class Parser
And two concrete instances, WordFileParser and
AutomataParser
"""
import abc
import re
from typing import Dict, List, Tuple, Union, Set

from more_itertools import grouper


class Parser(abc.ABC):
    """
    Base Parser class
    """
    @abc.abstractmethod
    def parse(self):
        """
        parse something
        """


class WordFileParser(Parser):
    """
    The class that models the parser for the words file
    """

    def __init__(self, *, file_name: str = None, content: str = None) -> None:
        """
        The constructor, either a file_name or a content must be provided
        If both are provided, file_name is used
        If none are provided, ValueError is raised
        """
        if file_name:
            with open(file_name) as f:
                self.content = f.read()
        elif content:
            self.content = content
        else:
            raise ValueError(
                "Either file_name or content must be provided"
                "(file_name is prioritized)"
            )

    def parse(self) -> List[Tuple[str, str]]:
        """
        Parse the contents and return a list of tuples
        With all the words
        """
        results = re.findall(r"\w*,\w*", self.content)
        to_return: List[Tuple[str, str]] = []
        for w in results:
            splitted: List[str] = w.split(",")
            to_return.append((splitted[0], splitted[1]))
        return to_return


class AutomataParser(Parser):
    """
    The Parser used to create an automata
    """
    def __init__(self, *, file_name: str = None, content: str = None) -> None:
        """
        The constructor, either a file_name or a content must be provided
        If both are provided, file_name is used
        If none are provided, ValueError is raised
        """
        if file_name:
            with open(file_name) as f:
                self.content = f.read()
        elif content:
            self.content = content
        else:
            raise ValueError(
                "Either file_name or content must be provided"
                "(file_name is prioritized)"
            )

    @property
    def content(self) -> str:
        """
        Returns the input string
        """
        return self._content

    @content.setter
    def content(self, s: str) -> None:
        """
        Changes the input string for the program
        """
        self._content = s

    @staticmethod
    def description_parse(
        description: str,
    ) -> Dict[str, Union[str, Set[str]]]:
        """
        Parses the description line
        returns a dictionary with the information
        """
        initial_description_results = re.findall(
            r"\w+(?==\()|(?<={)[\w*,]*(?=})|(?<=,)\w*(?=,)",
            description,
        )
        return {
            "name": initial_description_results[0],
            "states": set(initial_description_results[1].split(",")),
            "alphabet": set(initial_description_results[2].split(",")),
            "initial_state": initial_description_results[4],
            "final_states": set(initial_description_results[5].split(",")),
        }

    @staticmethod
    def program_function_parse(
        program_function: str,
    ) -> Dict[Tuple[str, str], str]:
        """
        Parses the program function
        returns a dictionary that waits for a tuple as a key (state, word)
        """
        program_function_results = re.findall(
            r"(?<=\()\w+,\w+(?=\)=)|(?<==)\w+", program_function
        )
        grouped = grouper(program_function_results, 2)
        return_dict = {}
        for group in grouped:
            state, transition_word = tuple(group[0].split(","))
            return_dict.update({(state, transition_word): group[1]})
        return return_dict

    def parse(
        self,
    ) -> Tuple[Dict[str, Union[str, Set[str]]], Dict[Tuple[str, str], str]]:
        """
        Run the whole parsing
        Returns 2 dictionaries: (description, program function)
        """
        split_string = self.content.split("\n")
        initial_description = split_string[0]
        program_function = "".join(split_string[2:])
        description_dict = self.description_parse(initial_description)
        program_dict = self.program_function_parse(program_function)
        return description_dict, program_dict

# %%
