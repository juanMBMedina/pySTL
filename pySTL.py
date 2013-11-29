import struct
from numpy import array
import numpy as np

#class for a 3d point
class point:

    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
    
    @classmethod
    def fromTuple(self,p):
        return point(p[0], p[1], p[2])
      

#class for a 3d face on a model
class triangle:
    
    def __init__(self,p1,p2,p3,n=None):
        #3 points of the triangle
        self.vertices=array(p1),array(p2),array(p3)
      
        #triangles normal
        if n != None:
            self.normal= n
        else:
            self.normal = array(self.calculate_normal(self.vertices[0],self.vertices[1],self.vertices[2]))
  
    def calculate_normal(self,p1,p2,p3):
        p12 = p2-p1
        p23 = p3-p2
        #calculate the cross product
        return np.cross(p12,p23)    
  

class STLmodel:


    def __init__(self,filename):
        self.filename = filename
        self.triangles=[]
        self.centroid = None
        self.volume = None
        self.load_stl()
      
    #return the faces of the triangles
    def get_triangles(self):
        if self.triangles:
            for face in self.triangles:
                yield face

    def get_centroid(self):
        if  self.centroid == None:
            self.calculateCentroid()
        return self.centroid

    def get_volume(self):
        if self.volume == None:
            self.calculateCentroid()
        return self.volume
            

    def calculateCentroid(self):
        totalVolume=0
        currentVolume=0
        xCenter = 0
        yCenter = 0
        zCenter = 0
        #Each triangle forms a tetrahedron with the origin.  
        #Calculate the size inside the volume of the model. Then add the 
        #contributions to the centroid of the 3-d shape based on those volumes.
        for tri in self.triangles:
            p1 = tri.vertices[0]
            p2 = tri.vertices[1]
            p3 = tri.vertices[2]
            currentVolume = ((p1[0]*p2[1]*p3[2] - p1[0]*p3[1]*p2[2] - p2[0]*p1[1]*p3[2] +
                    p2[0]*p3[1]*p1[2] + p3[0]*p1[1]*p2[2] - p3[0]*p2[1]*p1[2])/6)
            totalVolume += currentVolume
            xCenter += ((p1[0] + p2[0] + p3[0])/4) * currentVolume
            yCenter += ((p1[1] + p2[1] + p3[1])/4) * currentVolume
            zCenter += ((p1[2] + p2[2] + p3[2])/4) * currentVolume
        
        self.volume = totalVolume
        xCentroid = xCenter/totalVolume
        yCentroid = yCenter/totalVolume
        zCentroid = zCenter/totalVolume
        self.centroid = array([xCentroid,yCentroid,zCentroid])



    #load stl file detects if the file is a text file or binary file
    def load_stl(self):
        #read start of file to determine if its a binay stl file or a ascii stl file
        if self.filename:
            fp=open(self.filename,'rb')
            h=fp.read(80)
            type=h[0:5]
            fp.close()

            if type=='solid':
                print "reading text file "+str(self.filename)
                self.load_text_stl()
            else:
                print "reading binary stl file "+str(self.filename,)
                self.load_binary_stl()
  
    #read text stl match keywords to grab the points to build the model
    def load_text_stl(self):
        fp=open(self.filename,'r')
        #import pdb
        #pdb.set_trace()
        for line in fp:
            words=line.split()
            if len(words)>0:
                if words[0]=='solid':
                    try:
                        self.name=words[1]
                    except IndexError:
                        self.name="polyhedron"

                if words[0]=='facet':
                    center=[0.0,0.0,0.0]
                    vertices=[]
                    normal=(float(words[2]),float(words[3]),float(words[4]))
                  
                if words[0]=='vertex':
                    vertices.append((float(words[1]),float(words[2]),float(words[3])))
                  
                  
                if words[0]=='endloop':
                    #make sure we got the correct number of values before storing
                    if len(vertices)==3:
                        self.triangles.append(triangle(vertices[0],vertices[1],vertices[2],normal))
        fp.close()
        print "Loaded STL. " + self.name

    #load binary stl file check wikipedia for the binary layout of the file
    #we use the struct library to read in and convert binary data into a format we can use
    def load_binary_stl(self):
        fp=open(self.filename,'rb')
        h=fp.read(80)

        l=struct.unpack('I',fp.read(4))[0]
        count=0
        while True:
            try:
                p=fp.read(12)
                if len(p)==12:
                    n=struct.unpack('f',p[0:4])[0],struct.unpack('f',p[4:8])[0],struct.unpack('f',p[8:12])[0]
                  
                p=fp.read(12)
                if len(p)==12:
                    p1=struct.unpack('f',p[0:4])[0],struct.unpack('f',p[4:8])[0],struct.unpack('f',p[8:12])[0]

                p=fp.read(12)
                if len(p)==12:
                    p2=struct.unpack('f',p[0:4])[0],struct.unpack('f',p[4:8])[0],struct.unpack('f',p[8:12])[0]

                p=fp.read(12)
                if len(p)==12:
                    p3=struct.unpack('f',p[0:4])[0],struct.unpack('f',p[4:8])[0],struct.unpack('f',p[8:12])[0]

                new_tri=(n,p1,p2,p3)

                if len(new_tri)==4:
                    tri=triangle(p1,p2,p3,n)
                    self.triangles.append(tri)
                count+=1
                fp.read(2)

                if len(p)==0:
                    break
            except EOFError:
                break
        fp.close()
    
    def write_text_stl(self, filename):
        print "WRITE"

        try:
            f = open(filename, 'wb')
            f.write('solid {:s}\n'.format(self.name))
            for facet in self.triangles:
                normal = facet.normal
                f.write('  facet normal {0:.6E} {1:.6E} {2:.6E}\n'.format(normal[0], normal[1], normal[2]))
                f.write('    outer loop\n')
                for point in facet.vertices:
                    f.write('      vertex {0:.6E} {1:.6E} {2:.6E}\n'.format(point[0], point[1], point[2]))
                f.write('    endloop\n')
                f.write('  endfacet\n')
            f.write('endsolid {:s}\n'.format(self.name))
            f.close()
        except IOError:
            print "Couldn't write..."



    #Pass this a numpy 3-array to translate all the points in the .stl file. 
    def translate(self, p):
        for tri in self.triangles:
            for point in tri.vertices:
                point[0] += p[0]
                point[1] += p[1]
                point[2] += p[2]
        self.volume = None
        self.centroid = None

    #Pass this a numpy 2D array, not a numpy matrix a rotation object.
    def rotate(self, R):
        for tri in self.triangles:
            for point in tri.vertices:
                point = R*point
        self.centroid = None
        self.volume = None


