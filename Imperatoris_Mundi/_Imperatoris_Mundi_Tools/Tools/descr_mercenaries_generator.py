# descr_mercenaries generator
import csv
import math

COST_PER_XP = 15

class MercUnitEntry:
    def __init__(self, unit_name, xp, cost, replenish_low, replenish_high, max_pool, initial):
        self.name = unit_name
        self.xp = xp
        self.cost = cost
        self.replenish_low = replenish_low
        self.replenish_high = replenish_high
        self.max_pool = max_pool
        self.initial = initial

def importUnitCosts():
    unit_costs = {}
    unitClassCostModifiers = {
        "Elephant": 2,
        "Chariot": 1.6,
        "Cavalry": 1.4,
        "Archer": 1.2,
        "Infantry": 1
    }

    costsCSV = open(r"mercenary_costs.csv", "r")
    csvreader = csv.reader(costsCSV)
    header = next(csvreader)
    for row in csvreader:
        unitName = row[0]
        unitCost = int(row[1])
        unitClass = row[2]
        if not unitCost:
            print("FATAL: No cost for Unit '{0}' provided.".format(unitName))
            quit()

        if not unitClass in unitClassCostModifiers:
            print("FATAL: Unknown Class {0} for Unit '{1}' provided.".format(unitClass, unitName))
            quit()

        costModifier = unitClassCostModifiers[unitClass]
        unit_costs[unitName] = int(unitCost * costModifier)
    costsCSV.close()
    return unit_costs

def importUnitGrades():
    unit_grades = {}
    gradesCSV = open(r"mercenary_replenish_rate.csv", "r")
    csvreader = csv.reader(gradesCSV)
    header = next(csvreader)
    for row in csvreader:
        grade = row[0]
        unitReplenishLow = float(row[1])
        if not unitReplenishLow or (unitReplenishLow < 0.00) or math.isclose(0.00, unitReplenishLow):
            print("FATAL: Invalid low replenishment for Grade '{0}'".format(grade))
            quit()
        unitReplenishHigh = float(row[2])
        if not unitReplenishHigh or (unitReplenishHigh < unitReplenishLow):
            unitReplenishHigh = unitReplenishLow
            print("WARNING: Grade '{0}' has invalid high replenishment. Defaulting to same as low.".format(grade))

        unit_grades[grade] = (unitReplenishLow, unitReplenishHigh)

    gradesCSV.close()
    return unit_grades

def importPoolRegions():
    pool_regions = {}
    regionNamesFile = open(r"region_names.txt", "r")
    regionNames = regionNamesFile.read().split('\n')
    regionNamesFile.close()

    regionsCSV = open(r"mercenary_regions.csv", "r")
    csvreader = csv.reader(regionsCSV)
    header = next(csvreader)

    for row in csvreader:
        poolName = row[1]
        if not poolName:
            print("FATAL: Unnamed Pool.")
            quit()

        poolRegions = row[2:]
        if not poolRegions or poolRegions[0] == '':
            print("FATAL: Pool {0} has no regions".format(poolName))
            quit()

        for region in poolRegions:
            if not region in regionNames and region != '':
                print("FATAL: Region {0} does not exist".format(region))
                quit()

        pool_regions[poolName]=poolRegions

    regionsCSV.close()
    return pool_regions

def importPoolUnits(unit_grades, unit_costs, pool_regions):
    pool_units = {}
    unitsCSV = open(r"mercenary_units.csv", "r")
    csvreader = csv.reader(unitsCSV)
    header = next(csvreader)
    for row in csvreader:
        poolName = row[0]
        unitName = row[1]
        if not poolName or not poolName in pool_regions:
            print("WARNING: Unknown Pool '{0}'. Skipping Unit Entry for unit {1}...".format(poolName, unitName))
            continue
        if not unitName or not unitName in unit_costs:
            print("FATAL: Invalid unit name '{1}' provided for entry in pool '{0}'".format(poolName, unitName))
            quit()
        
        unitXP = int(row[2])
        if not unitXP and unitXP != 0:
            unitXP = 0
            print("WARNING: Pool '{0}' Unit '{1}' has no XP data. Defaulting to 0.".format(poolName, unitName))
        unitCost = unit_costs[unitName] + (COST_PER_XP * unitXP)
        if not unitCost:
            print("FATAL: No cost for Unit '{0}' provided.".format(unitName))
            quit()

        unitGrade = row[3]
        if not unitGrade:
            print("FATAL: No grade for Unit '{0}' provided in pool '{1}'".format(unitName, poolName))
            quit()
        unitReplenishLow = unit_grades[unitGrade][0]
        unitReplenishHigh = unit_grades[unitGrade][1]

        unitMaxNumber = int(row[4])
        if not unitMaxNumber:
            print("FATAL: Invalid max number for Unit '{0}' provided in pool '{1}'".format(unitName, poolName))
            quit()
        unitInitialNumber = int(row[5])
        if unitInitialNumber is None or (unitInitialNumber > unitMaxNumber):
            unitInitialNumber = unitMaxNumber
            print("WARNING: Pool '{0}' Unit '{1}' has invalid initial number. Defaulting to same as max.".format(poolName, unitName))

        unitEntry = MercUnitEntry(unitName, unitXP, unitCost, unitReplenishLow, unitReplenishHigh, unitMaxNumber, unitInitialNumber)
        if not poolName in pool_units:
            pool_units[poolName] = [unitEntry]
        else:
            pool_units[poolName].append(unitEntry)

    unitsCSV.close()
    return pool_units

# merc unit grades
unit_grades = importUnitGrades()
# merc unit costs
unit_costs = importUnitCosts()
# pool - regions
pool_regions = importPoolRegions()
# pool - units
pool_units=importPoolUnits(unit_grades, unit_costs, pool_regions)

descrFile = open(r"descr_mercenaries.txt", "w")
for pool in pool_regions:
    if not pool in pool_units:
        print("WARNING: Pool '{0}' has no units. Skipping...".format(pool))
        continue

    descrFile.write("\n")
    descrFile.write("pool {0}\n".format(pool))
    descrFile.write("\tregions")
    for region in pool_regions[pool]:
        if not region == '':
            descrFile.write(" {0}".format(region))
    descrFile.write("\n")
    
    for unit in pool_units[pool]:
        descrFile.write("\tunit {0},\t\t\texp {1} cost {2} replenish {3} - {4} max {5} initial {6}\n".format(unit.name, unit.xp, unit.cost, unit.replenish_low, unit.replenish_high, unit.max_pool, unit.initial))

descrFile.close()