import numpy as np
from scipy.interpolate import griddata

class steam():
    def __init__(self, pressure, T=None, x=None, v=None, h=None, s=None, name=None):
        '''
        constructor for steam
        :param pressure: pressure in kPa
        :param T: Temperature in degrees C
        :param x: quality of steam x=1 is saturated vapor, x=0 is saturated liquid
        :param v: specific volume in m^3/kg
        :param h: specific enthalpy in kJ/kg
        :param s: specific entropy in kJ/(kg*K)
        :param name: a convenient identifier
        '''
        #assign arguments to class properties
        self.p = pressure
        self.T = T
        self.x = x
        self.v = v
        self.h = h
        self.s = s
        self.name = name
        self.region = None #'superheated' or 'saturated' or 'two-phase'
        if T==None and x==None and v==None and h==None and s==None: return
        else: self.calc()

    def calc(self):
        '''
        The Rankine cycle operates between two isobars (i.e., p_high (Turbine inlet state 1) & p_low (Turbine exit state 2)
        So, given a pressure, we need to determine if the other given property puts
        us in the saturated or superheated region.
        :return: nothing returned, just set the properties
        '''
        #1. need to determine which second property is known
        #2. determine if two-phase/saturated or superheated
        #3. find all unknown thermodynamic properties by interpolation from appropriate steam table

        #read in the thermodynamic data from files
        ts, ps, hfs, hgs, sfs, sgs, vfs, vgs= np.loadtxt('sat_water_table.txt', skiprows=1, unpack=True)
        tcol, hcol, scol, pcol = np.loadtxt('superheated_water_table.txt', skiprows=1, unpack=True)

        R=8.314/(18/1000) #ideal gas constant for water [J/(mol K)]/[kg/mol]
        Pbar=self.p/100 #pressure in bar - 1bar=100kPa roughly

        #get saturated properties at Pbar from table using griddata
        Tsat = float(griddata((ps), ts, (Pbar)))
        hf= float(griddata((ps), hfs, (Pbar)))
        hg= float(griddata((ps), hgs, (Pbar)))
        sf= float(griddata((ps), sfs, (Pbar)))
        sg= float(griddata((ps), sgs, (Pbar)))
        vf= float(griddata((ps), vfs, (Pbar)))
        vg= float(griddata((ps), vgs, (Pbar)))

        self.hf=hf #this creates a member variable for the class that can be accessed from an object

        if self.T!=None: #use T&Pbar for interpolation with griddata
            if self.T>Tsat:
                self.region='Superheated'
                self.h = float(griddata((tcol, pcol), hcol, (self.T, self.p)))
                self.s = float(griddata((tcol, pcol), scol, (self.T, self.p)))
                self.x=1.0
                TK = self.T + 273.14  # temperature conversion to Kelvin
                self.v = R*TK/(self.p*1000)
        elif self.x!=None: #given a quality means saturated properties.  Interpolate manually.
            self.region='Saturated'
            self.T=Tsat
            self.h=hf+self.x*(hg-hf)
            self.s=sf+self.x*(sg-sf)
            self.v=vf+self.x*(vg-vf)
        elif self.h!=None:
            self.x=(self.h-hf)/(hg-hf) #calculate quality given Pbar and h
            if self.x<=1.0: #manual interpolation
                self.region='Saturated'
                self.T=Tsat
                self.s=sf+self.x*(sg-sf)
                self.v=vf+self.x*(vg-vf)
            else: #interpolate with griddata
                self.region='Superheated'
                self.T = float(griddata((hcol, pcol), tcol, (self.h, self.p)))
                self.s = float(griddata((hcol, pcol), scol, (self.h, self.p)))
        elif self.s!=None:
            self.x=(self.s-sf)/(sg-sf)
            if self.x<=1.0: #manual interpolation
                self.region='Saturated'
                self.T=Tsat
                self.h=hf+self.x*(hg-hf)
                self.v=vf+self.x*(vg-vf)
            else: #interpolate with griddata
                self.region = 'Superheated'
                self.T = float(griddata((scol, pcol), tcol, (self.s, self.p)))
                self.h = float(griddata((scol, pcol), scol, (self.s, self.p)))

    def print(self):
        print('Name: ', self.name)
        if self.x<0.0: print('Region: compressed liquid')
        else: print('Region: ', self.region)
        print('p = {:0.2f} kPa'.format(self.p))
        if self.x >= 0.0: print('T = {:0.1f} degrees C'.format(self.T))
        print('h = {:0.2f} kJ/kg'.format(self.h))
        if self.x >= 0.0:
            print('s = {:0.4f} kJ/(kg K)'.format(self.s))
            if self.region == 'Saturated': print('v = {:0.6f} m^3/kg'.format(self.v))
            if self.region == 'Saturated': print('x = {:0.4f}'.format(self.x))
        print()

def main():
    inlet=steam(7350,name='Turbine Inlet') #not enough information to calculate
    inlet.x=0.9 #90 percent quality
    inlet.calc()
    inlet.print()

    h1=inlet.h
    s1=inlet.s
    print(h1,s1,'\n')

    outlet=steam(100, s=inlet.s, name='Turbine Exit')
    outlet.print()

    another=steam(8575, h=2050, name='State 3')
    another.print()

    yetanother = steam(8575, h=3125, name='State 4')
    yetanother.print()

#the following if statement causes main() to run
#only if this file is being run in isolation, not if it is
#being imported into another Python program as a module.
#This allows us to test the class, but not run main if it is imported
#into another program.
if __name__=="__main__":
    main()
