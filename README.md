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
To run the script, execute `python main.py`. It will open a small window with the option to either draw a graph of the most common faces in your photo collection `draw all` or you can select a person and draw a graph of the most common faces that appear together with this person `draw for selected`. You can also select the tab `Connections` to get a network graph of the most common faces. You can specify the number of "root" faces `Roots` and the number of "leafs" `Leafs`. The faces are sorted according to how often they appear. In the input box `Graph Size` you can specify the number of people to consider when you create a network graph for one selected person with `connections for selected`. In the last `Cutoff` input field you can specify the least amount of times a person has to appear (together) to be displayed.