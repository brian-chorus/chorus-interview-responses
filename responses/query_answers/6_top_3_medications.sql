-- Find the top 3 most prescribed medications

-- Slightly unclear about definition of most commmonly perscribed
select medication_name,
    count(1) as number_of_prescriptions
from "MedicationRequest"
where status != 'cancelled'
group by 1
order by 2 desc
limit 3