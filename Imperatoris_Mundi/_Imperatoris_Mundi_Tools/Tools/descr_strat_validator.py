# descr_strat validator

descr_strat_path = input("Path to descr_strat : ");

def isValidResource(resourceString):
    validResources = ["gold", "silver", "iron", "pottery", "furs", "grain", "timber", "elephants", "camels", "olive_oil", "wine", "slaves", "glass", "marble", "textiles", "purple_dye", "incense", "silk", "wild_animals", "hides", "tin", "copper", "lead", "amber"]
    
    resourceStringParts = resourceString.split(",")
    if len(resourceStringParts) != 4:
        return False
    else:
        resourceType = resourceStringParts[0].split(" ")[1]
        return resourceType in validResources

descr_strat_file = open(descr_strat_path, "r")

line = descr_strat_file.readline();
while line:
    if line.startswith("resource ") and not isValidResource(line):
        print("Invalid Resource String: " + line)

    line = descr_strat_file.readline()