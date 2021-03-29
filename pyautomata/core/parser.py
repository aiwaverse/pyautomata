import abc
import re
from more_itertools import grouper
from typing import Dict, List, Union, Tuple


class Parser(abc.ABC):
    @abc.abstractmethod
    def parse(self):
        pass


class AutomataParser(Parser):
    def __init__(self, input_string: str) -> None:
        self._input_string = input_string

    @property
    def input_string(self) -> str:
        """
        Devolve a string de input
        """
        return self._input_string

    @input_string.setter
    def input_string(self, s: str) -> None:
        """
        Dada uma string s, atribui s à input_string
        """
        self._input_string = s

    def description_parse(
        self, description: str
    ) -> Dict[str, Union[str, List[str]]]:
        """
        Faz o parsing da linha de descrição
        retorna um dicionário com as informações
        """
        initial_description_results = re.findall(
            r"\w+(?==\()|(?<={)[\w+,]+(?=})|(?<=,)\w+(?=,)",
            description,
        )
        return {
            "name": initial_description_results[0],
            "states": initial_description_results[1].split(","),
            "alphabet": initial_description_results[2].split(","),
            "initial_state": initial_description_results[4],
            "final_states": initial_description_results[5].split(","),
        }

    def program_function_parse(
        self, program_function: str
    ) -> Dict[Tuple[str, str], str]:
        """
        Faz o parsing da função programa
        retorna um dicinário que espera uma tupla como chave (estado, palavra)
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
    ) -> Tuple[Dict[str, Union[str, List[str]]], Dict[Tuple[str, str], str]]:
        """
        Executa o parsing inteiro, retorna os dois dicinários
        (descrição, função programa)
        """
        splitted_string = self.input_string.split("\n")
        initial_description = splitted_string[0]
        program_function = "".join(splitted_string[2:])
        description_dict = self.description_parse(initial_description)
        program_dict = self.program_function_parse(program_function)
        return description_dict, program_dict
