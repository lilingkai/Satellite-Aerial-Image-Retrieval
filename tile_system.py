import math

EarthRadius = 6378137
MinLat = -85.05112878
MaxLat = 85.05112878
MinLong = -180
MaxLong = 180

def Clip(n, minVal, maxVal):
	"""
	Summary:
		Clip will clip a number to the specified min and max values.

	Input Params:
		n - the number to clip
		minVal - minimum allowable value
		maxVal - maximum allowable value

	Returns:
		the clipped value
	"""		
	return min(max(n, minVal), maxVal)

def MapSize(levelOfDetail):
	"""
	Summary:
		Determines the map width and height (in pixels) at a specified level of detail.

	Input Params:
		levelOfDetail - level of detail from 1 (lowest detail) to 23 (highest detail)

	Returns:
		The map width and height in pixels
	"""
	return 256 << levelOfDetail

def GroundResolution(latitude, levelOfDetail):
	"""
	Summary:
		Determines the ground resolution (in meters per pixel) at a specified latitude and level of detail.
	
	Input Params:
		latitude - latitude (in degrees) at which to measure the map scale
		levelOfDetail - level of detail from 1 (lowest detail) to 23 (highest detail)

	Returns:
		The ground resolution, in meters per pixel
	"""
	latitude = Clip(latitude, MinLat, MaxLat)
	return math.cos(latitude*math.pi / 180) * 2 * math.pi * EarthRadius / MapSize(levelOfDetail)

def MapScale(latitude, levelOfDetail, screenDpi):
	"""
	Summary:
		Determines the map scale at a specified latitude, level of detail, and screen resolution.

	Input Params:
		latitude - latitude (in degrees) at which to measure the map scale
		levelOfDetail - level of detail from 1 (lowest detail) to 23 (highest detail)
		screenDpi - Resolution of the screen, in dots per inch

	Returns:
		The map scale, expressed as the denominator N of the ratio 1 : N
	"""
	return GroundResolution(latitude, levelOfDetail) * screenDpi/0.0254 

def LatLongToPixelXY(latitude, longitude, levelOfDetail):
	"""
	Summary:
		Converts a point from latitude/longitutde WGS-84 coordinates (in degrees)
		into pixel XY coordinates at a specified level of detail.

	Input Params:
		latitude - latitude of the point, in degrees.
		longitude - longitutde of the point, in degrees.
		levelOfDetail - level of detail from 1 (lowest detail) to 23 (highest detail)

	Returns:
		pixelX, pixelY - X and Y coordinate in pixels

	"""
	latitude = Clip(latitude, MinLat, MaxLat)
	longitude = Clip(longitude, MinLong, MaxLong)

	x = (longitude + 180) / 360
	sinLatitude = math.sin(latitude * math.pi / 180)
	y = 0.5 - math.log((1 + sinLatitude) / (1 - sinLatitude)) / (4 * math.pi)

	mapSize = MapSize(levelOfDetail)
	pixelX = int(Clip(x * mapSize + 0.5, 0, mapSize - 1))
	pixelY = int(Clip(y * mapSize + 0.5, 0, mapSize - 1))

	return pixelX, pixelY

def PixelXYToLatLong(pixelX, pixelY, levelOfDetail):
	"""
	Summary:
		Converts a pixel from pixel XY coordinates at a specified level of detail
		into latitude/longitude WGS-84 coordinates (in degrees).
	
	Input Params:
		pixelX - X coordinate of the point, in pixels
		pixelY - Y coordinate of the point, in pixels
		levelOfDetail - Level of detail, from 1 (lowest detail) to 23 (highest detail)

	Returns:
		latitude, longitude - latitude and longitude in degrees
	"""
	mapSize = MapSize(levelOfDetail)
	x = (Clip(pixelX, 0, mapSize-1) / mapSize) - 0.5
	y = 0.5 - (Clip(pixelY, 0, mapSize - 1) / mapSize)

	latitude = 90 - 360 * math.atan(math.exp(-y * 2 * math.pi)) / math.pi
	longitude = 360 * x

	return latitude, longitude

def PixelXYToTileXY(pixelX, pixelY):
	"""
	Summary:
		Converts pixel XY coordinates into tile XY coordinates of the tile containing the specified pixel.

	Input Params:
		pixelX - X coordinate of the point, in pixels
		pixelY - Y coordinate of the point, in pixels
	
	Returns: 
		tileX, tileY
	"""
	tileX = int(pixelX / 256)
	tileY = int(pixelY / 256)
	return tileX, tileY

def TileXYToPixelXY(tileX, tileY):
	"""
	Summary:
		Converts tile XY coordinates into pixel XY coordinates of the upper-left pixel 
		of the specified tile.

	Input Params:
		tileX - Tile X coordinate
		tileY - Tile Y coordinate
	
	Returns: 
		pixelX, pixelY
	"""
	pixelX = tileX * 256
	pixelY = tileY * 256

def TileXYToQuadKey(tileX, tileY, levelOfDetail):
	"""
	Summary:
		Converts tile XY coordinates into a QuadKey at a specified level of detail.

	Input Params:
		tileX - Tile X coordinate
		tileY - Tile Y coordinate
		levelOfDetail - Level of detail, from 1 (lowest detail) to 23 (highest detail)

	Returns:
		quadKey - A string containing the QuadKey
	"""
	quadKey = ""
	for i in range(levelOfDetail, 0, -1):
		digit = '0'
		mask = 1 << (i-1)
		if ((tileX & mask) != 0):
			digit = chr(ord(digit) + 1)
		if ((tileY & mask) != 0):           # "and" is for booleans, "&" is for bits
			digit = chr(ord(digit) + 1)
			digit = chr(ord(digit) + 1)
		quadKey += digit
	return quadKey

def LatLongToQuadKey(latitude, longitude, levelOfDetail):
	pixelX, pixelY = LatLongToPixelXY(latitude, longitude, levelOfDetail)
	print "pixelX, pixelY are ",
	print pixelX,
	print pixelY
	tileX, tileY = PixelXYToTileXY(pixelX, pixelY)
	print "tileX, tileY are ",
	print tileX,
	print tileY
	quadKey = TileXYToQuadKey(tileX, tileY, levelOfDetail)
	print "quadKey is",
	print quadKey
	return quadKey

def LatLongToTileXY(latitude, longitude, levelOfDetail):
	pixelX, pixelY = LatLongToPixelXY(latitude, longitude, levelOfDetail)
	tileX, tileY = PixelXYToTileXY(pixelX, pixelY)
	return tileX, tileY

# def QuadKeyToTileXY(quadKey):
# 	#
# 	Summary: 
# 		Converts a QuadKey into tile XY coordinates.

# 	Input Params:
# 		quadKey - QuadKey of the Tile

# 	Returns: 
# 		tileX, tileY, levelOfDetail
# 	#
# 	tileX = tileY = 0;
# 	levelOfDetail = len(quadKey)
# 	for i in range (levelOfDetail, 0, -1):
# 		mask = 1 << (i-1);
# 		if quadKey[levelOfDetail - i] == '0':
# 			break
# 		elif quadKey[levelOfDetail - i] == '1':
# 			tileX
# 			break
# 		elif quadKey[levelOfDetail -i] == '2':
# 			tileY
# 			break
# 		elif qudKey[levelOfdetail - i] == '3':
# 			tileX
# 			tileY
# 			break
# 		else:
# 			raise ValueError("Invalid QuadKey digit sequence.")
if __name__ == '__main__':
    LatLongToQuadKey(42.052799, -87.673748, 2) # Northwestern QuadKey

