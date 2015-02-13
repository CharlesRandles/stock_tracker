#!/bin/bash

echo "Creating database of holdings"
DB=holdings.db

sqlite3 $DB < createHoldings.sql
sqlite3 $DB < createConfig.sql
sqlite3 $DB < createCache.sql

