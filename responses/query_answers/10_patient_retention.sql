-- Determine patient retention by cohort


-- Get first encounter
with first_encounter as (
	select patient_id,
	    min(encounter_date) as first_encounter_date
	from "Encounter"
	group by patient_id
),
-- Create an encounter table that includes the next encounter as a column
subsequent_encounter as (
	select e.patient_id,
	    e.encounter_date,
		LEAD(e.encounter_date) over (
			partition by e.patient_id
			order by e.encounter_date
		) as subsequent_encounter_date
	from "Encounter" e
),
-- filter records to only get first encounters from the subsequent encounter table
only_first_encounters as (
	select se.patient_id,
	    se.encounter_date,
	    se.subsequent_encounter_date
	from subsequent_encounter se
	join first_encounter fe
		on fe.patient_id = se.patient_id
		and fe.first_encounter_date = se.encounter_date
),
-- determine if the subsequent encounter is within 6 months
-- create column YYYY-MM to make next step easier
is_within_6_months as (
	select patient_id,
	    TO_CHAR(encounter_date, 'YYYY-MM') AS encounter_month,
	    encounter_date, subsequent_encounter_date,
		(CASE
			WHEN subsequent_encounter_date is not null
				AND AGE(subsequent_encounter_date, encounter_date) <= interval '6 month' then true
				ELSE false
		 END) as is_6_months
	from only_first_encounters
)
-- Calculate how many patient had their first encoutner in a given month and a follow up within 6 months
select  encounter_month,
    count(1) as patient_retention
from is_within_6_months
where is_6_months
group by encounter_month