# workforce-diversity-data

Process Oracle employee data and prepare it for workforce diversity
statistic analysis.

## Installation
Clone the repository and install dependencies via:

```bash
pip install -r requirements.txt
```

## Usage
```bash
python main.py hires-sample.csv
```

Note: use [`in2csv`][in2csv] to convert Excel files to `.csv`.
You may need to specify `--format xls` despite the file extension
of `.xlsx` that Oracle provides.

[in2csv]: http://csvkit.readthedocs.io/en/833/scripts/in2csv.html
