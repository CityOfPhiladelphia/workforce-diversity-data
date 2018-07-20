 SELECT DISTINCT ON (exempt_workforce_normalized.payroll_number, exempt_workforce_normalized.latest_start_date) exempt_workforce_normalized.snapshot_date,
    exempt_workforce_normalized.payroll_number,
    exempt_workforce_normalized.first_name,
    exempt_workforce_normalized.last_name,
    exempt_workforce_normalized.dob,
    exempt_workforce_normalized.department,
    exempt_workforce_normalized.division,
    exempt_workforce_normalized.index_code,
    exempt_workforce_normalized.orig_appointment_date,
    exempt_workforce_normalized.job_seniority_date,
    exempt_workforce_normalized.latest_start_date,
    exempt_workforce_normalized.department_number,
    exempt_workforce_normalized.hiring_department,
    exempt_workforce_normalized."position",
    exempt_workforce_normalized.job,
    exempt_workforce_normalized.pay_group_name,
    exempt_workforce_normalized.base_salary,
    exempt_workforce_normalized.total_salary,
    exempt_workforce_normalized.employment_category,
    exempt_workforce_normalized.assignment_status,
    exempt_workforce_normalized.eeo_category,
    exempt_workforce_normalized.hispanic_or_latino_of_any_race,
    exempt_workforce_normalized.american_indian_or_alaskan_native,
    exempt_workforce_normalized.asian,
    exempt_workforce_normalized.black_or_african_american,
    exempt_workforce_normalized.native_hawaiian_or_other_pacific,
    exempt_workforce_normalized.white,
    exempt_workforce_normalized.two_or_more_races,
    exempt_workforce_normalized.did_not_disclose_race,
    exempt_workforce_normalized.female,
    exempt_workforce_normalized.male
   FROM workforce_diversity.exempt_workforce_normalized
  WHERE exempt_workforce_normalized.job_seniority_date = exempt_workforce_normalized.latest_start_date
  ORDER BY exempt_workforce_normalized.payroll_number, exempt_workforce_normalized.latest_start_date, exempt_workforce_normalized.snapshot_date DESC;