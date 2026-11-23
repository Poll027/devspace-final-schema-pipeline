import csv
with open("orders.csv", "r", newline="") as source:
    rows = list(csv.DictReader(source))
