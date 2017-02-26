import sys, math, urllib, io
from tile_system import LatLongToPixelXY, PixelXYToTileXY, TileXYToQuadKey
from PIL import Image

def getURL(quadkey):
	license_key = "41W7SFbE1T0EL5ZXwqs3~1Qz6gK41TViufkWWMdrxbg~Au2gvdXSyRpNSFsqjlnA5hVuP-2kaFHPdz3pUKMZasjOWt89LqbSAyUCSjx8qsJm"
	return "http://h0.ortho.tiles.virtualearth.net/tiles/h%s.jpeg?g=131&key=%s" % (quadkey, license_key)

def main():
	# This function runs the code for HW3
	lat1 = float(sys.argv[1])
	lon1 = float(sys.argv[2])
	lat2 = float(sys.argv[3])
	lon2 = float(sys.argv[4])
	
	q = 7 #quality of image
	
	# First convert the four corners to pixels
	x11, y11 = LatLongToPixelXY(lat1, lon1, q)
	x22, y22 = LatLongToPixelXY(lat2, lon2, q)
	x12, y12 = LatLongToPixelXY(lat1, lon2, q)
	x21, y21 = LatLongToPixelXY(lat2, lon1, q)
	# Next, convert pixel coordinates to tile coordinates
	tx11, ty11 = PixelXYToTileXY(x11, y11)
	tx22, ty22 = PixelXYToTileXY(x22, y22)
	tx12, ty12 = PixelXYToTileXY(x12, y12)
	tx21, ty21 = PixelXYToTileXY(x21, y21)
	# Now convert tile coordinates to QuadKey
	qk11 = TileXYToQuadKey(tx11, ty11, q)
	qk22 = TileXYToQuadKey(tx22, ty22, q)
	qk12 = TileXYToQuadKey(tx12, ty12, q)
	qk21 = TileXYToQuadKey(tx21, ty21, q)

	# IDK WHAT TO DO FROM HERE, but the quadkeys are supposed to be inserted 
	# between frontURL and backURL

	###### THIS LINE HERE NEEDS TO BE CHANGED
	quadkey = qk11
	######
	
	print quadkey
	frontURL = "http://h0.ortho.tiles.virtualearth.net/tiles/h"
	backURL = ".jpeg?g=131"
	fullURL = frontURL + quadkey + backURL
	#urllib.urlretrieve(fullURL, "aerial_image.jpg")
	socket = urllib.urlopen(getURL(quadkey))
	tinker = socket.read()
	img = Image.open(io.BytesIO(tinker))
	# img.save('test.jpg')
	img.show()

if __name__ == '__main__':
    main()
