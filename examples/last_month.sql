WITH RECURSIVE last_month(month_date, timestamp_begin, timestamp_end) AS (
	SELECT
		DATE("now"),
		STRFTIME("%s", DATE("now")),
		STRFTIME("%s", DATE("now", "+1 day"))
	UNION
	SELECT
		DATE(month_date, "-1 day"),
		STRFTIME("%s", DATE(month_date, "-1 day")),
		STRFTIME("%s", month_date)
	FROM
		last_month
	WHERE
		month_date > date("now", "-1 month")
)
SELECT
	month_date,
	IFNULL(
		(SELECT
			SUM(bytes_sent + bytes_received)
		FROM
			traffic
		WHERE
			traffic.timestamp_begin >= last_month.timestamp_begin
			AND traffic.timestamp_end < last_month.timestamp_end
		) / 1024 / 1024,
		0
	) AS traffic_MiB
FROM
	last_month
ORDER BY
	month_date ASC
;
