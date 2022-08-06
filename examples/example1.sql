SELECT
"users_user"."id",
"users_user"."first_name",
"users_user"."second_name",
"users_user"."last_name",
"users_user"."email",
"users_user"."address",
"users_user"."phone_number",
"users_user"."company_id",
"users_user"."job_id",
CONCAT(
"users_user"."last_name",
CONCAT(
' ',
CONCAT(
"users_user"."first_name",
CONCAT(' ', "users_user"."second_name")
)
)
) AS "fio",
"users_company"."title" as company_title,
"users_job"."title" as job_title
FROM
"users_user"
INNER JOIN "users_company" ON (
"users_user"."company_id" = "users_company"."id"
)
INNER JOIN "users_job" ON (
"users_user"."job_id" = "users_job"."id"
)
WHERE (UPPER("users_user"."id"::text) = UPPER('aboba') OR UPPER("users_user"."first_name"::text) LIKE UPPER('aboba%') OR UPPER("users_user"."last_name"::text) LIKE UPPER('aboba%'));
