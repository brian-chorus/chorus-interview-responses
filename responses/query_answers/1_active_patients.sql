--Retrieve all active patients

select name, id, active
from "Patient"
-- Filter on active patients
where active;