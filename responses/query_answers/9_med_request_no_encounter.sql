-- Identify patients who have never had an encounter but have a medication request

select p.id, p.name
from "Patient" p
where p.id in
-- Patient has record in MeidcationRequest
	(select distinct(patient_id) from "MedicationRequest")
AND p.id not in
-- But no record in encounter
	(select distinct(patient_id) from "Encounter");