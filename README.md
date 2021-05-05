# Pyautomata

Pyautomata is a python project made to simulate the execution of a Deterministic Finite Automata (DFA). This repository includes the [core library](https://github.com/aiwaverse/pyautomata-git/tree/main/pyautomata/core) and a [GUI](https://github.com/aiwaverse/pyautomata-git/tree/main/pyautomata/gui) made with [PySimpleGUI](https://pypi.org/project/PySimpleGUI/). At the root of this repository there is a ```main.py``` file to run the project completely integrated.

## Installation

To install this program, run the following commands on Linux:

```bash
git clone https://github.com/aiwaverse/pyautomata-git
cd pytautomata-git
pip install -r requirements.txt
```
On other operational systems, to install the instructions are the same:
1. Clone this repository
2. Enter the folder
3. Use pip to install the requirements on requirements.txt
## File format
This program requires a DFA file, the expected format is:
```
<M>=({<q0>,...,<qn>},{<s1>,...,<sn>},Prog,<ini>,{<f0>,...,<fn>})
Prog
(<q0>,<s1>)=<q1>
...
(<qn>,<sn>)=<q0>
```
Where:
* ```<M>``` is the automata name.
* ```{<q0>,...,<qn>}``` are the automata states.
* ```{<s1>,...,<sn>}``` are the alphabet symbols. 
* ```<ini>``` is the initial state.
* ```{<f0>,...,<fn>}``` are the final (accepting) states.

It is of extreme importance that the file has the **exact** same formatting, specially containing no spaces on the file.

The program can also verify a file of word pairs, with the following expected format:
```
<w0>,<w2>
<w2>,<w3>
```
Where ```wn``` is a word in the language of the automata.
## Usage
The program can be run directly with Python:
```bash
python main.py
```
![First Screen](https://raw.githubusercontent.com/aiwaverse/pyautomata-git/GUI-Refactor/images/program_initial.png)

You must them browse and submit the file where the automata is defined:
![Defined Automata](https://raw.githubusercontent.com/aiwaverse/pyautomata-git/GUI-Refactor/images/program_automata_submitter.png)

You may now test for individual words, where the result will appear in a new window, alongside the path the program used to aprove the words, or, if it was rejected, the reason why.

![Word Accepted](https://raw.githubusercontent.com/aiwaverse/pyautomata-git/GUI-Refactor/images/word_accepted.png)

You can also verify using a file of word pairs, where the result will be all pairs that had both words accepted.

![Final program](https://raw.githubusercontent.com/aiwaverse/pyautomata-git/GUI-Refactor/images/program_final.png)

![Pairs](https://raw.githubusercontent.com/aiwaverse/pyautomata-git/GUI-Refactor/images/pairs.png)

It can also be used inside other Python codes:
```python
import pyautomata

p = pyautomata.AutomataParser(file_name="automata.txt")
description, function_program = p.parse()
aut = pyautomata.Automata(function_program, **description)
print(aut.check_word("aab")) # will print the result
```

## License
[MIT](https://choosealicense.com/licenses/mit/)