from Rankine import rankine

def main():
    '''
    A test program for rankine power cycles.
    R1 is a rankine cycle object that instantiated for turbvine inlet of saturated vapor.
    R2 is a rankine cytcle object that is instantiated for turbine ineltof superheated vapor.
    :return:
    '''
    R1=rankine(p_high=8000, p_low=8)
    R1.calc_efficiency()
    R1.print_summary()

    R2=rankine(p_high=8000, p_low=8, t_high=500)
    R2.calc_efficiency()
    R2.print_summary()

main()