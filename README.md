# Satellite-Aerial-Image-Retrieval
##Group Members
Yue Hu (yhn490), Shin Lee (syl097), James Kim (yjk114), Kevin Li (kwl424)

##Prerequsite
Pillow library with Python 2.7 : https://python-pillow.org/

##Algorithm
1. Convert the Bing Tile System. Code is in tile.system.py.
    Reference: https://msdn.microsoft.com/en-us/library/bb259689.aspx#Anchor_0
2. Iteratively paste a higher quality tile to the previous image until the Bing server could not provide better data.
⋅⋅1. The base canvas is created.
⋅⋅2. Choose the highest resoluation with which image have at least one side has only one tile as the starting point.
⋅⋅3. Increase the resoluton, iterate through all the tiles from the Bing Map server, and paste the better one to the correct position in the big canvas.
⋅⋅4. Repeat Step 3 until resolution of some data is null returned by the Server.

##Usage
```python main.py lat1 lon1 lat2 lon2```
Result will be saved as "complete.jpeg" in the same directory.

##Examples
Near Northwestern University:
```python main.py 42.047360 -87.679623 42.048300 -87.679902```
National Mall in DC:
```python main.py 38.891794 -77.050090 38.887919 -77.005973```
Staten Island in New York:
```python main.py 40.638058 -74.254028 40.504013 -74.061080```
Opera House in Australia
```python main.py -33.856098 151.214184 -33.858352 151.215814```
Some other images are also included in the directory.

##Caveat
If the selected bonding box is too tiny, for example, the location is in the same tile even when the resolution is 23 (maximum), but Bing Map Tile System does not have data with 23 resolution for it, then the code does not generate the tile. 

