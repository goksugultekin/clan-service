WITH base AS (
  SELECT
    event_date,
    country,
    platform,
    user_id,
    SUM(total_session_count) AS total_session_count,
    SUM(total_session_match_duration) AS total_session_match_duration,
    SUM(start_count) AS start_count,
    SUM(match_end_count) AS match_end_count,
    SUM(victory_count) AS victory_count,
    SUM(defeat_count) AS defeat_count,
    SUM(server_connection_error) AS server_connection_error,
    SUM(iap_revenue) AS iap_revenue,
    SUM(ad_revenue) AS ad_revenue
  FROM `clan-service-project.game_raw.daily_user_events`
  GROUP BY event_date, country, platform, user_id
),



agg AS (
  SELECT
    event_date,
    country,
    platform,
    COUNT(DISTINCT user_id) AS dau,
    SUM(iap_revenue) AS total_iap_revenue,
    SUM(ad_revenue) AS total_ad_revenue,
    (SUM(iap_revenue) + SUM(ad_revenue)) / NULLIF(COUNT(DISTINCT user_id), 0) AS arpdau,
    SUM(start_count) AS matches_started,
    SUM(start_count) / NULLIF(COUNT(DISTINCT user_id), 0) AS match_per_dau,
    SUM(victory_count) / NULLIF(SUM(match_end_count), 0) AS win_ratio,
    SUM(defeat_count) / NULLIF(SUM(match_end_count), 0) AS defeat_ratio,
    SUM(server_connection_error) / NULLIF(COUNT(DISTINCT user_id), 0) AS server_error_per_dau
  FROM base
  GROUP BY event_date, country, platform
)

SELECT
  event_date,
  country,
  platform,
  dau,
  total_iap_revenue,
  total_ad_revenue,
  arpdau,
  matches_started,
  match_per_dau,
  win_ratio,
  defeat_ratio,
  server_error_per_dau
FROM agg
ORDER BY event_date DESC;
