with initial as (
select
initial_call_type,
cast(priority as float) as priority,
count(*) as cnt,
(cast(priority as float) * count(*)) as ph
FROM gt.dbo.call_data_20251019_processed
group by initial_call_type, priority
),

initial_pseudo_priority_i as (
select 
initial_call_type as initial_call_type_i,
(sum(ph) / sum(cnt)) as initial_pseudo_priority_i
from initial
group by initial_call_type
),

initial_pseudo_priority_ii as (
select 
case when initial_call_type LIKE 'ALARM%' THEN 'ALARM'
WHEN initial_call_type LIKE 'ASLT%' OR initial_call_type LIKE 'ASSAULT%' THEN 'ASSAULT'
WHEN initial_call_type LIKE 'ANIMAL%' THEN 'ANIMAL'
when initial_call_type like 'ASSIGNED DUTY%' then 'ASSIGNED'
when initial_call_type like 'ASSIST%' then 'ASSIST'
when initial_call_type like 'AUTO%' or initial_call_type like 'CAR%' or initial_call_type like 'MVC%' then 'AUTO'
WHEN initial_call_type LIKE 'BOMB%' THEN 'BOMB'
WHEN initial_call_type LIKE 'BURG%' THEN 'BURG'
WHEN initial_call_type LIKE 'CHILD%' THEN 'CHILD'
WHEN initial_call_type LIKE 'DV%' THEN 'DV'
WHEN initial_call_type LIKE 'FIGHT%' THEN 'FIGHT'
WHEN initial_call_type LIKE 'HARBOR%' THEN 'HARBOR'
WHEN initial_call_type LIKE 'JUVENILE%' THEN 'JUVENILE'
WHEN initial_call_type LIKE 'LIQUOR%' THEN 'LIQUOR'
WHEN initial_call_type LIKE 'MISSING%' THEN 'MISSING'
WHEN initial_call_type LIKE 'NARCOTICS%' THEN 'NARCOTICS'
WHEN initial_call_type LIKE 'NOISE%' THEN 'NOISE'
WHEN initial_call_type LIKE 'OBS%' THEN 'OBS'
WHEN initial_call_type LIKE 'ORDER%' THEN 'ORDER'
WHEN initial_call_type LIKE 'OUT%' THEN 'OUT'
WHEN initial_call_type LIKE 'PERSON%' THEN 'PERSON'
WHEN initial_call_type LIKE 'PROPERTY%' THEN 'PROPERTY'
WHEN initial_call_type LIKE 'ROBBERY%' THEN 'ROBBERY'
WHEN initial_call_type LIKE 'SHOT%' THEN 'SHOT'
WHEN initial_call_type LIKE 'SUICIDE%' THEN 'SUICIDE'
WHEN initial_call_type LIKE 'SUSPICIOUS%' THEN 'SUSPICIOUS'
WHEN initial_call_type LIKE 'THEFT%' THEN 'THEFT'
WHEN initial_call_type LIKE 'THREAT%' THEN 'THREAT'
WHEN initial_call_type LIKE 'TRAF%' THEN 'TRAF'
WHEN initial_call_type LIKE 'TRU%' THEN 'TRU'
WHEN initial_call_type LIKE 'UNKNOWN%' THEN 'UNKNOWN'
WHEN initial_call_type LIKE 'WARRANT%' THEN 'WARRANT'
WHEN initial_call_type LIKE 'WEAP%' THEN 'WEAP'
else initial_call_type end as initial_call_type_mapping_ii,
(sum(ph) / sum(cnt)) as initial_pseudo_priority_ii
from initial
group by case WHEN initial_call_type LIKE 'ALARM%' THEN 'ALARM'
WHEN initial_call_type LIKE 'ASLT%' OR initial_call_type LIKE 'ASSAULT%' THEN 'ASSAULT'
WHEN initial_call_type LIKE 'ANIMAL%' THEN 'ANIMAL'
when initial_call_type like 'ASSIGNED DUTY%' then 'ASSIGNED'
when initial_call_type like 'ASSIST%' then 'ASSIST'
when initial_call_type like 'AUTO%' or initial_call_type like 'CAR%' or initial_call_type like 'MVC%' then 'AUTO'
WHEN initial_call_type LIKE 'BOMB%' THEN 'BOMB'
WHEN initial_call_type LIKE 'BURG%' THEN 'BURG'
WHEN initial_call_type LIKE 'CHILD%' THEN 'CHILD'
WHEN initial_call_type LIKE 'DV%' THEN 'DV'
WHEN initial_call_type LIKE 'FIGHT%' THEN 'FIGHT'
WHEN initial_call_type LIKE 'HARBOR%' THEN 'HARBOR'
WHEN initial_call_type LIKE 'JUVENILE%' THEN 'JUVENILE'
WHEN initial_call_type LIKE 'LIQUOR%' THEN 'LIQUOR'
WHEN initial_call_type LIKE 'MISSING%' THEN 'MISSING'
WHEN initial_call_type LIKE 'NARCOTICS%' THEN 'NARCOTICS'
WHEN initial_call_type LIKE 'NOISE%' THEN 'NOISE'
WHEN initial_call_type LIKE 'OBS%' THEN 'OBS'
WHEN initial_call_type LIKE 'ORDER%' THEN 'ORDER'
WHEN initial_call_type LIKE 'OUT%' THEN 'OUT'
WHEN initial_call_type LIKE 'PERSON%' THEN 'PERSON'
WHEN initial_call_type LIKE 'PROPERTY%' THEN 'PROPERTY'
WHEN initial_call_type LIKE 'ROBBERY%' THEN 'ROBBERY'
WHEN initial_call_type LIKE 'SHOT%' THEN 'SHOT'
WHEN initial_call_type LIKE 'SUICIDE%' THEN 'SUICIDE'
WHEN initial_call_type LIKE 'SUSPICIOUS%' THEN 'SUSPICIOUS'
WHEN initial_call_type LIKE 'THEFT%' THEN 'THEFT'
WHEN initial_call_type LIKE 'THREAT%' THEN 'THREAT'
WHEN initial_call_type LIKE 'TRAF%' THEN 'TRAF'
WHEN initial_call_type LIKE 'TRU%' THEN 'TRU'
WHEN initial_call_type LIKE 'UNKNOWN%' THEN 'UNKNOWN'
WHEN initial_call_type LIKE 'WARRANT%' THEN 'WARRANT'
WHEN initial_call_type LIKE 'WEAP%' THEN 'WEAP'
case WHEN initial_call_type LIKE 'ALARM%' THEN 'ALARM'
WHEN initial_call_type LIKE 'ASLT%' OR initial_call_type LIKE 'ASSAULT%' THEN 'ASSAULT'
WHEN initial_call_type LIKE 'ANIMAL%' THEN 'ANIMAL'
when initial_call_type like 'ASSIGNED DUTY%' then 'ASSIGNED'
when initial_call_type like 'ASSIST%' then 'ASSIST'
when initial_call_type like 'AUTO%' or initial_call_type like 'CAR%' or initial_call_type like 'MVC%' then 'AUTO'
WHEN initial_call_type LIKE 'BOMB%' THEN 'BOMB'
WHEN initial_call_type LIKE 'BURG%' THEN 'BURG'
WHEN initial_call_type LIKE 'CHILD%' THEN 'CHILD'
WHEN initial_call_type LIKE 'DV%' THEN 'DV'
WHEN initial_call_type LIKE 'FIGHT%' THEN 'FIGHT'
WHEN initial_call_type LIKE 'HARBOR%' THEN 'HARBOR'
WHEN initial_call_type LIKE 'JUVENILE%' THEN 'JUVENILE'
WHEN initial_call_type LIKE 'LIQUOR%' THEN 'LIQUOR'
WHEN initial_call_type LIKE 'MISSING%' THEN 'MISSING'
WHEN initial_call_type LIKE 'NARCOTICS%' THEN 'NARCOTICS'
WHEN initial_call_type LIKE 'NOISE%' THEN 'NOISE'
WHEN initial_call_type LIKE 'OBS%' THEN 'OBS'
WHEN initial_call_type LIKE 'ORDER%' THEN 'ORDER'
WHEN initial_call_type LIKE 'OUT%' THEN 'OUT'
WHEN initial_call_type LIKE 'PERSON%' THEN 'PERSON'
WHEN initial_call_type LIKE 'PROPERTY%' THEN 'PROPERTY'
WHEN initial_call_type LIKE 'ROBBERY%' THEN 'ROBBERY'
WHEN initial_call_type LIKE 'SHOT%' THEN 'SHOT'
WHEN initial_call_type LIKE 'SUICIDE%' THEN 'SUICIDE'
WHEN initial_call_type LIKE 'SUSPICIOUS%' THEN 'SUSPICIOUS'
WHEN initial_call_type LIKE 'THEFT%' THEN 'THEFT'
WHEN initial_call_type LIKE 'THREAT%' THEN 'THREAT'
WHEN initial_call_type LIKE 'TRAF%' THEN 'TRAF'
WHEN initial_call_type LIKE 'TRU%' THEN 'TRU'
WHEN initial_call_type LIKE 'UNKNOWN%' THEN 'UNKNOWN'
WHEN initial_call_type LIKE 'WARRANT%' THEN 'WARRANT'
WHEN initial_call_type LIKE 'WEAP%' THEN 'WEAP'
else initial_call_type end as initial_call_type_mapping_ii,
(sum(ph) / sum(cnt)) as initial_pseudo_priority_ii
from initial
group by case WHEN initial_call_type LIKE 'ALARM%' THEN 'ALARM'
WHEN initial_call_type LIKE 'ASLT%' OR initial_call_type LIKE 'ASSAULT%' THEN 'ASSAULT'
WHEN initial_call_type LIKE 'ANIMAL%' THEN 'ANIMAL'
when initial_call_type like 'ASSIGNED DUTY%' then 'ASSIGNED'
when initial_call_type like 'ASSIST%' then 'ASSIST'
when initial_call_type like 'AUTO%' or initial_call_type like 'CAR%' or initial_call_type like 'MVC%' then 'AUTO'
WHEN initial_call_type LIKE 'BOMB%' THEN 'BOMB'
WHEN initial_call_type LIKE 'BURG%' THEN 'BURG'
WHEN initial_call_type LIKE 'CHILD%' THEN 'CHILD'
WHEN initial_call_type LIKE 'DV%' THEN 'DV'
WHEN initial_call_type LIKE 'FIGHT%' THEN 'FIGHT'
WHEN initial_call_type LIKE 'HARBOR%' THEN 'HARBOR'
WHEN initial_call_type LIKE 'JUVENILE%' THEN 'JUVENILE'
WHEN initial_call_type LIKE 'LIQUOR%' THEN 'LIQUOR'
WHEN initial_call_type LIKE 'MISSING%' THEN 'MISSING'
WHEN initial_call_type LIKE 'NARCOTICS%' THEN 'NARCOTICS'
WHEN initial_call_type LIKE 'NOISE%' THEN 'NOISE'
WHEN initial_call_type LIKE 'OBS%' THEN 'OBS'
WHEN initial_call_type LIKE 'ORDER%' THEN 'ORDER'
WHEN initial_call_type LIKE 'OUT%' THEN 'OUT'
WHEN initial_call_type LIKE 'PERSON%' THEN 'PERSON'
WHEN initial_call_type LIKE 'PROPERTY%' THEN 'PROPERTY'
WHEN initial_call_type LIKE 'ROBBERY%' THEN 'ROBBERY'
WHEN initial_call_type LIKE 'SHOT%' THEN 'SHOT'
WHEN initial_call_type LIKE 'SUICIDE%' THEN 'SUICIDE'
WHEN initial_call_type LIKE 'SUSPICIOUS%' THEN 'SUSPICIOUS'
WHEN initial_call_type LIKE 'THEFT%' THEN 'THEFT'
WHEN initial_call_type LIKE 'THREAT%' THEN 'THREAT'
WHEN initial_call_type LIKE 'TRAF%' THEN 'TRAF'
WHEN initial_call_type LIKE 'TRU%' THEN 'TRU'
WHEN initial_call_type LIKE 'UNKNOWN%' THEN 'UNKNOWN'
WHEN initial_call_type LIKE 'WARRANT%' THEN 'WARRANT'
WHEN initial_call_type LIKE 'WEAP%' THEN 'WEAP'
else initial_call_type end
),

final as (
select
final_call_type,
cast(priority as float) as priority,
count(*) as cnt,
(cast(priority as float) * count(*)) as ph
FROM gt.dbo.call_data_20251019_processed
group by final_call_type, priority
),

final_pseudo_priority_i as (
select 
final_call_type as final_call_type_i,
(sum(ph) / sum(cnt)) as final_pseudo_priority_i
from final
group by final_call_type
),

final_pseudo_priority_ii as (
select 
case WHEN final_call_type LIKE 'ALARM%' THEN 'ALARM'
WHEN final_call_type LIKE 'ASLT%' OR final_call_type LIKE 'ASSAULT%' THEN 'ASSAULT'
WHEN final_call_type LIKE 'ANIMAL%' THEN 'ANIMAL'
when final_call_type like 'ASSIGNED DUTY%' then 'ASSIGNED'
when final_call_type like 'ASSIST%' then 'ASSIST'
when final_call_type like 'AUTO%' or final_call_type like 'CAR%' or final_call_type like 'MVC%' then 'AUTO'
WHEN final_call_type LIKE 'BOMB%' THEN 'BOMB'
WHEN final_call_type LIKE 'BURG%' THEN 'BURG'
WHEN final_call_type LIKE 'CHILD%' THEN 'CHILD'
WHEN final_call_type LIKE 'DV%' THEN 'DV'
WHEN final_call_type LIKE 'FIGHT%' THEN 'FIGHT'
WHEN final_call_type LIKE 'HARBOR%' THEN 'HARBOR'
WHEN final_call_type LIKE 'JUVENILE%' THEN 'JUVENILE'
WHEN final_call_type LIKE 'LIQUOR%' THEN 'LIQUOR'
WHEN final_call_type LIKE 'MISSING%' THEN 'MISSING'
WHEN final_call_type LIKE 'NARCOTICS%' THEN 'NARCOTICS'
WHEN final_call_type LIKE 'NOISE%' THEN 'NOISE'
WHEN final_call_type LIKE 'OBS%' THEN 'OBS'
WHEN final_call_type LIKE 'ORDER%' THEN 'ORDER'
WHEN final_call_type LIKE 'OUT%' THEN 'OUT'
WHEN final_call_type LIKE 'PERSON%' THEN 'PERSON'
WHEN final_call_type LIKE 'PROPERTY%' THEN 'PROPERTY'
WHEN final_call_type LIKE 'ROBBERY%' THEN 'ROBBERY'
WHEN final_call_type LIKE 'SHOT%' THEN 'SHOT'
WHEN final_call_type LIKE 'SUICIDE%' THEN 'SUICIDE'
WHEN final_call_type LIKE 'SUSPICIOUS%' THEN 'SUSPICIOUS'
WHEN final_call_type LIKE 'THEFT%' THEN 'THEFT'
WHEN final_call_type LIKE 'THREAT%' THEN 'THREAT'
WHEN final_call_type LIKE 'TRAF%' THEN 'TRAF'
WHEN final_call_type LIKE 'TRU%' THEN 'TRU'
WHEN final_call_type LIKE 'UNKNOWN%' THEN 'UNKNOWN'
WHEN final_call_type LIKE 'WARRANT%' THEN 'WARRANT'
WHEN final_call_type LIKE 'WEAP%' THEN 'WEAP'
else final_call_type end as final_call_type_mapping_ii,
(sum(ph) / sum(cnt)) as final_pseudo_priority_ii
from final
group by case WHEN final_call_type LIKE 'ALARM%' THEN 'ALARM'
WHEN final_call_type LIKE 'ASLT%' OR final_call_type LIKE 'ASSAULT%' THEN 'ASSAULT'
WHEN final_call_type LIKE 'ANIMAL%' THEN 'ANIMAL'
when final_call_type like 'ASSIGNED DUTY%' then 'ASSIGNED'
when final_call_type like 'ASSIST%' then 'ASSIST'
when final_call_type like 'AUTO%' or final_call_type like 'CAR%' or final_call_type like 'MVC%' then 'AUTO'
WHEN final_call_type LIKE 'BOMB%' THEN 'BOMB'
WHEN final_call_type LIKE 'BURG%' THEN 'BURG'
WHEN final_call_type LIKE 'CHILD%' THEN 'CHILD'
WHEN final_call_type LIKE 'DV%' THEN 'DV'
WHEN final_call_type LIKE 'FIGHT%' THEN 'FIGHT'
WHEN final_call_type LIKE 'HARBOR%' THEN 'HARBOR'
WHEN final_call_type LIKE 'JUVENILE%' THEN 'JUVENILE'
WHEN final_call_type LIKE 'LIQUOR%' THEN 'LIQUOR'
WHEN final_call_type LIKE 'MISSING%' THEN 'MISSING'
WHEN final_call_type LIKE 'NARCOTICS%' THEN 'NARCOTICS'
WHEN final_call_type LIKE 'NOISE%' THEN 'NOISE'
WHEN final_call_type LIKE 'OBS%' THEN 'OBS'
WHEN final_call_type LIKE 'ORDER%' THEN 'ORDER'
WHEN final_call_type LIKE 'OUT%' THEN 'OUT'
WHEN final_call_type LIKE 'PERSON%' THEN 'PERSON'
WHEN final_call_type LIKE 'PROPERTY%' THEN 'PROPERTY'
WHEN final_call_type LIKE 'ROBBERY%' THEN 'ROBBERY'
WHEN final_call_type LIKE 'SHOT%' THEN 'SHOT'
WHEN final_call_type LIKE 'SUICIDE%' THEN 'SUICIDE'
WHEN final_call_type LIKE 'SUSPICIOUS%' THEN 'SUSPICIOUS'
WHEN final_call_type LIKE 'THEFT%' THEN 'THEFT'
WHEN final_call_type LIKE 'THREAT%' THEN 'THREAT'
WHEN final_call_type LIKE 'TRAF%' THEN 'TRAF'
WHEN final_call_type LIKE 'TRU%' THEN 'TRU'
WHEN final_call_type LIKE 'UNKNOWN%' THEN 'UNKNOWN'
WHEN final_call_type LIKE 'WARRANT%' THEN 'WARRANT'
WHEN final_call_type LIKE 'WEAP%' THEN 'WEAP'
case WHEN final_call_type LIKE 'ALARM%' THEN 'ALARM'
WHEN final_call_type LIKE 'ASLT%' OR final_call_type LIKE 'ASSAULT%' THEN 'ASSAULT'
WHEN final_call_type LIKE 'ANIMAL%' THEN 'ANIMAL'
when final_call_type like 'ASSIGNED DUTY%' then 'ASSIGNED'
when final_call_type like 'ASSIST%' then 'ASSIST'
when final_call_type like 'AUTO%' or final_call_type like 'CAR%' or final_call_type like 'MVC%' then 'AUTO'
WHEN final_call_type LIKE 'BOMB%' THEN 'BOMB'
WHEN final_call_type LIKE 'BURG%' THEN 'BURG'
WHEN final_call_type LIKE 'CHILD%' THEN 'CHILD'
WHEN final_call_type LIKE 'DV%' THEN 'DV'
WHEN final_call_type LIKE 'FIGHT%' THEN 'FIGHT'
WHEN final_call_type LIKE 'HARBOR%' THEN 'HARBOR'
WHEN final_call_type LIKE 'JUVENILE%' THEN 'JUVENILE'
WHEN final_call_type LIKE 'LIQUOR%' THEN 'LIQUOR'
WHEN final_call_type LIKE 'MISSING%' THEN 'MISSING'
WHEN final_call_type LIKE 'NARCOTICS%' THEN 'NARCOTICS'
WHEN final_call_type LIKE 'NOISE%' THEN 'NOISE'
WHEN final_call_type LIKE 'OBS%' THEN 'OBS'
WHEN final_call_type LIKE 'ORDER%' THEN 'ORDER'
WHEN final_call_type LIKE 'OUT%' THEN 'OUT'
WHEN final_call_type LIKE 'PERSON%' THEN 'PERSON'
WHEN final_call_type LIKE 'PROPERTY%' THEN 'PROPERTY'
WHEN final_call_type LIKE 'ROBBERY%' THEN 'ROBBERY'
WHEN final_call_type LIKE 'SHOT%' THEN 'SHOT'
WHEN final_call_type LIKE 'SUICIDE%' THEN 'SUICIDE'
WHEN final_call_type LIKE 'SUSPICIOUS%' THEN 'SUSPICIOUS'
WHEN final_call_type LIKE 'THEFT%' THEN 'THEFT'
WHEN final_call_type LIKE 'THREAT%' THEN 'THREAT'
WHEN final_call_type LIKE 'TRAF%' THEN 'TRAF'
WHEN final_call_type LIKE 'TRU%' THEN 'TRU'
WHEN final_call_type LIKE 'UNKNOWN%' THEN 'UNKNOWN'
WHEN final_call_type LIKE 'WARRANT%' THEN 'WARRANT'
WHEN final_call_type LIKE 'WEAP%' THEN 'WEAP'
else final_call_type end as final_call_type_mapping_ii,
(sum(ph) / sum(cnt)) as final_pseudo_priority_ii
from final
group by case WHEN final_call_type LIKE 'ALARM%' THEN 'ALARM'
WHEN final_call_type LIKE 'ASLT%' OR final_call_type LIKE 'ASSAULT%' THEN 'ASSAULT'
WHEN final_call_type LIKE 'ANIMAL%' THEN 'ANIMAL'
when final_call_type like 'ASSIGNED DUTY%' then 'ASSIGNED'
when final_call_type like 'ASSIST%' then 'ASSIST'
when final_call_type like 'AUTO%' or final_call_type like 'CAR%' or final_call_type like 'MVC%' then 'AUTO'
WHEN final_call_type LIKE 'BOMB%' THEN 'BOMB'
WHEN final_call_type LIKE 'BURG%' THEN 'BURG'
WHEN final_call_type LIKE 'CHILD%' THEN 'CHILD'
WHEN final_call_type LIKE 'DV%' THEN 'DV'
WHEN final_call_type LIKE 'FIGHT%' THEN 'FIGHT'
WHEN final_call_type LIKE 'HARBOR%' THEN 'HARBOR'
WHEN final_call_type LIKE 'JUVENILE%' THEN 'JUVENILE'
WHEN final_call_type LIKE 'LIQUOR%' THEN 'LIQUOR'
WHEN final_call_type LIKE 'MISSING%' THEN 'MISSING'
WHEN final_call_type LIKE 'NARCOTICS%' THEN 'NARCOTICS'
WHEN final_call_type LIKE 'NOISE%' THEN 'NOISE'
WHEN final_call_type LIKE 'OBS%' THEN 'OBS'
WHEN final_call_type LIKE 'ORDER%' THEN 'ORDER'
WHEN final_call_type LIKE 'OUT%' THEN 'OUT'
WHEN final_call_type LIKE 'PERSON%' THEN 'PERSON'
WHEN final_call_type LIKE 'PROPERTY%' THEN 'PROPERTY'
WHEN final_call_type LIKE 'ROBBERY%' THEN 'ROBBERY'
WHEN final_call_type LIKE 'SHOT%' THEN 'SHOT'
WHEN final_call_type LIKE 'SUICIDE%' THEN 'SUICIDE'
WHEN final_call_type LIKE 'SUSPICIOUS%' THEN 'SUSPICIOUS'
WHEN final_call_type LIKE 'THEFT%' THEN 'THEFT'
WHEN final_call_type LIKE 'THREAT%' THEN 'THREAT'
WHEN final_call_type LIKE 'TRAF%' THEN 'TRAF'
WHEN final_call_type LIKE 'TRU%' THEN 'TRU'
WHEN final_call_type LIKE 'UNKNOWN%' THEN 'UNKNOWN'
WHEN final_call_type LIKE 'WARRANT%' THEN 'WARRANT'
WHEN final_call_type LIKE 'WEAP%' THEN 'WEAP'
else final_call_type end
),

agg_data as(
select
cad_event_number,
cad_event_clearance_description,
call_type,
priority,
initial_call_type,
case 
when initial_call_type like 'ALARM%' and priority in ('1', '2', '3') then 'ALARM_lv1'
when initial_call_type like 'ALARM%' and priority in ('4', '5', '6') then 'ALARM_lv2'
when initial_call_type like 'ALARM%' and priority in ('7', '8', '9') then 'ALARM_lv3'
when (initial_call_type like 'ASLT%' or initial_call_type like 'ASSAULT%') and priority in ('1', '2', '3') then 'ASSAULT_lv1'
when (initial_call_type like 'ASLT%' or initial_call_type like 'ASSAULT%') and priority in ('4', '5', '6') then 'ASSAULT_lv2'
when (initial_call_type like 'ASLT%' or initial_call_type like 'ASSAULT%') and priority in ('7', '8', '9') then 'ASSAULT_lv3'
when initial_call_type like 'ANIMAL%' and priority in ('1', '2', '3') then 'ANIMAL_lv1'
when initial_call_type like 'ANIMAL%' and priority in ('4', '5', '6') then 'ANIMAL_lv2'
when initial_call_type like 'ANIMAL%' and priority in ('7', '8', '9') then 'ANIMAL_lv3'
when initial_call_type like 'ASSIGNED DUTY%' and priority in ('1', '2', '3') then 'ASSIGNED_lv1'
when initial_call_type like 'ASSIGNED DUTY%' and priority in ('4', '5', '6') then 'ASSIGNED_lv2'
when initial_call_type like 'ASSIGNED DUTY%' and priority in ('7', '8', '9') then 'ASSIGNED_lv3'
when initial_call_type like 'ASSIST%' and priority in ('1', '2', '3') then 'ASSIST_lv1'
when initial_call_type like 'ASSIST%' and priority in ('4', '5', '6') then 'ASSIST_lv2'
when initial_call_type like 'ASSIST%' and priority in ('7', '8', '9') then 'ASSIST_lv3'
when (initial_call_type like 'AUTO%' or initial_call_type like 'CAR%' or initial_call_type like 'MVC%') and priority in ('1', '2', '3') then 'AUTO_lv1'
when (initial_call_type like 'AUTO%' or initial_call_type like 'CAR%' or initial_call_type like 'MVC%') and priority in ('4', '5', '6') then 'AUTO_lv2'
when (initial_call_type like 'AUTO%' or initial_call_type like 'CAR%' or initial_call_type like 'MVC%') and priority in ('7', '8', '9') then 'AUTO_lv3'
when initial_call_type like 'BOMB%' and priority in ('1', '2', '3') then 'BOMB_lv1'
when initial_call_type like 'BOMB%' and priority in ('4', '5', '6') then 'BOMB_lv2'
when initial_call_type like 'BOMB%' and priority in ('7', '8', '9') then 'BOMB_lv3'
when initial_call_type like 'BURG%' and priority in ('1', '2', '3') then 'BURG_lv1'
when initial_call_type like 'BURG%' and priority in ('4', '5', '6') then 'BURG_lv2'
when initial_call_type like 'BURG%' and priority in ('7', '8', '9') then 'BURG_lv3'
when initial_call_type like 'CHILD%' and priority in ('1', '2', '3') then 'CHILD_lv1'
when initial_call_type like 'CHILD%' and priority in ('4', '5', '6') then 'CHILD_lv2'
when initial_call_type like 'CHILD%' and priority in ('7', '8', '9') then 'CHILD_lv3'
when initial_call_type like 'DV%' and priority in ('1', '2', '3') then 'DV_lv1'
when initial_call_type like 'DV%' and priority in ('4', '5', '6') then 'DV_lv2'
when initial_call_type like 'DV%' and priority in ('7', '8', '9') then 'DV_lv3'
when initial_call_type like 'FIGHT%' and priority in ('1', '2', '3') then 'FIGHT_lv1'
when initial_call_type like 'FIGHT%' and priority in ('4', '5', '6') then 'FIGHT_lv2'
when initial_call_type like 'FIGHT%' and priority in ('7', '8', '9') then 'FIGHT_lv3'
when initial_call_type like 'HARBOR%' and priority in ('1', '2', '3') then 'HARBOR_lv1'
when initial_call_type like 'HARBOR%' and priority in ('4', '5', '6') then 'HARBOR_lv2'
when initial_call_type like 'HARBOR%' and priority in ('7', '8', '9') then 'HARBOR_lv3'
when initial_call_type like 'JUVENILE%' and priority in ('1', '2', '3') then 'JUVENILE_lv1'
when initial_call_type like 'JUVENILE%' and priority in ('4', '5', '6') then 'JUVENILE_lv2'
when initial_call_type like 'JUVENILE%' and priority in ('7', '8', '9') then 'JUVENILE_lv3'
when initial_call_type like 'LIQUOR%' and priority in ('1', '2', '3') then 'LIQUOR_lv1'
when initial_call_type like 'LIQUOR%' and priority in ('4', '5', '6') then 'LIQUOR_lv2'
when initial_call_type like 'LIQUOR%' and priority in ('7', '8', '9') then 'LIQUOR_lv3'
when initial_call_type like 'MISSING%' and priority in ('1', '2', '3') then 'MISSING_lv1'
when initial_call_type like 'MISSING%' and priority in ('4', '5', '6') then 'MISSING_lv2'
when initial_call_type like 'MISSING%' and priority in ('7', '8', '9') then 'MISSING_lv3'
when initial_call_type like 'NARCOTICS%' and priority in ('1', '2', '3') then 'NARCOTICS_lv1'
when initial_call_type like 'NARCOTICS%' and priority in ('4', '5', '6') then 'NARCOTICS_lv2'
when initial_call_type like 'NARCOTICS%' and priority in ('7', '8', '9') then 'NARCOTICS_lv3'
when initial_call_type like 'NOISE%' and priority in ('1', '2', '3') then 'NOISE_lv1'
when initial_call_type like 'NOISE%' and priority in ('4', '5', '6') then 'NOISE_lv2'
when initial_call_type like 'NOISE%' and priority in ('7', '8', '9') then 'NOISE_lv3'
when initial_call_type like 'OBS%' and priority in ('1', '2', '3') then 'OBS_lv1'
when initial_call_type like 'OBS%' and priority in ('4', '5', '6') then 'OBS_lv2'
when initial_call_type like 'OBS%' and priority in ('7', '8', '9') then 'OBS_lv3'
when initial_call_type like 'ORDER%' and priority in ('1', '2', '3') then 'ORDER_lv1'
when initial_call_type like 'ORDER%' and priority in ('4', '5', '6') then 'ORDER_lv2'
when initial_call_type like 'ORDER%' and priority in ('7', '8', '9') then 'ORDER_lv3'
when initial_call_type like 'OUT%' and priority in ('1', '2', '3') then 'OUT_lv1'
when initial_call_type like 'OUT%' and priority in ('4', '5', '6') then 'OUT_lv2'
when initial_call_type like 'OUT%' and priority in ('7', '8', '9') then 'OUT_lv3'
when initial_call_type like 'PERSON%' and priority in ('1', '2', '3') then 'PERSON_lv1'
when initial_call_type like 'PERSON%' and priority in ('4', '5', '6') then 'PERSON_lv2'
when initial_call_type like 'PERSON%' and priority in ('7', '8', '9') then 'PERSON_lv3'
when initial_call_type like 'PROPERTY%' and priority in ('1', '2', '3') then 'PROPERTY_lv1'
when initial_call_type like 'PROPERTY%' and priority in ('4', '5', '6') then 'PROPERTY_lv2'
when initial_call_type like 'PROPERTY%' and priority in ('7', '8', '9') then 'PROPERTY_lv3'
when initial_call_type like 'ROBBERY%' and priority in ('1', '2', '3') then 'ROBBERY_lv1'
when initial_call_type like 'ROBBERY%' and priority in ('4', '5', '6') then 'ROBBERY_lv2'
when initial_call_type like 'ROBBERY%' and priority in ('7', '8', '9') then 'ROBBERY_lv3'
when initial_call_type like 'SHOT%' and priority in ('1', '2', '3') then 'SHOT_lv1'
when initial_call_type like 'SHOT%' and priority in ('4', '5', '6') then 'SHOT_lv2'
when initial_call_type like 'SHOT%' and priority in ('7', '8', '9') then 'SHOT_lv3'
when initial_call_type like 'SUICIDE%' and priority in ('1', '2', '3') then 'SUICIDE_lv1'
when initial_call_type like 'SUICIDE%' and priority in ('4', '5', '6') then 'SUICIDE_lv2'
when initial_call_type like 'SUICIDE%' and priority in ('7', '8', '9') then 'SUICIDE_lv3'
when initial_call_type like 'SUSPICIOUS%' and priority in ('1', '2', '3') then 'SUSPICIOUS_lv1'
when initial_call_type like 'SUSPICIOUS%' and priority in ('4', '5', '6') then 'SUSPICIOUS_lv2'
when initial_call_type like 'SUSPICIOUS%' and priority in ('7', '8', '9') then 'SUSPICIOUS_lv3'
when initial_call_type like 'THEFT%' and priority in ('1', '2', '3') then 'THEFT_lv1'
when initial_call_type like 'THEFT%' and priority in ('4', '5', '6') then 'THEFT_lv2'
when initial_call_type like 'THEFT%' and priority in ('7', '8', '9') then 'THEFT_lv3'
when initial_call_type like 'THREAT%' and priority in ('1', '2', '3') then 'THREAT_lv1'
when initial_call_type like 'THREAT%' and priority in ('4', '5', '6') then 'THREAT_lv2'
when initial_call_type like 'THREAT%' and priority in ('7', '8', '9') then 'THREAT_lv3'
when initial_call_type like 'TRAF%' and priority in ('1', '2', '3') then 'TRAF_lv1'
when initial_call_type like 'TRAF%' and priority in ('4', '5', '6') then 'TRAF_lv2'
when initial_call_type like 'TRAF%' and priority in ('7', '8', '9') then 'TRAF_lv3'
when initial_call_type like 'TRU%' and priority in ('1', '2', '3') then 'TRU_lv1'
when initial_call_type like 'TRU%' and priority in ('4', '5', '6') then 'TRU_lv2'
when initial_call_type like 'TRU%' and priority in ('7', '8', '9') then 'TRU_lv3'
when initial_call_type like 'UNKNOWN%' and priority in ('1', '2', '3') then 'UNKNOWN_lv1'
when initial_call_type like 'UNKNOWN%' and priority in ('4', '5', '6') then 'UNKNOWN_lv2'
when initial_call_type like 'UNKNOWN%' and priority in ('7', '8', '9') then 'UNKNOWN_lv3'
when initial_call_type like 'WARRANT%' and priority in ('1', '2', '3') then 'WARRANT_lv1'
when initial_call_type like 'WARRANT%' and priority in ('4', '5', '6') then 'WARRANT_lv2'
when initial_call_type like 'WARRANT%' and priority in ('7', '8', '9') then 'WARRANT_lv3'
when initial_call_type like 'WEAP%' and priority in ('1', '2', '3') then 'WEAP_lv1'
when initial_call_type like 'WEAP%' and priority in ('4', '5', '6') then 'WEAP_lv2'
when initial_call_type like 'WEAP%' and priority in ('7', '8', '9') then 'WEAP_lv3'
else initial_call_type end as initial_call_type_priority_mapping,

case WHEN initial_call_type LIKE 'ALARM%' THEN 'ALARM'
WHEN initial_call_type LIKE 'ASLT%' OR initial_call_type LIKE 'ASSAULT%' THEN 'ASSAULT'
WHEN initial_call_type LIKE 'ANIMAL%' THEN 'ANIMAL'
when initial_call_type like 'ASSIGNED DUTY%' then 'ASSIGNED'
when initial_call_type like 'ASSIST%' then 'ASSIST'
when initial_call_type like 'AUTO%' or initial_call_type like 'CAR%' or initial_call_type like 'MVC%' then 'AUTO'
WHEN initial_call_type LIKE 'BOMB%' THEN 'BOMB'
WHEN initial_call_type LIKE 'BURG%' THEN 'BURG'
WHEN initial_call_type LIKE 'CHILD%' THEN 'CHILD'
WHEN initial_call_type LIKE 'DV%' THEN 'DV'
WHEN initial_call_type LIKE 'FIGHT%' THEN 'FIGHT'
WHEN initial_call_type LIKE 'HARBOR%' THEN 'HARBOR'
WHEN initial_call_type LIKE 'JUVENILE%' THEN 'JUVENILE'
WHEN initial_call_type LIKE 'LIQUOR%' THEN 'LIQUOR'
WHEN initial_call_type LIKE 'MISSING%' THEN 'MISSING'
WHEN initial_call_type LIKE 'NARCOTICS%' THEN 'NARCOTICS'
WHEN initial_call_type LIKE 'NOISE%' THEN 'NOISE'
WHEN initial_call_type LIKE 'OBS%' THEN 'OBS'
WHEN initial_call_type LIKE 'ORDER%' THEN 'ORDER'
WHEN initial_call_type LIKE 'OUT%' THEN 'OUT'
WHEN initial_call_type LIKE 'PERSON%' THEN 'PERSON'
WHEN initial_call_type LIKE 'PROPERTY%' THEN 'PROPERTY'
WHEN initial_call_type LIKE 'ROBBERY%' THEN 'ROBBERY'
WHEN initial_call_type LIKE 'SHOT%' THEN 'SHOT'
WHEN initial_call_type LIKE 'SUICIDE%' THEN 'SUICIDE'
WHEN initial_call_type LIKE 'SUSPICIOUS%' THEN 'SUSPICIOUS'
WHEN initial_call_type LIKE 'THEFT%' THEN 'THEFT'
WHEN initial_call_type LIKE 'THREAT%' THEN 'THREAT'
WHEN initial_call_type LIKE 'TRAF%' THEN 'TRAF'
WHEN initial_call_type LIKE 'TRU%' THEN 'TRU'
WHEN initial_call_type LIKE 'UNKNOWN%' THEN 'UNKNOWN'
WHEN initial_call_type LIKE 'WARRANT%' THEN 'WARRANT'
WHEN initial_call_type LIKE 'WEAP%' THEN 'WEAP'
else initial_call_type end as initial_call_type_mapping,

final_call_type,
case WHEN final_call_type LIKE 'ALARM%' THEN 'ALARM'
WHEN final_call_type LIKE 'ASLT%' OR final_call_type LIKE 'ASSAULT%' THEN 'ASSAULT'
WHEN final_call_type LIKE 'ANIMAL%' THEN 'ANIMAL'
when final_call_type like 'ASSIGNED DUTY%' then 'ASSIGNED'
when final_call_type like 'ASSIST%' then 'ASSIST'
when final_call_type like 'AUTO%' or final_call_type like 'CAR%' or final_call_type like 'MVC%' then 'AUTO'
WHEN final_call_type LIKE 'BOMB%' THEN 'BOMB'
WHEN final_call_type LIKE 'BURG%' THEN 'BURG'
WHEN final_call_type LIKE 'CHILD%' THEN 'CHILD'
WHEN final_call_type LIKE 'DV%' THEN 'DV'
WHEN final_call_type LIKE 'FIGHT%' THEN 'FIGHT'
WHEN final_call_type LIKE 'HARBOR%' THEN 'HARBOR'
WHEN final_call_type LIKE 'JUVENILE%' THEN 'JUVENILE'
WHEN final_call_type LIKE 'LIQUOR%' THEN 'LIQUOR'
WHEN final_call_type LIKE 'MISSING%' THEN 'MISSING'
WHEN final_call_type LIKE 'NARCOTICS%' THEN 'NARCOTICS'
WHEN final_call_type LIKE 'NOISE%' THEN 'NOISE'
WHEN final_call_type LIKE 'OBS%' THEN 'OBS'
WHEN final_call_type LIKE 'ORDER%' THEN 'ORDER'
WHEN final_call_type LIKE 'OUT%' THEN 'OUT'
WHEN final_call_type LIKE 'PERSON%' THEN 'PERSON'
WHEN final_call_type LIKE 'PROPERTY%' THEN 'PROPERTY'
WHEN final_call_type LIKE 'ROBBERY%' THEN 'ROBBERY'
WHEN final_call_type LIKE 'SHOT%' THEN 'SHOT'
WHEN final_call_type LIKE 'SUICIDE%' THEN 'SUICIDE'
WHEN final_call_type LIKE 'SUSPICIOUS%' THEN 'SUSPICIOUS'
WHEN final_call_type LIKE 'THEFT%' THEN 'THEFT'
WHEN final_call_type LIKE 'THREAT%' THEN 'THREAT'
WHEN final_call_type LIKE 'TRAF%' THEN 'TRAF'
WHEN final_call_type LIKE 'TRU%' THEN 'TRU'
WHEN final_call_type LIKE 'UNKNOWN%' THEN 'UNKNOWN'
WHEN final_call_type LIKE 'WARRANT%' THEN 'WARRANT'
WHEN final_call_type LIKE 'WEAP%' THEN 'WEAP'
case WHEN initial_call_type LIKE 'ALARM%' THEN 'ALARM'
WHEN initial_call_type LIKE 'ASLT%' OR initial_call_type LIKE 'ASSAULT%' THEN 'ASSAULT'
WHEN initial_call_type LIKE 'ANIMAL%' THEN 'ANIMAL'
when initial_call_type like 'ASSIGNED DUTY%' then 'ASSIGNED'
when initial_call_type like 'ASSIST%' then 'ASSIST'
when initial_call_type like 'AUTO%' or initial_call_type like 'CAR%' or initial_call_type like 'MVC%' then 'AUTO'
WHEN initial_call_type LIKE 'BOMB%' THEN 'BOMB'
WHEN initial_call_type LIKE 'BURG%' THEN 'BURG'
WHEN initial_call_type LIKE 'CHILD%' THEN 'CHILD'
WHEN initial_call_type LIKE 'DV%' THEN 'DV'
WHEN initial_call_type LIKE 'FIGHT%' THEN 'FIGHT'
WHEN initial_call_type LIKE 'HARBOR%' THEN 'HARBOR'
WHEN initial_call_type LIKE 'JUVENILE%' THEN 'JUVENILE'
WHEN initial_call_type LIKE 'LIQUOR%' THEN 'LIQUOR'
WHEN initial_call_type LIKE 'MISSING%' THEN 'MISSING'
WHEN initial_call_type LIKE 'NARCOTICS%' THEN 'NARCOTICS'
WHEN initial_call_type LIKE 'NOISE%' THEN 'NOISE'
WHEN initial_call_type LIKE 'OBS%' THEN 'OBS'
WHEN initial_call_type LIKE 'ORDER%' THEN 'ORDER'
WHEN initial_call_type LIKE 'OUT%' THEN 'OUT'
WHEN initial_call_type LIKE 'PERSON%' THEN 'PERSON'
WHEN initial_call_type LIKE 'PROPERTY%' THEN 'PROPERTY'
WHEN initial_call_type LIKE 'ROBBERY%' THEN 'ROBBERY'
WHEN initial_call_type LIKE 'SHOT%' THEN 'SHOT'
WHEN initial_call_type LIKE 'SUICIDE%' THEN 'SUICIDE'
WHEN initial_call_type LIKE 'SUSPICIOUS%' THEN 'SUSPICIOUS'
WHEN initial_call_type LIKE 'THEFT%' THEN 'THEFT'
WHEN initial_call_type LIKE 'THREAT%' THEN 'THREAT'
WHEN initial_call_type LIKE 'TRAF%' THEN 'TRAF'
WHEN initial_call_type LIKE 'TRU%' THEN 'TRU'
WHEN initial_call_type LIKE 'UNKNOWN%' THEN 'UNKNOWN'
WHEN initial_call_type LIKE 'WARRANT%' THEN 'WARRANT'
WHEN initial_call_type LIKE 'WEAP%' THEN 'WEAP'
else initial_call_type end as initial_call_type_mapping,

final_call_type,
case WHEN final_call_type LIKE 'ALARM%' THEN 'ALARM'
WHEN final_call_type LIKE 'ASLT%' OR final_call_type LIKE 'ASSAULT%' THEN 'ASSAULT'
WHEN final_call_type LIKE 'ANIMAL%' THEN 'ANIMAL'
when final_call_type like 'ASSIGNED DUTY%' then 'ASSIGNED'
when final_call_type like 'ASSIST%' then 'ASSIST'
when final_call_type like 'AUTO%' or final_call_type like 'CAR%' or final_call_type like 'MVC%' then 'AUTO'
WHEN final_call_type LIKE 'BOMB%' THEN 'BOMB'
WHEN final_call_type LIKE 'BURG%' THEN 'BURG'
WHEN final_call_type LIKE 'CHILD%' THEN 'CHILD'
WHEN final_call_type LIKE 'DV%' THEN 'DV'
WHEN final_call_type LIKE 'FIGHT%' THEN 'FIGHT'
WHEN final_call_type LIKE 'HARBOR%' THEN 'HARBOR'
WHEN final_call_type LIKE 'JUVENILE%' THEN 'JUVENILE'
WHEN final_call_type LIKE 'LIQUOR%' THEN 'LIQUOR'
WHEN final_call_type LIKE 'MISSING%' THEN 'MISSING'
WHEN final_call_type LIKE 'NARCOTICS%' THEN 'NARCOTICS'
WHEN final_call_type LIKE 'NOISE%' THEN 'NOISE'
WHEN final_call_type LIKE 'OBS%' THEN 'OBS'
WHEN final_call_type LIKE 'ORDER%' THEN 'ORDER'
WHEN final_call_type LIKE 'OUT%' THEN 'OUT'
WHEN final_call_type LIKE 'PERSON%' THEN 'PERSON'
WHEN final_call_type LIKE 'PROPERTY%' THEN 'PROPERTY'
WHEN final_call_type LIKE 'ROBBERY%' THEN 'ROBBERY'
WHEN final_call_type LIKE 'SHOT%' THEN 'SHOT'
WHEN final_call_type LIKE 'SUICIDE%' THEN 'SUICIDE'
WHEN final_call_type LIKE 'SUSPICIOUS%' THEN 'SUSPICIOUS'
WHEN final_call_type LIKE 'THEFT%' THEN 'THEFT'
WHEN final_call_type LIKE 'THREAT%' THEN 'THREAT'
WHEN final_call_type LIKE 'TRAF%' THEN 'TRAF'
WHEN final_call_type LIKE 'TRU%' THEN 'TRU'
WHEN final_call_type LIKE 'UNKNOWN%' THEN 'UNKNOWN'
WHEN final_call_type LIKE 'WARRANT%' THEN 'WARRANT'
WHEN final_call_type LIKE 'WEAP%' THEN 'WEAP'
else final_call_type end as final_call_type_mapping,

cad_event_original_time_queued,
cast(cad_event_original_time_queued_date as date) as cad_event_original_time_queued_date,
cast(cad_event_original_time_queued_time as time) as cad_event_original_time_queued_time,
try_cast(cad_event_original_time_queued_datetime as datetime2) as cad_event_original_time_queued_datetime,
cad_event_original_time_queued_datetime_hour,
try_cast(cad_event_arrived_time_datetime as datetime2) as cad_event_arrived_time_datetime,
dispatch_precinct,
dispatch_sector,
dispatch_beat,
dispatch_longitude,
dispatch_latitude,
dispatch_reporting_area,
cad_event_response_category,
call_sign_dispatch_id,
try_cast(call_sign_dispatch_time_datetime as datetime2) as call_sign_dispatch_time_datetime,
try_cast(first_care_call_sign_at_scene_time_datetime as datetime2) as first_care_call_sign_at_scene_time_datetime,
try_cast(first_care_call_sign_dispatch_time_datetime as datetime2) as first_care_call_sign_dispatch_time_datetime,
try_cast(first_co_response_call_sign_at_scene_time_datetime as datetime2) as first_co_response_call_sign_at_scene_time_datetime,
try_cast(first_co_response_call_sign_dispatch_time_datetime as datetime2) as first_co_response_call_sign_dispatch_time_datetime,
try_cast(first_spd_call_sign_at_scene_time_datetime as datetime2) as first_spd_call_sign_at_scene_time_datetime,
try_cast(first_spd_call_sign_dispatch_time_datetime as datetime2) as first_spd_call_sign_dispatch_time_datetime,
try_cast(last_care_call_sign_in_service_time_datetime as datetime2) as last_care_call_sign_in_service_time_datetime,
try_cast(last_co_response_call_sign_in_service_time_datetime as datetime2) as last_co_response_call_sign_in_service_time_datetime,
try_cast(last_spd_call_sign_in_service_time_datetime as datetime2) as last_spd_call_sign_in_service_time_datetime,
CAST(REPLACE(care_call_sign_total_service_time_s, ',', '') AS FLOAT) AS care_call_sign_total_service_time_s,
CAST(REPLACE(co_response_call_sign_total_service_time_s, ',', '') AS FLOAT) AS co_response_call_sign_total_service_time_s,
CAST(REPLACE(spd_call_sign_total_service_time_s, ',', '') AS FLOAT) AS spd_call_sign_total_service_time_s,
CAST(REPLACE(call_sign_total_service_time_s, ',', '') AS FLOAT) AS call_sign_total_service_time_s,
CAST(REPLACE(first_care_call_sign_dispatch_delay_time_s, ',', '') AS FLOAT) AS first_care_call_sign_dispatch_delay_time_s,
CAST(REPLACE(first_care_call_sign_response_time_s, ',', '') AS FLOAT) AS first_care_call_sign_response_time_s,
CAST(REPLACE(first_co_response_call_sign_dispatch_delay_time_s, ',', '') AS FLOAT) AS first_co_response_call_sign_dispatch_delay_time_s,
CAST(REPLACE(first_co_response_call_sign_response_time_s, ',', '') AS FLOAT) AS first_co_response_call_sign_response_time_s,
CAST(REPLACE(first_spd_call_sign_dispatch_delay_time_s, ',', '') AS FLOAT) AS first_spd_call_sign_dispatch_delay_time_s,
CAST(REPLACE(first_spd_call_sign_response_time_s, ',', '') AS FLOAT) AS first_spd_call_sign_response_time_s,
CAST(REPLACE(call_sign_dispatch_delay_time_s, ',', '') AS FLOAT) AS call_sign_dispatch_delay_time_s,
CAST(REPLACE(call_sign_response_time_s, ',', '') AS FLOAT) AS call_sign_response_time_s,
try_cast(call_sign_at_scene_time_datetime as datetime2) as call_sign_at_scene_time_datetime,
CAST(REPLACE(cad_event_first_response_time_s, ',', '') AS FLOAT) AS cad_event_first_response_time_s,
try_cast(call_sign_in_service_time_datetime as datetime2) as call_sign_in_service_time_datetime,
call_type_indicator,
dispatch_neighborhood,
call_type_received_classification,
dispatch_address,
count_of_officers
FROM gt.dbo.call_data_20251019_processed
where cast(cad_event_original_time_queued_date as date) is not NULL
and (CAST(REPLACE(call_sign_total_service_time_s, ',', '') AS FLOAT) > 0)
and (cad_event_clearance_description not in ('CCR only - COMMUNITY PRESENCE',
'CCR only - INTERPERSONAL SUPPORT ONLY', 
'CCR only - RESOURCES OR SUPPLIES PROVIDED',
'CCR only - UNABLE TO LOCATE',
'DUPLICATE EVENT',
'FK ERROR',
'RADIO BROADCAST AND CLEAR')
or call_type not in ('HISTORY CALL (RETRO)',
'IN PERSON COMPLAINT',
'POLICE (VARDA) ALARM',
'PROACTIVE (OFFICER INITIATED)',
'SCHEDULED EVENT (RECURRING)')
or dispatch_sector not in ('HARBOR'))
), -- 10,418,709 record count


agg_data_ii as (
select
*,
/*
When initial call and final call match, use priority
When initial call and final call do not match refer to exact final priority
When initial call and final call do no match and final priority is not there use pseudo final call mapping priority value
When initial call and final call do no match and final priority/pseudo final priority do not match then use pseudo initial call mapping priority value
Else use priority
*/
case when initial_call_type = final_call_type then priority
when final_call_type = final_call_type_i then final_pseudo_priority_i
when final_call_type_mapping = final_call_type_mapping_ii then final_pseudo_priority_ii
when initial_call_type_mapping = initial_call_type_mapping_ii then initial_pseudo_priority_ii
else priority end as pseudo_priority_score,
row_number() over (partition by cad_event_number
order by cad_event_original_time_queued_datetime, call_sign_response_time_s, call_sign_dispatch_delay_time_s) as rnk
from agg_data a
left join initial_pseudo_priority_i b
on a.initial_call_type = b.initial_call_type_i
left join initial_pseudo_priority_ii c
on a.initial_call_type_mapping = c.initial_call_type_mapping_ii
left join final_pseudo_priority_i d
on a.final_call_type = d.final_call_type_i
left join final_pseudo_priority_ii e
on a.final_call_type_mapping = e.final_call_type_mapping_ii
), -- 10,418,709

agg_data_iii as (
) -- 10,418,709

select
cad_event_number
,cad_event_clearance_description
,replace(call_type, ',', '') as call_type
,priority
,replace(initial_call_type, ',', '') as initial_call_type
,replace(initial_call_type_priority_mapping, ',', '') as initial_call_type_priority_mapping
,replace(initial_call_type_mapping, ',', '') as initial_call_type_mapping
,replace(final_call_type, ',', '') as final_call_type
,replace(final_call_type_mapping, ',', '') as final_call_type_mapping
,cad_event_original_time_queued
,cad_event_original_time_queued_date
,cad_event_original_time_queued_time
,cad_event_original_time_queued_datetime
,cad_event_original_time_queued_datetime_hour
,cad_event_arrived_time_datetime
,dispatch_precinct
,dispatch_sector
,dispatch_beat
,dispatch_longitude
,dispatch_latitude
,dispatch_reporting_area
,cad_event_response_category
,call_sign_dispatch_id
,call_sign_dispatch_time_datetime
,first_care_call_sign_at_scene_time_datetime
,first_care_call_sign_dispatch_time_datetime
,first_co_response_call_sign_at_scene_time_datetime
,first_co_response_call_sign_dispatch_time_datetime
,first_spd_call_sign_at_scene_time_datetime
,first_spd_call_sign_dispatch_time_datetime
,last_care_call_sign_in_service_time_datetime
,last_co_response_call_sign_in_service_time_datetime
,last_spd_call_sign_in_service_time_datetime
,care_call_sign_total_service_time_s
,co_response_call_sign_total_service_time_s
,spd_call_sign_total_service_time_s
,call_sign_total_service_time_s
,first_care_call_sign_dispatch_delay_time_s
,first_care_call_sign_response_time_s
,first_co_response_call_sign_dispatch_delay_time_s
,first_co_response_call_sign_response_time_s
,first_spd_call_sign_dispatch_delay_time_s
,first_spd_call_sign_response_time_s
,call_sign_dispatch_delay_time_s
,call_sign_response_time_s
,call_sign_at_scene_time_datetime
,cad_event_first_response_time_s
,call_sign_in_service_time_datetime
,call_type_indicator
,dispatch_neighborhood
,call_type_received_classification
,dispatch_address
,count_of_officers
,pseudo_priority_score
from agg_data_ii
where rnk = 1
and cad_event_original_time_queued_date >= '2023-10-27'
), -- 641,904

quartiles AS (
SELECT 
PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY call_sign_total_service_time_s) OVER () AS Q1,
PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY call_sign_total_service_time_s) OVER () AS Q3
FROM agg_data_iii
WHERE call_sign_total_service_time_s IS NOT NULL
),

IQR_Calc AS (
SELECT TOP 1
Q1,
Q3,
(Q3 - Q1) AS IQR,
(Q1 - 1.5 * (Q3 - Q1)) AS LowerBound,
(Q3 + 1.5 * (Q3 - Q1)) AS UpperBound
FROM Quartiles
)

SELECT 
*
into gt.dbo.call_data_20251019_processed_v4
FROM agg_data_iii t
WHERE t.call_sign_total_service_time_s IS NOT NULL
AND t.call_sign_total_service_time_s >= (SELECT LowerBound FROM IQR_Calc)
AND t.call_sign_total_service_time_s <= (SELECT UpperBound FROM IQR_Calc)
-- 583,022
into gt.dbo.call_data_20251019_processed_v3
from agg_data_ii
where rnk = 1
and cad_event_original_time_queued_date >= '2023-10-27'
