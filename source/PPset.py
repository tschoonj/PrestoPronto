global spectra # list that contain the spectra
global x       # x to use for saving and plotting
global xlabel  # xlabel to use for saving and plotting
global filesel_spectra # list in wich the file selected and not averaged are stored

class listum(list):
    def __init__(self, *args, **kws):
        super(listum, self).__init__(*args,**kws)
        self.call_pe={'e0':None, 'step':None, 'nnorm':3, 'nvict':0, 'pre1':None, 
                   'pre2':-50, 'norm1':100, 'norm2':None, 'make_flat':True}
        self.call_abk={'rbkg':1, 'nknots':None, 'e0':None,
             'edge_step':None, 'kmin':0, 'kmax':None, 'kweight':1, 'dk':0,
               'win':'hanning', 'k_std':None, 'chi_std':None, 'nfft':2048, 
               'kstep':0.05,'pre_edge_kws':None, 'nclamp':4, 'clamp_lo':1,
                                 'clamp_hi':1, 'calc_uncertainties':False}
        self.call_xftf=dict()

 

        



spectra=listum()
x=list()
filesel_spectra=list()
xlabel=str()

parameter=dict()