f = open(r"descr_map_tiles_generated.txt", "w")

numberOfTiles = input("How many tiles? : ");

for x in range(1, int(numberOfTiles)+1):
	xAsString = str(x).zfill(3)
	f.write("file data/terrain/campaign/imperial_campaign/pieces/" + xAsString + "_lod0.cas\n")
	f.write("base_albedo data/terrain/campaign/imperial_campaign/albedos/" + xAsString + "_albedo.tga.tga\n")
	f.write("base_material data/terrain/campaign/imperial_campaign/materials/" + xAsString + "_material.tga.tga\n")
	f.write("winter_base_albedo data/terrain/campaign/imperial_campaign/albedos_winter/" + xAsString + "_albedo.tga.tga\n")
	f.write("heightmap data/terrain/campaign/imperial_campaign/heightmap/" + xAsString + "_lod0.bin\n")
	f.write("\n")

f.close