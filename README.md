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

Upsert the output of the above files to 3 tables in postgres using the following command.

```sh
the_el write {table name} --table-schema-path {schema in schemas/} --db-schema workforce_diversity --geometry-support postgis --skip-headers --upsert --connection-string {connection to redash data database}
```

### Database and Views

These are all in the redash.covdnv9qscn1.us-east-1.rds.amazonaws.com/data database. Credentials are in lastpass.

| Schema | Table/View | Description | Dependencies |
| ------ | ---------- | ----------- | ------------ |
| `public` | `departments` | Lookup table of departments and cabinets |
| `workforce_diversity` | `cabinets_departments_dropdown` | View powering the cabinets and departments dropdown. | |
| `workforce_diversity` | `census_acs_2015` | US Census American Community Survey demographic data. | |
| `workforce_diversity` | `exempt_workforce` | **Updates** - Table used upserted with the exempt roster data. | |
| `workforce_diversity` | `exempt_workforce_normalized` | Cleans up `workforce_diversity.exempt_workforce` | `workforce_diversity.exempt_workforce` |
| `workforce_diversity` | `hires` | **Updates** - Raw data from the hiring transformations. | |
| `workforce_diversity` | `hires_normalized` | Cleans up `workforce_diversity.hires` | `workforce_diversity.hires` and `workforce_diversity.exempt_workforce_normalized` |
| `workforce_diversity` | `hiring_events` | Every unique hiring event for each employee. | `workforce_diversity.hires_normalized` |
| `workforce_diversity` | `latest_exempt_workforce` | The latest available snapshot of the exempt workforce. | `workforce_diversity.exempt_workforce_normalized` |
| `workforce_diversity` | `separation_events` | Every unique separation event for each employee. | `workforce_diversity.separations_normalized` |
| `workforce_diversity` | `separations` | **Updates** - Raw data from the separations transformation. | |
| `workforce_diversity` | `separations_normalized` | Cleans up `workforce_diversity.separations` | `workforce_diversity.separations` and `workforce_diversity.exempt_workforce_normalized` |