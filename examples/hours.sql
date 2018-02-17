WITH RECURSIVE hours(hour) AS (
	SELECT
		0
	UNION
	SELECT
		hour + 1
	FROM
		hours
	LIMIT
		24
)
SELECT
	hour,
	IFNULL(
		(SELECT
			SUM(bytes_sent + bytes_received)
		FROM
			traffic
		WHERE
			STRFTIME("%H", timestamp_begin, "unixepoch") = PRINTF("%02d", hour)
		) / 1024 / 1024,
		0
	) AS traffic_MiB
FROM
	hours
ORDER BY
	hour ASC
;
