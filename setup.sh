#!/bin/bash
export DATABASE_URL="postgresql://postgres:1234567890@fsnd-db.cud9wfdw2uig.us-east-2.rds.amazonaws.com:5432/fsnd_db"
export EXCITED="true"
export FLASK_APP=app
export FLASK_DEBUG=true 
echo "setup.sh script executed successfully!"