select hardware_corecount, count(*) from hosts
group by hardware_corecount
having count(*)>1
