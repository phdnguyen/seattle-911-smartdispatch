

select
[cad event number] as cad_event_number,
[cad event clearance description] as cad_event_clearance_description,
[call type] as call_type,
[priority] as priority,
[initial call type] as initial_call_type,
[final call type] as final_call_type,
[cad event original time queued] as cad_event_original_time_queued,
case when [cad event original time queued] like '' then null 
else cast(convert(varchar(10), convert(datetime, [cad event original time queued], 0), 23) as date) end as cad_event_original_time_queued_date,
case when [cad event original time queued] like '' then null 
else cast(try_convert(datetime, [cad event original time queued]) as time) end as cad_event_original_time_queued_time,
case when [cad event original time queued] like '' then null 
else cast(try_convert(datetime, [cad event original time queued]) as datetime2) end as cad_event_original_time_queued_datetime,
case when [cad event original time queued] like '' then null 
else cast(datepart(hour, [cad event original time queued]) as int) end as cad_event_original_time_queued_datetime_hour,

[cad event arrived time] as cad_event_arrived_time,
case when [cad event arrived time] like '' then null 
else cast(convert(varchar(10), convert(datetime, [cad event arrived time], 0), 23) as date) end as cad_event_arrived_time_date,
case when [cad event arrived time] like '' then null 
else cast(try_convert(datetime, [cad event arrived time]) as time) end as cad_event_arrived_time_time,
case when [cad event arrived time] like '' then null 
else cast(try_convert(datetime, [cad event arrived time]) as datetime2) end as cad_event_arrived_time_datetime,
case when [cad event arrived time] like '' then null 
else cast(datepart(hour, [cad event arrived time]) as int) end as cad_event_arrived_time_hour,

[dispatch precinct] as dispatch_precinct,
[dispatch sector] as dispatch_sector,
[dispatch beat] as dispatch_beat,
[dispatch longitude] as dispatch_longitude,
[dispatch latitude] as dispatch_latitude,
[dispatch reporting area] as dispatch_reporting_area,
[cad event response category] as cad_event_response_category,
[call sign dispatch id] as call_sign_dispatch_id,

[call sign dispatch time] as call_sign_dispatch_time,
case when [call sign dispatch time] like '' then null 
else cast(convert(varchar(10), convert(datetime, [call sign dispatch time], 0), 23) as date) end as call_sign_dispatch_time_date,
case when [call sign dispatch time] like '' then null 
else cast(try_convert(datetime, [call sign dispatch time]) as time) end as call_sign_dispatch_time_time,
case when [call sign dispatch time] like '' then null 
else cast(try_convert(datetime, [call sign dispatch time]) as datetime2) end as call_sign_dispatch_time_datetime,
case when [call sign dispatch time] like '' then null 
else cast(datepart(hour, [call sign dispatch time]) as int) end as call_sign_dispatch_time_hour,

[first care call sign at scene time] as first_care_call_sign_at_scene_time,
case when [first care call sign at scene time] like '' then null 
else cast(convert(varchar(10), convert(datetime, [first care call sign at scene time], 0), 23) as date) end as first_care_call_sign_at_scene_time_date,
case when [first care call sign at scene time] like '' then null 
else cast(try_convert(datetime, [first care call sign at scene time]) as time) end as first_care_call_sign_at_scene_time_time,
case when [first care call sign at scene time] like '' then null 
else cast(try_convert(datetime, [first care call sign at scene time]) as datetime2) end as first_care_call_sign_at_scene_time_datetime,
case when [first care call sign at scene time] like '' then null 
else cast(datepart(hour, [first care call sign at scene time]) as int) end as first_care_call_sign_at_scene_time_hour,

-- first care call sign dispatch time
[first care call sign dispatch time] as first_care_call_sign_dispatch_time,
case when [first care call sign dispatch time] like '' then null 
else cast(convert(varchar(10), convert(datetime, [first care call sign dispatch time], 0), 23) as date) end as first_care_call_sign_dispatch_time_date,
case when [first care call sign dispatch time] like '' then null 
else cast(try_convert(datetime, [first care call sign dispatch time]) as time) end as first_care_call_sign_dispatch_time_time,
case when [first care call sign dispatch time] like '' then null 
else cast(try_convert(datetime, [first care call sign dispatch time]) as datetime2) end as first_care_call_sign_dispatch_time_datetime,
case when [first care call sign dispatch time] like '' then null 
else cast(datepart(hour, [first care call sign dispatch time]) as int) end as first_care_call_sign_dispatch_time_hour,

[first co-response call sign at scene time] as first_co_response_call_sign_at_scene_time,
case when [first co-response call sign at scene time] like '' then null 
else cast(convert(varchar(10), convert(datetime, [first co-response call sign at scene time], 0), 23) as date) end as first_co_response_call_sign_at_scene_time_date,
case when [first co-response call sign at scene time] like '' then null 
else cast(try_convert(datetime, [first co-response call sign at scene time]) as time) end as first_co_response_call_sign_at_scene_time_time,
case when [first co-response call sign at scene time] like '' then null 
else cast(try_convert(datetime, [first co-response call sign at scene time]) as datetime2) end as first_co_response_call_sign_at_scene_time_datetime,
case when [first co-response call sign at scene time] like '' then null 
else cast(datepart(hour, [first co-response call sign at scene time]) as int) end as first_co_response_call_sign_at_scene_time_hour,

[first co-response call sign dispatch time] as first_co_response_call_sign_dispatch_time,
case when [first co-response call sign dispatch time] like '' then null 
else cast(convert(varchar(10), convert(datetime, [first co-response call sign dispatch time], 0), 23) as date) end as first_co_response_call_sign_dispatch_time_date,
case when [first co-response call sign dispatch time] like '' then null 
else cast(try_convert(datetime, [first co-response call sign dispatch time]) as time) end as first_co_response_call_sign_dispatch_time_time,
case when [first co-response call sign dispatch time] like '' then null 
else cast(try_convert(datetime, [first co-response call sign dispatch time]) as datetime2) end as first_co_response_call_sign_dispatch_time_datetime,
case when [first co-response call sign dispatch time] like '' then null 
else cast(datepart(hour, [first co-response call sign dispatch time]) as int) end as first_co_response_call_sign_dispatch_time_hour,

[first spd call sign at scene time] as first_spd_call_sign_at_scene_time,
case when [first spd call sign at scene time] like '' then null 
else cast(convert(varchar(10), convert(datetime, [first spd call sign at scene time], 0), 23) as date) end as first_spd_call_sign_at_scene_time_date,
case when [first spd call sign at scene time] like '' then null 
else cast(try_convert(datetime, [first spd call sign at scene time]) as time) end as first_spd_call_sign_at_scene_time_time,
case when [first spd call sign at scene time] like '' then null 
else cast(try_convert(datetime, [first spd call sign at scene time]) as datetime2) end as first_spd_call_sign_at_scene_time_datetime,
case when [first spd call sign at scene time] like '' then null 
else cast(datepart(hour, [first spd call sign at scene time]) as int) end as first_spd_call_sign_at_scene_time_hour,

[first spd call sign dispatch time] as first_spd_call_sign_dispatch_time,
case when [first spd call sign dispatch time] like '' then null 
else cast(convert(varchar(10), convert(datetime, [first spd call sign dispatch time], 0), 23) as date) end as first_spd_call_sign_dispatch_time_date,
case when [first spd call sign dispatch time] like '' then null 
else cast(try_convert(datetime, [first spd call sign dispatch time]) as time) end as first_spd_call_sign_dispatch_time_time,
case when [first spd call sign dispatch time] like '' then null 
else cast(try_convert(datetime, [first spd call sign dispatch time]) as datetime2) end as first_spd_call_sign_dispatch_time_datetime,
case when [first spd call sign dispatch time] like '' then null 
else cast(datepart(hour, [first spd call sign dispatch time]) as int) end as first_spd_call_sign_dispatch_time_hour,

[last care call sign in-service time] as last_care_call_sign_in_service_time,
case when [last care call sign in-service time] like '' then null 
else cast(convert(varchar(10), convert(datetime, [last care call sign in-service time], 0), 23) as date) end as last_care_call_sign_in_service_time_date,
case when [last care call sign in-service time] like '' then null 
else cast(try_convert(datetime, [last care call sign in-service time]) as time) end as last_care_call_sign_in_service_time_time,
case when [last care call sign in-service time] like '' then null 
else cast(try_convert(datetime, [last care call sign in-service time]) as datetime2) end as last_care_call_sign_in_service_time_datetime,
case when [last care call sign in-service time] like '' then null 
else cast(datepart(hour, [last care call sign in-service time]) as int) end as last_care_call_sign_in_service_time_hour,

[last co-response call sign in-service time] as last_co_response_call_sign_in_service_time,
case when [last co-response call sign in-service time] like '' then null 
else cast(convert(varchar(10), convert(datetime, [last co-response call sign in-service time], 0), 23) as date) end as last_co_response_call_sign_in_service_time_date,
case when [last co-response call sign in-service time] like '' then null 
else cast(try_convert(datetime, [last co-response call sign in-service time]) as time) end as last_co_response_call_sign_in_service_time_time,
case when [last co-response call sign in-service time] like '' then null 
else cast(try_convert(datetime, [last co-response call sign in-service time]) as datetime2) end as last_co_response_call_sign_in_service_time_datetime,
case when [last co-response call sign in-service time] like '' then null 
else cast(datepart(hour, [last co-response call sign in-service time]) as int) end as last_co_response_call_sign_in_service_time_hour,

[last spd call sign in-service time] as last_spd_call_sign_in_service_time,
case when [last spd call sign in-service time] like '' then null 
else cast(convert(varchar(10), convert(datetime, [last spd call sign in-service time], 0), 23) as date) end as last_spd_call_sign_in_service_time_date,
case when [last spd call sign in-service time] like '' then null 
else cast(try_convert(datetime, [last spd call sign in-service time]) as time) end as last_spd_call_sign_in_service_time_time,
case when [last spd call sign in-service time] like '' then null 
else cast(try_convert(datetime, [last spd call sign in-service time]) as datetime2) end as last_spd_call_sign_in_service_time_datetime,
case when [last spd call sign in-service time] like '' then null 
else cast(datepart(hour, [last spd call sign in-service time]) as int) end as last_spd_call_sign_in_service_time_hour,

[care call sign total service time (s)] as care_call_sign_total_service_time_s,
[co-response call sign total service time (s)] as co_response_call_sign_total_service_time_s,
[spd call sign total service time (s)] as spd_call_sign_total_service_time_s,
[call sign total service time (s)] as call_sign_total_service_time_s,
[first care call sign dispatch delay time (s)] as first_care_call_sign_dispatch_delay_time_s,
[first care call sign response time (s)] as first_care_call_sign_response_time_s,
[first co-response call sign dispatch delay time (s)] as first_co_response_call_sign_dispatch_delay_time_s,
[first co-response call sign response time (s)] as first_co_response_call_sign_response_time_s,
[first spd call sign dispatch delay time (s)] as first_spd_call_sign_dispatch_delay_time_s,
[first spd call sign response time (s)] as first_spd_call_sign_response_time_s,
[call sign dispatch delay time (s)] as call_sign_dispatch_delay_time_s,
[call sign response time (s)] as call_sign_response_time_s,

[call sign at scene time] as call_sign_at_scene_time,
case when [call sign at scene time] like '' then null 
else cast(convert(varchar(10), convert(datetime, [call sign at scene time], 0), 23) as date) end as call_sign_at_scene_time_date,
case when [call sign at scene time] like '' then null 
else cast(try_convert(datetime, [call sign at scene time]) as time) end as call_sign_at_scene_time_time,
case when [call sign at scene time] like '' then null 
else cast(try_convert(datetime, [call sign at scene time]) as datetime2) end as call_sign_at_scene_time_datetime,
case when [call sign at scene time] like '' then null 
else cast(datepart(hour, [call sign at scene time]) as int) end as call_sign_at_scene_time_hour,

[cad event first response time (s)] as cad_event_first_response_time_s,

[call sign in-service time] as call_sign_in_service_time,
case when [call sign in-service time] like '' then null 
else cast(convert(varchar(10), convert(datetime, [call sign in-service time], 0), 23) as date) end as call_sign_in_service_time_date,
case when [call sign in-service time] like '' then null 
else cast(try_convert(datetime, [call sign in-service time]) as time) end as call_sign_in_service_time_time,
case when [call sign in-service time] like '' then null 
else cast(try_convert(datetime, [call sign in-service time]) as datetime2) end as call_sign_in_service_time_datetime,
case when [call sign in-service time] like '' then null 
else cast(datepart(hour, [call sign in-service time]) as int) end as call_sign_in_service_time_hour,

[call type indicator] as call_type_indicator,
[dispatch neighborhood] as dispatch_neighborhood,
[call type received classification] as call_type_received_classification,
[dispatch address] as dispatch_address,
[count of officers] as count_of_officers
from [gt].[dbo].[call_data_20251019_v2]

