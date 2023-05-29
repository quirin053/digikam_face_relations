# Digikam Face Relations
This is a small (and poorly written) tool to visualize which are the most common faces in your photo collection, and how often they appear together.

## Installation
[First of all, you need to install python.](https://www.python.org/downloads/)
Next, upgrade **pip** and install the required packages:
```
pip install --upgrade pip
pip install -r requirements.txt
```
You need to add your Digikam-Database path to the `.env` file `DATABASE_PATH = /path/to/your/database/digikam4.db`
## Usage
To run the script, execute `python main.py`. It will open a small window with the option to either draw a graph of the most common faces in your photo collection `draw all` or you can select a person and draw a graph of the most common faces that appear together with this person `draw for selected`. You can also select `draw connections` to get a network graph of the most common faces. You can specify the number of "root" faces (first input box) and the number of "child" faces (second input box). The faces are sorted according to how often they appear. In the third input box you can specify the number of people to consider when you create a network graph for the selected person `connections for selected`. In the last input field you can specify the least amount of times a person has to appear (together).