# PCC3

## Information

Testing version of the "PC Creator 2" Bot

Release repo [here](https://github.com/YES-German/PC_Creator_2).

## Installation

Install all dependencies:
```bash
pip install -r requirements.txt
```

Rename ```rename-to json_files``` to ```json_files```.

Edit ```json_files/mainconfig.json``` for your use.


## Usage

Start by typing:
```bash
python main.py
```
### ATTENTION
Using the bot for the first time causes a few errors.

Setting a logging channel in ```cogs/logger``` in BOTH python files, resolves all except one.

The last one one can be fixed by creating a Ticket-Channel and typing ```.create_ticket```

### ATTENTION2
The permissions and roles are set for our use case. Just change the Role-IDs in the .py files. (It's self explanatory.)

## Contributing
Create a bug report [here](https://github.com/SleepyYui/PCC3/issues/new?assignees=&labels=&template=bug_report.md&title=).

Create a feature request [here](https://github.com/SleepyYui/PCC3/issues/new?assignees=&labels=&template=feature_request.md&title=).

## License
[GPL3](https://www.gnu.org/licenses/gpl-3.0.en.html)
