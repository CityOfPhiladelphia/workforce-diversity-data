# workforce-diversity-data

Process Oracle employee data and prepare it for workforce diversity
statistic analysis.

## Installation
Clone the repository and install dependencies via:

```bash
pip install -r requirements.txt
```

## Usage

### Snapshot Date

Before running each command below, make sure to seet the LAST_MODIFIED variable to the modified time of the original file or an approimation of when the report file run.

`export LAST_MODIFIED=2018-07-01T04:03:44Z`

#### Transformations

Roster report file

```sh
cat /path/to/roster_report.csv | python main.py transform_exempt_roster > exempt_roster.csv
```

Hiring and promotions file

```sh
cat /path/to/roster_report.csv | python main.py transform_hires > hires.csv
```

Separations file

```sh
cat /path/to/roster_report.csv | python main.py transform_separations > separations.csv
```

### The EL

Upsert the output of the above files to 3 tables in postgres usign the following command.

```sh
the_el write {table name} --table-schema-path {schema in schemas/} --db-schema workforce_diversity --geometry-support postgis --skip-headers --upsert --connection-string {connection to redash data database}
```