#!/bin/bash

echo "Creating database of holdings"

sqlite3 holdings.db -init createHoldings.sql
