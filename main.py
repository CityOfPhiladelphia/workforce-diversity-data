import sys

import click
import petl

column_map_shared = {
    'Payroll Number': 'payroll_number',
    'First Name': 'first_name',
    'Last Name': 'last_name',
    'Department': 'department',
    'Position': 'position',
    'Job': 'job',
    'Latest Start Date': 'latest_start_date',
    'Job Seniority Date': 'job_seniority_date',
    'Total Salary': 'total_salary',
    'Gender': 'gender',
    'Hispanic or Latino of any race': 'hispanic_or_latino_of_any_race',
    'American Indian or Alaskan Native': 'american_indian_or_alaskan_native',
    'Asian': 'asian',
    'Black or African American': 'black_or_african_american',
    'Native Hawaiian or Other Pacific': 'native_hawaiian_or_other_pacific',
    'White': 'white',
    'Two or More Races': 'two_or_more_races',
    'Assignment Status': 'assignment_status',
    'Assignment Category': 'assignment_category'
}

column_map_separations = {
    'Leave Reason': 'leave_reason',
    'Termination Date': 'termination_date'
}

@click.command()
@click.argument('hires_and_promotions_excel', type=click.Path(exists=True))
@click.argument('separations_excel', type=click.Path(exists=True))
@click.option('--output-file', type=click.Path(), default=None)
def transform(hires_and_promotions_excel, separations_excel, output_file):
    hires_and_promotions = petl.io.xls \
                            .fromxls(hires_and_promotions_excel, sheet='Data') \
                            .rename(column_map_shared)

    separations = petl.io.xls \
                    .fromxls(separations_excel, sheet='Data') \
                    .rename({**column_map_shared, **column_map_separations})

    def dedup_separations(payroll_number, rows):
        rows_sorted = sorted(rows, key=lambda x: x['termination_date'])
        return rows_sorted[-1]

    separations_deduped = petl.rowreduce(separations, 'payroll_number', dedup_separations)

    merged = petl.mergesort(hires_and_promotions, separations_deduped, key='payroll_number')

    petl.tocsv(merged, source=output_file)

if __name__ == '__main__':
    transform()
