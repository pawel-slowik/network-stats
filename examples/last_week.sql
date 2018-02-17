WITH RECURSIVE last_week(week_date, timestamp_begin, timestamp_end) AS (
	SELECT
		DATE("now"),
		STRFTIME("%s", DATE("now")),
		STRFTIME("%s", DATE("now", "+1 day"))
	UNION
	SELECT
		DATE(week_date, "-1 day"),
		STRFTIME("%s", DATE(week_date, "-1 day")),
		STRFTIME("%s", week_date)
	FROM
		last_week
	LIMIT
		7
)
SELECT
	week_date,
	IFNULL(
		(SELECT
			SUM(bytes_sent + bytes_received)
		FROM
			traffic
		WHERE
			traffic.timestamp_begin >= last_week.timestamp_begin
			AND traffic.timestamp_end < last_week.timestamp_end
		) / 1024 / 1024,
		0
	) AS traffic_MiB
FROM
	last_week
ORDER BY
	week_date ASC
;
