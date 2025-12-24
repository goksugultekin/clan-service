
  
    

    create or replace table `clan-service-project`.`game_analytics`.`daily_metrics`
      
    
    

    
    OPTIONS()
    as (
      -- models/daily_metrics.sql
WITH base AS (
  SELECT
    event_date,
    country,
    platform,
    user_id,
    SUM(total_session_count)          AS total_session_count,
    SUM(total_session_duration)       AS total_session_duration,
    SUM(match_start_count)            AS match_start_count,
    SUM(match_end_count)              AS match_end_count,
    SUM(victory_count)                AS victory_count,
    SUM(defeat_count)                 AS defeat_count,
    SUM(server_connection_error)      AS server_connection_error,
    SUM(iap_revenue)                  AS iap_revenue,
    SUM(ad_revenue)                   AS ad_revenue
  FROM `clan-service-project.game_raw.daily_user_events`
  GROUP BY 1,2,3,4
)

SELECT
  event_date,
  country,
  platform,
  COUNT(DISTINCT user_id)                                AS dau,
  SUM(iap_revenue)                                       AS total_iap_revenue,
  SUM(ad_revenue)                                        AS total_ad_revenue,
  SAFE_DIVIDE(SUM(iap_revenue) + SUM(ad_revenue),
              COUNT(DISTINCT user_id))                   AS arpdau,
  SUM(match_start_count)                                 AS matches_started,
  SAFE_DIVIDE(SUM(match_start_count),
              COUNT(DISTINCT user_id))                   AS match_per_dau,
  SAFE_DIVIDE(SUM(victory_count),
              NULLIF(SUM(match_end_count), 0))           AS win_ratio,
  SAFE_DIVIDE(SUM(defeat_count),
              NULLIF(SUM(match_end_count), 0))           AS defeat_ratio,
  SAFE_DIVIDE(SUM(server_connection_error),
              NULLIF(COUNT(DISTINCT user_id), 0))        AS server_error_per_dau
FROM base
GROUP BY 1,2,3
ORDER BY event_date DESC
    );
  