#!/bin/sh

PGPASSWORD="postgres!" pg_dump -h localhost -U postgres postgres | gzip > /media/backup/rayapp_`date "+%Y-%m-%d_%H.%M.%S"`.sql.gz