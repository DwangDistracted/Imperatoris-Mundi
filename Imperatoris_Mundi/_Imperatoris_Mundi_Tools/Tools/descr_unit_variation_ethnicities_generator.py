import csv

def writeEntriesToDescrFile(descrFile, entryEthnicities, entryRegions):
	for regionName in entryRegions:
		entry = f"{regionName}"
		entry += "\n{\n"
		for ethnicity in entryEthnicities:
			ethnicityName = ethnicity[0]
			ethnicityDistribution = ethnicity[1]
			entry += "\tvariant\n\t{\n\t\tethnicity "
			entry += f"{ethnicityName}"
			entry += "\n\t\tdistribution "
			entry += f"{ethnicityDistribution}"
			entry += "\n\t}\n"
		entry += "}\n"
		descrFile.write(entry)
	return;

sourceCSV = open(r"region_ethnicities.csv", "r")
descrFile = open(r"region_ethnicities_paste_into_descr_unit_variation.txt", "w")

csvreader = csv.reader(sourceCSV)
header = next(csvreader)

for row in csvreader:
	entryLabel = row[0]
	entryEthnicities = []
	entryRegions = row[2].split(";")

	rowEthnicities = row[1].split(';')
	for n in range(0, len(rowEthnicities), 2):
		entryEthnicities.append((rowEthnicities[n], int(rowEthnicities[n+1])))

	totalPercentage = 0
	for eth in entryEthnicities:
		totalPercentage += eth[1]

	if (totalPercentage != 100):
		print(f"ERROR - {entryLabel} has improper breakdown of ethnicities")
	else:
		print(f"INFO - {entryLabel} has {len(entryRegions)} regions with ethnicities {entryEthnicities}")
		writeEntriesToDescrFile(descrFile, entryEthnicities, entryRegions)

sourceCSV.close()
descrFile.close()