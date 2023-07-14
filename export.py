import csv

with open("products.csv", "r", encoding="utf-8", newline="") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
    for row in spamreader:
        print(", ".join(row))
        print(row)
