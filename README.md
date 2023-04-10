# Digikam Face Relations
This is a small (and poorly written) tool to view which are the most common faces in your pictures, and how often they appear together.

## Installation
[First of all, you need to install python.](https://www.python.org/downloads/)
Then upgrade **pip** and install the required packages:
```
pip install --upgrade pip
pip install -r requirements.txt
```
You need to add your Digikam-Database path to the `.env` file `DATABASE_PATH = /path/to/your/database/digikam4.db`
## Usage
When you run the script `python main.py`, it will open a small window with the option to either draw a graph of the most common faces in your picture collection `draw for all` or you can select a person and draw a graph of the most common faces that appear together with this person `draw for selected`. Additionally, you can select `draw connections` to get a network graph of the most common faces. You can specify the number of "root" faces (first input box) and the number of "child" faces (second input box). The faces are sorted according to how often they appear. In the last input box you can set a number of people that are considered when you create a network graph for the selected perseon `connections for selected`