from Steam import steam

class rankine():
    def __init__(self, p_low, p_high, t_high=None, name='Rankine Cycle', x=1.0):
        '''
        Constructor for the Rankine power cycle
        :param p_low: low pressure isobar (kPa) states 4&1
        :param p_high: high pressure isobar (kPa) states 2&3
        :param t_high: the highest temperature in the cycle (degrees C) state 1
        :param name: a convenient name
        '''
        #set the class property values
        self.p_low=p_low
        self.p_high=p_high
        self.t_high=t_high
        self.name=name
        #define more class properties
        self.efficiency=None
        self.turbine_work=0
        self.pump_work=0
        self.heat_added=0
        self.x=x
        self.state1=None #a steam object at t_high, p_high
        self.state2=None #a steam object at p_low, s_2 (s_2s)
        self.state3=None #a steam object at p_low, sat liq.
        self.state4=None #a steam object at p_high

    def calc_efficiency(self):
        # calculate the 4 states
        # state 1: turbine inlet (p_high, t_high) superheated or saturated vapor
        if(self.t_high==None):
            self.state1 = steam(self.p_high, x=self.x, name='Turbine Inlet')
        else:  # probably superheated
            self.state1= steam(self.p_high, T=self.t_high, name='Turbine Inlet')
        # state 2: turbine exit (p_low, s=s_turbine inlet) two-phase
        self.state2= steam(self.p_low, s=self.state1.s, name='Turbine Exit')
        # state 3: pump inlet (p_low, x=0) saturated liquid
        self.state3= steam(self.p_low, x=0, name='Pump Exit')
        # state 4: pump exit (p_high,s=s_pump_inlet) typically sub-cooled, but estimate as saturated liquid
        self.state4=steam(self.p_high, s=self.state3.s, name='Pump Exit')
        # assume incompressible fluid, but h increases because of increase in p while v remains constant
        self.state4.h=self.state3.h+self.state3.v*(self.p_high-self.p_low)

        self.turbine_work = self.state1.h - self.state2.h
        self.pump_work = self.state4.h - self.state3.h
        self.heat_added = self.state1.h - self.state4.h
        self.efficiency = 100 * (self.turbine_work - self.pump_work) / self.heat_added
        return self.efficiency

    def print_summary(self):

        if self.efficiency==None:
            self.calc_efficiency()
        print('Cycle Summary for: ', self.name)
        print('\tEfficiency: {:0.3f}%'.format(self.efficiency))
        print('\tTurbine Work: {:0.3f} kJ/kg'.format(self.turbine_work))
        print('\tPump Work: {:0.3f} kJ/kg'.format(self.pump_work))
        print('\tHeat Added: {:0.3f} kJ/kg'.format(self.heat_added))
        self.state1.print()
        self.state2.print()
        self.state3.print()
        self.state4.print()

def main():
    rankine1=rankine(8,8000,t_high=500,name='Rankine Cycle - Superheated at turbine inlet')
    #t_high is specified
    #if t_high were not specified, then x_high = 1 is assumed
    eff=rankine1.calc_efficiency()
    print(eff)
    rankine1.state3.print()
    rankine1.print_summary()
    #hf=rankine1.state1.hf
    #hg=rankine1.state1.hg
    rankine2=rankine(8,8000, name='Rankine Cycle - Saturated at turbine inlet')
    eff2=rankine2.calc_efficiency()
    print(eff2)

    rankine2.print_summary()

if __name__=="__main__":
    main()