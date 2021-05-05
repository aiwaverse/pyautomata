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
<M>=({<q0>,...,<qn>},{<s1>,...,<sn>},Prog,<ini>,{ <f0>,...,<fn>})
Prog
(<q0>,<s1>)=<q1>
...
(<qn>,<sn>)=<q0>
```
Where:
* ```<M>``` is the automata name.
* ```{<q0>,...,<qn>}``` are the automata states.
* ```{<s1>,...,<sn>}``` are the alphabet symbols. 
*```<ini>```
## Usage
The program can be run directly with Python:
```bash
python main.py
```
It can also be used inside other Python codes:
```python
import pyautomata

p = pyautomata.AutomataParser(file_name="automata.txt")
description, function_program = p.parse()
aut = pyautomata.Automata(function_program, **description)
print(aut.check_word("aab")) # will print the result
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)