# Little-NavCup

Convert the SeeYou CUP format to a CSV format readable by Little Navmap using Python.

- [SeeYou CUP format documentation](https://downloads.naviter.com/docs/SeeYou_CUP_file_format.pdf)
- [Little Navmap CSV documentation](https://www.littlenavmap.org/manuals/littlenavmap/release/3.0/en/USERPOINT.html#csv-data-format)

## Installation:

1. Install [python 3](https://www.python.org/downloads/).
2. Download the repository using the creen `code` button.

## Usage:

The program parses CUP files and writes Little Navmap-compatible `.csv` files to import as userpoints.

### CMD/Terminal

`python main.py [-h] cupfiles [cupfiles ...]`

`cupfiles`: Paths to CUP files. Multiple paths can be supplied. Examples:

- `python main.py "DE-WPT-National-XCSoar.cup"`
- `python main.py "DE-WPT-National-XCSoar.cup" "NL-WPT-National-XCSoar.cup"`

### Drag-and-Drop Bat Script

(Multiple) CUP files can be dropped on `drop_cup_here.bat`. The program writes the `.csv` files next to the original files.

## Notes

- Perhaps a binary executable should be built and released to make installation easier.