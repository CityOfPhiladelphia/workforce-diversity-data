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
        .rename({'Payroll Number': 'payroll_number',
                 'First Name': 'first_name',
                 'Last Name': 'last_name',
                 'Department': 'department',
                 'Position': 'position',
                 'Job': 'job',
                 'Latest Start Date': 'latest_start_date',
                 'Job Seniority Date': 'job_seniority_date',
                 'Total Salary': 'total_salary',
                 'Gender': 'gender',
                 'Assignment Status': 'assignment_status',
                 'Assignment Category': 'assignment_category'}) \
        .select('{latest_start_date} == {job_seniority_date}') \
        .addfield('race_ethnicity', add_race_ethnicity) \
        .cutout(*RACES)
    etl.tocsv(table)

if __name__ == '__main__':
    process()
