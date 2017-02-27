import sys, math, urllib, io, operator
from tile_system import *
from PIL import Image

def getURL(quadkey):
	license_key = "41W7SFbE1T0EL5ZXwqs3~1Qz6gK41TViufkWWMdrxbg~Au2gvdXSyRpNSFsqjlnA5hVuP-2kaFHPdz3pUKMZasjOWt89LqbSAyUCSjx8qsJm"
	return "http://h0.ortho.tiles.virtualearth.net/tiles/h%s.jpeg?g=131&key=%s" % (quadkey, license_key)

def getImageFromQuadkey(quadkey):
	socket = urllib.urlopen(getURL(quadkey))
	tinker = socket.read()
	img = Image.open(io.BytesIO(tinker))
	return img

def getLowestQuality(lat1, lon1, lat2, lon2):
	'''
	The quality which at least one side of the large image contains only one tile
	'''
	i = 1

	for i in xrange(23, 0, -1):
		tx1, ty1 = LatLongToTileXY(lat1, lon1, i)
		tx2, ty2 = LatLongToTileXY(lat2, lon2, i)
		if tx1 > tx2:
			tx1, tx2 = tx2, tx1
		if ty1 > ty2:
			ty1, ty2 = ty2, ty1
		if (tx2 - tx1 <= 1) and (ty2 - ty1 <= 1):
			print "Lowest Quality found at ",
			print i
			return i, tx1, ty1
	print "Error: should not reach here"
	
def nullResult(img):
	'''Compare the query result with the null image. If they match, then Bing server does not have data for that location'''
	result = (img == Image.open('null.jpeg'))
	# print result
	return result



def main():
	# This function runs the code for HW3
	lat1 = float(sys.argv[1])
	lon1 = float(sys.argv[2])
	lat2 = float(sys.argv[3])
	lon2 = float(sys.argv[4])
	# Define the base image fixed size. It should take longer as the required image gets larger.
	# 1<<12 is the workable size for us to open the result image efficiently
	BASE_SIZE = 1 << 12 
	MIN_TILE_SIZE = 1 << 6
	base = Image.new('RGB', (BASE_SIZE, BASE_SIZE))

	q, tx0, ty0 = getLowestQuality(lat1, lon1, lat2, lon2)
	curr_tile_size = BASE_SIZE/2
	flag = True 
	# The full image with best resolution is updated after each iteration of double for loop
	best_result = base 
	while q <= 23 and curr_tile_size >= MIN_TILE_SIZE and flag:

		print "Fetch quality at ",
		print q
		print "curr_tile_size is",
		print curr_tile_size
		tx1, ty1 = LatLongToTileXY(lat1, lon1, q)
		tx2, ty2 = LatLongToTileXY(lat2, lon2, q)
		if tx1 > tx2:
			tx1, tx2 = tx2, tx1
		if ty1 > ty2:
			ty1, ty2 = ty2, ty1
		for x in xrange(tx1, tx2+1):
			if not flag:
				break
			for y in xrange(ty1, ty2+1):
				if not flag:
					break
				curr_quadKey = TileXYToQuadKey(x, y, q)
				# print "curr_quadKey is",
				# print curr_quadKey
				try:
					curr_image = getImageFromQuadkey(curr_quadKey)
					# print len(curr_image.histogram())
					# curr_image = curr_image.resize((MIN_TILE_SIZE, MIN_TILE_SIZE))
					# print len(curr_image.histogram())
					# curr_image.show()
					# if q==21:
					# 	curr_image.show()
				
					if not nullResult(curr_image):
						curr_image = curr_image.resize((curr_tile_size, curr_tile_size))
						start_x = (x - tx0) * curr_tile_size 
						start_y = (y - ty0) * curr_tile_size
						end_x = start_x + curr_tile_size
						end_y = start_y + curr_tile_size
						base.paste(curr_image, (start_x, start_y, end_x, end_y))
					else:
						flag = False
						print "can't find tile:",
						print x, 
						print y,
						print "at the quality level",
						print q
						break
				except:
					print "Bing connection problem"
					continue

		tx0 = tx0 * 2
		ty0 = ty0 * 2
		q += 1
		curr_tile_size /= 2
		if flag:
			best_result = base
			# best_result.show()

	print "finish while loop"
	best_result.save('complete.jpeg')
	# base.show()

	

if __name__ == '__main__':
	main()



