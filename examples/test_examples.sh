#!/bin/sh

# example0.sql
python ../main.py all -q "SELECT x.id, x.name, y.name from x join y on x.id = y.id where x.id > 2" -s '{"x":{"id":"INT", "name":"STRING"},"y":{"id":"INT","name":"STRING"}}' -o optimize
