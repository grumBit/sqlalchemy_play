CREATE TABLE prod_pre_aggregations.playable_sessions_daily_interactions20230301 
AS
    SELECT
        "playable_sessions".target_type "playable_sessions__target_type", 
        "playable_sessions".target_uuid "playable_sessions__target_uuid", 
        date_trunc('day', CAST(date_add('minute', 
        timezone_minute("playable_sessions".first_interaction_at AT TIME ZONE 'Australia/Melbourne'),
        date_add('hour', timezone_hour("playable_sessions".first_interaction_at AT TIME ZONE 'Australia/Melbourne'),
        "playable_sessions".first_interaction_at AT TIME ZONE 'Australia/Melbourne')) AS TIMESTAMP)) "playable_sessions__first_interaction_at_day",
        sum("playable_sessions".was_playable_completed) "playable_sessions__sessions_completed_playable", 
        count(*) "playable_sessions__sessions_interacted", 
        sum("playable_sessions".was_playable_played) "playable_sessions__sessions_played_playable", 
        sum("playable_sessions".was_playable_started) "playable_sessions__sessions_started_playable"
    FROM
        apsys_apsys_dev_komodo_eventsdb.fct_vx_playable_sessions 
    AS "playable_sessions"  
    WHERE ("playable_sessions".first_interaction_at >= from_iso8601_timestamp(?) AND "playable_sessions".first_interaction_at <= from_iso8601_timestamp(?))
    GROUP BY 1, 2, 3



Error: Error during create table: 
CREATE TABLE prod_pre_aggregations.playable_sessions_daily_interactions20230301_vpdgkv5i_g2sei2ob_1i2240d 
(
    `playable_sessions__target_type` varchar(255), 
    `playable_sessions__target_uuid` varchar(255), 
    `playable_sessions__first_interaction_at_day` timestamp(3), 
    `playable_sessions__sessions_completed_playable` bigint, 
    `playable_sessions__sessions_interacted` bigint, 
    `playable_sessions__sessions_played_playable` bigint, 
    `playable_sessions__sessions_started_playable` bigint
) 
WITH 
(
    input_format = 'csv_no_header', 
    build_range_end = '2023-03-24T18:52:14.168'
)
LOCATION ?, ?, ?, ?, ?, ?: Internal: ParserError("Expected ',' or ')' after column definition, found: (")

CREATE TABLE grum_test 
(
    `playable_sessions__target_type` varchar(255), 
    `playable_sessions__target_uuid` varchar(255), 
    `playable_sessions__first_interaction_at_day` timestamp(3), 
    `playable_sessions__sessions_completed_playable` bigint, 
    `playable_sessions__sessions_interacted` bigint, 
    `playable_sessions__sessions_played_playable` bigint, 
    `playable_sessions__sessions_started_playable` bigint
) 




CREATE TABLE grum_test 
(
    "playable_sessions__target_type" varchar(255), 
    "playable_sessions__target_uuid" varchar(255), 
    "playable_sessions__first_interaction_at_day" timestamp(3), 
    "playable_sessions__sessions_completed_playable" bigint, 
    "playable_sessions__sessions_interacted" bigint, 
    "playable_sessions__sessions_played_playable" bigint, 
    "playable_sessions__sessions_started_playable" bigint
)
WITH 
(
    input_format = 'csv_no_header', 
    build_range_end = '2023-03-24T18:52:14.168'
)
LOCATION "arn:aws:s3:::tmp-grum"


