import sys, math, urllib, io
from tile_system import *
from PIL import Image

def getURL(quadkey):
	license_key = "41W7SFbE1T0EL5ZXwqs3~1Qz6gK41TViufkWWMdrxbg~Au2gvdXSyRpNSFsqjlnA5hVuP-2kaFHPdz3pUKMZasjOWt89LqbSAyUCSjx8qsJm"
	return "http://h0.ortho.tiles.virtualearth.net/tiles/h%s.jpeg?g=131&key=%s" % (quadkey, license_key)

def getImageFromQuadkey(quadkey):
	socket = urllib.urlopen(getURL(quadkey))
	tinker = socket.read()
	img = Image.open(io.BytesIO(tinker))
	# img.save('test.jpg')
	# img.show()
	return img

def getLowestQuality(lat1, lon1, lat2, lon2):
	'''
	The quality which at least one side of the large image contains only one tile
	'''
	i = 1

	while i <= 23:
		tx1, ty1 = LatLongToTileXY(lat1, lon1, i)
		tx2, ty2 = LatLongToTileXY(lat2, lon2, i)
		if tx1 > tx2:
			tx1, tx2 = tx2, tx1
		if ty1 > ty2:
			ty1, ty2 = ty2, ty1
		if (tx2 - tx1 > 1) or (ty2 - ty1 > 1):
			print "Lowest Quality found at ",
			print i-1
			return i-1, tx1/2, ty1/2
		# tx0 = tx1
		# ty0 = ty1
		i += 1
	return 23, 0, 0
		

def main():
	# This function runs the code for HW3
	lat1 = float(sys.argv[1])
	lon1 = float(sys.argv[2])
	lat2 = float(sys.argv[3])
	lon2 = float(sys.argv[4])
	LARGE_SIZE = 1 << 10
	base = Image.new('RGB', (LARGE_SIZE, LARGE_SIZE))

	q, tx0, ty0 = getLowestQuality(lat1, lon1, lat2, lon2)
	curr_tile_size = LARGE_SIZE/2

	cantfind = Image.open("cantfind.bmp")

	while q <= 23:
		tx1, ty1 = LatLongToTileXY(lat1, lon1, q)
		tx2, ty2 = LatLongToTileXY(lat2, lon2, q)
		if tx1 > tx2:
			tx1, tx2 = tx2, tx1
		if ty1 > ty2:
			ty1, ty2 = ty2, ty1
		for x in xrange(tx1, tx2+1):
			for y in xrange(ty1, ty2+1):
				curr_quadKey = TileXYToQuadKey(x, y, q)
				try:
					curr_image = getImageFromQuadkey(curr_quadKey)
					# curr_image.show()
				except:
					print "Bing connection problem"
					continue
				if curr_image != cantfind:
					curr_image = curr_image.resize((curr_tile_size, curr_tile_size))
					# find coordinates in the large image
					start_x = (x - tx0) * curr_tile_size 
					start_y = (y - ty0) * curr_tile_size
					end_x = start_x + curr_tile_size
					end_y = start_y + curr_tile_size
					base.paste(curr_image, (start_x, start_y, end_x, end_y))
				else:
					print "can't find tile:",
					print x, 
					print y,
					print "at the quality level",
					print q

		tx0 = tx0 * 2
		ty0 = ty0 * 2
		q += 1
		curr_tile_size /= 2
	print "finish while loop"
	curr_image.save('complete.bmp')
	curr_image.show()

	

if __name__ == '__main__':
	main()

# python main.py 42.047360 -87.679623 42.047361 -87.679624



