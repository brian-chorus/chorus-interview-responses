-- Get practitioners who have never prescribed any medication

select p.id, p.name
from "Practitioner" p
where p.id not in
-- Get list of all practioniors who have places a prescription
(select distinct(mr.practitioner_id) from "MedicationRequest" mr);