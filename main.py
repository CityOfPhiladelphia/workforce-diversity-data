import sys
import os
from datetime import datetime
from collections import OrderedDict

import click
import petl
import arrow

column_map_hires = OrderedDict([
    ('Payroll Number', 'payroll_number'),
    ('First Name', 'first_name'),
    ('Last Name', 'last_name'),
    ('Department', 'department'),
    ('Division', 'division'),
    ('Index Code', 'index_code'),
    ('Position', 'position'),
    ('Job', 'job'),
    ('Latest Start Date', 'latest_start_date'),
    ('Job Seniority Date', 'job_seniority_date'),
    ('Orig Appointment Date', 'orig_appointment_date'),
    ('Hiring Department', 'hiring_department'),
    ('Total Salary', 'total_salary'),
    ('Gender', 'gender'),
    ('Hispanic or Latino of any race', 'hispanic_or_latino_of_any_race'),
    ('American Indian or Alaskan Native', 'american_indian_or_alaskan_native'),
    ('Asian', 'asian'),
    ('Black or African American', 'black_or_african_american'),
    ('Native Hawaiian or Other Pacific', 'native_hawaiian_or_other_pacific'),
    ('White', 'white'),
    ('Two or More Races', 'two_or_more_races'),
    ('Assignment Status', 'assignment_status'),
    ('Assignment Category', 'assignment_category')
])

hires_date_fields = [
    'orig_appointment_date',
    'job_seniority_date',
    'latest_start_date'
]

column_map_shared = OrderedDict([
    ('Payroll Number', 'payroll_number'),
    ('First Name', 'first_name'),
    ('Last Name', 'last_name'),
    ('Department', 'department'),
    ('Division', 'division'),
    ('Index Code', 'index_code'),
    ('Position', 'position'),
    ('Job', 'job'),
    ('Latest Start Date', 'latest_start_date'),
    ('Job Seniority Date', 'job_seniority_date'),
    ('Hiring Department', 'hiring_department'),
    ('Total Salary', 'total_salary'),
    ('Gender', 'gender'),
    ('Hispanic or Latino of any race', 'hispanic_or_latino_of_any_race'),
    ('American Indian or Alaskan Native', 'american_indian_or_alaskan_native'),
    ('Asian', 'asian'),
    ('Black or African American', 'black_or_african_american'),
    ('Native Hawaiian or Other Pacific', 'native_hawaiian_or_other_pacific'),
    ('White', 'white'),
    ('Two or More Races', 'two_or_more_races'),
    ('Assignment Status', 'assignment_status'),
    ('Assignment Category', 'assignment_category')
])

column_map_separations = OrderedDict([
    ('Leaving Reason', 'leaving_reason'),
    ('Termination Date', 'termination_date')
])

separations_date_fields = [
    'latest_start_date',
    'job_seniority_date',
    'termination_date'
]

column_map_roster = OrderedDict([
    ('Employee Number', 'payroll_number'),
    ('First Name', 'first_name'),
    ('Last Name', 'last_name'),
    ('Date Of Birth', 'dob'),
    ('Department', 'department'),
    ('Division', 'division'),
    ('Index Code', 'index_code'),
    ('Hispanic of Latino of any race', 'hispanic_or_latino_of_any_race'),
    ('American Indian or Alaskan Native', 'american_indian_or_alaskan_native'),
    ('Asian', 'asian'),
    ('Black or African American', 'black_or_african_american'),
    ('Native Hawaiian or Other Pacific', 'native_hawaiian_or_other_pacific'),
    ('White', 'white'),
    ('Two or More Races', 'two_or_more_races'),
    ('Sex', 'gender'),
    ('Orig Appointment Date', 'orig_appointment_date'),
    ('Job Seniority Date', 'job_seniority_date'),
    ('Latest Start Date', 'latest_start_date'),
    ('Department Number', 'department_number'),
    ('Hiring Department', 'hiring_department'),
    ('Position', 'position'),
    ('Job', 'job'),
    ('Pay Group Name', 'pay_group_name'),
    ('Base Salary', 'base_salary'),
    ('Total Salary', 'total_salary'),
    ('Emp Category', 'employment_category'),
    ('Assignment Status', 'assignment_status'),
    ('EEO Category', 'eeo_category')
])

roster_date_fields = [
    'dob',
    'orig_appointment_date',
    'job_seniority_date',
    'latest_start_date'
]

def convert_date(value):
    if value == '':
        return None
    return datetime.strptime(value, '%Y/%m/%d %I:%M:%S %p').isoformat() + 'Z'
    #return arrow.get(value, 'M/D/YYYY H:mm').isoformat().replace('+00:00', 'Z')

    # try:
    #     return arrow.get(value, 'M/D/YYYY').isoformat().replace('+00:00', 'Z')
    # except:
    #     return arrow.get(value, 'D-MMM-YYYY').isoformat().replace('+00:00', 'Z')

def transformer(snapshot_date, date_fields):
    def transform_row(row):
        out = list(row)

        for date_field in date_fields:
            i = row.flds.index(date_field)
            out[i] = convert_date(out[i])

        return [snapshot_date] + out
    return transform_row

@click.group()
def main():
    pass

def get_last_modified():
    return os.getenv('LAST_MODIFIED', datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))

@main.command()
def transform_exempt_roster():
    snapshot_date = get_last_modified()

    new_headers = ['snapshot_date'] + list(column_map_roster.values())

    (
        petl
        .fromcsv()
        .rename(column_map_roster)
        .rowmap(transformer(snapshot_date, roster_date_fields), new_headers, failonerror=True)
        .tocsv()
    )

@main.command()
def transform_hires():
    snapshot_date = get_last_modified()

    new_headers = ['snapshot_date'] + list(column_map_hires.values())

    (
        petl
        .fromcsv()
        .rename(column_map_hires)
        .rowmap(transformer(snapshot_date, hires_date_fields), new_headers, failonerror=True)
        .tocsv()
    )

@main.command()
def transform_separations():
    snapshot_date = get_last_modified()

    new_headers = ['snapshot_date'] + list(column_map_shared.values()) + list(column_map_separations.values())

    (
        petl
        .fromcsv()
        .rename({**column_map_shared, **column_map_separations})
        .rowmap(transformer(snapshot_date, separations_date_fields), new_headers, failonerror=True)
        .tocsv()
    )

@main.command()
@click.argument('hires_and_promotions_excel', type=click.Path(exists=True))
@click.argument('separations_excel', type=click.Path(exists=True))
@click.argument('exempt_roster_excel', type=click.Path(exists=True))
@click.option('--output-file', type=click.Path(), default=None)
def transform_xls(hires_and_promotions_excel, separations_excel, exempt_roster_excel, output_file):
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

    exempt_roster = petl.io.xls \
                        .fromxls(exempt_roster_excel, sheet='Data') \
                        .rename(column_map_roster)

    merged = petl.mergesort(hires_and_promotions, separations_deduped, exempt_roster, key='payroll_number')

    def dedup_merged(payroll_number, rows):
        rows_sorted = sorted(rows, key=lambda x: x['latest_start_date'])

        if len(rows_sorted) == 1:
            return rows_sorted[-1]

        merged_row = []
        for i in range(0, len(rows_sorted[0]) - 1):
            if (rows_sorted[0][i] == '' or rows_sorted[0][i] == None) and rows_sorted[1][i] != '' and rows_sorted[1][i] != None:
                merged_row.append(rows_sorted[1][i])
            elif (rows_sorted[1][i] == '' or rows_sorted[1][i] == None) and rows_sorted[0][i] != '' and rows_sorted[0][i] != None:
                merged_row.append(rows_sorted[0][i])
            elif rows_sorted[0][i] == rows_sorted[1][i]:
                merged_row.append(rows_sorted[0][i])
            else:
                merged_row.append(rows_sorted[1][i]) ## take latest value by start date

        return merged_row

    merged_deduped = petl.rowreduce(merged, 'payroll_number', dedup_merged)

    petl.tocsv(merged_deduped, source=output_file)

if __name__ == '__main__':
    main()
