import click
import petl as etl

RACES = [
    'Hispanic or Latino of any race',
    'American Indian or Alaskan Native',
    'Asian',
    'Black or African American',
    'Native Hawaiian or Other Pacific',
    'White',
    'Two or More Races',
]

def add_race_ethnicity(row):
    race_ethnicity = ''

    for option in RACES:
        if row[option] == 'True':
            return option

@click.command()
@click.argument('hires', type=click.Path(exists=True))
def process(hires):
    # Exclude promotions, replace race fields with one
    table = etl.fromcsv(hires) \
        .select('{Latest Start Date} == {Job Seniority Date}') \
        .addfield('Race/Ethnicity', add_race_ethnicity) \
        .cutout(*RACES)
    print(etl.tocsv(table))

if __name__ == '__main__':
    process()
