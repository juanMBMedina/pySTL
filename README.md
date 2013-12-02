pySTL
=====

Python code for working with .STL (sterolithography) files.  

Often, STL files are exported from modelling software in awkward locations or with strange bounding boxes.  It can be useful to move them around and rotate them without having to open with modelling software again.  This is a simple library that can read, write and do basic manipulations of STL files.  

Currently can be given inputs of ASCII or binary STL and outputs ASCII STL.  ASCII inputs are better tested.


Usage
-----

The basic workflow goes like this:

1. Import a model from a file
2. Manipulate that model
3. Export the model to another or the same file

*Importing a File*

To import a file, create a new pySTL STLmodel object.  The constructor takes one argument, the filename to import.  

```
import pySTL

#Load a model from a file.
model = pySTL.STLmodel('text.stl')
```

*Manipulations*

Manipulate through, translation, scaling, and rotation.  Use 3-D rotation matrices to rotate the model.  

To translate, pass a 3 element NumPy array to the translate method of the model. 
```
import numpy
#Move ten units in the X direction.
movement = numpy.array([10, 0, 0])
model.translate(movement)
```

To scale, pass the scale value to the scale method. 

```
#Scale down to 10% size
scale = 0.1
model.scale(scale)
```

To rotate, create a [3-D rotation matrix](http://en.wikipedia.org/wiki/Rotation_matrix#Basic_rotations) as a 3*3 numpy array and pass to the model's rotate method.  There are three convenience methods to allow for easy calculation of rotations about the X,Y, and Z axes (give angles in radians).  You can combine these to develop any rotation matrix necessary (e.g. from [Euler Angles](http://en.wikipedia.org/wiki/Euler_angles#Proper_Euler_angles)). 

```
#Rotate the model
R1 = pySTL.rotationAboutX(-3.14149/2)
R2 = pySTL.rotationAboutY(-3.14159/4)

R = R1.dot(R2)

model.rotate(R)
```

You can also get the centroid and volume of the model.  

```
c = model.get_centroid()
v = model.get_volume()
```

And finally, export the model back to a new (or the same) .STL file. 
```
model.write_text_stl('newText.stl')
```

