![](https://mobiuslau.s-ul.eu/PNQCQxAc)

# Little-NavCup: Import CUP Userpoints

Convert the SeeYou CUP format to a CSV format readable by Little Navmap, which is used to import userpoints, with Python.

- [SeeYou CUP format documentation](https://downloads.naviter.com/docs/SeeYou_CUP_file_format.pdf)
- [Little Navmap CSV documentation](https://www.littlenavmap.org/manuals/littlenavmap/release/3.0/en/USERPOINT.html#csv-data-format)

## Installation:

1. Install [python 3](https://www.python.org/downloads/).
2. Download the repository using the green `code` button.

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
- No bijection exists between the CUP format's waypoint styles and Little Navmap's types. Therefore, a choice had to be made how the CUP waypoint styles get mapped. The mapping can be found [here](https://github.com/Mobiuslau/Little-NavCup/blob/9fa22f71b341f327110c771da3b897ade3a7477a/main.py#L175). The user could change this mapping to suit their own needs by changing the values in the dictionary to any other [Little Navmap-compatible types](https://www.littlenavmap.org/manuals/littlenavmap/release/3.0/en/USERPOINT.html#types).
- Perhaps a binary executable should be built and released to make installation easier.
