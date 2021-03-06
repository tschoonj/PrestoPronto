# -*- coding: utf-8 -*-
# Copyright 2009 ESRF
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL ILLINOIS INSTITUTE OF TECHNOLOGY BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Except as contained in this notice, the name of ESRF
# shall not be used in advertising or otherwise to promote
# the sale, use or other dealings in this Software without prior written
# authorization from ESRF.

from   Tkinter import *   
import ttk
import numpy
import utility as ut
import bm29_tools as bt


import PPset



      
global __verbose__                                                                    
__verbose__=False#True#
global num_deriv
num_deriv=True




from matplotlib.backends.backend_tkagg import  cursors
###########################################################################################clas####
class EXAFSparam(object):
    def __init__(self, genitore):
        self.genitore=genitore
       #--------------------------   Declare--------------------------------------------------
        self._Eop    = StringVar()
        self._skmin  = StringVar()
        self._skmax  = StringVar()
        self._rbkg   = StringVar()
        self.kweigth = IntVar()
        self.kweigthp= IntVar()
        
        self.parN= ["e0" , "kmin", "kmax", "rbkg", "kweight"]

       #--------------------------   Define--------------------------------------------------
        self.num=0
        
        if PPset.spectra.call_abk["e0"]: self._Eop.set(PPset.spectra.call_abk["e0"]) 
        else:      self._Eop.set("default")   
        
        if PPset.spectra.call_abk["kmin"]: self._skmin.set(PPset.spectra.call_abk["kmin"])
        else:      self._skmin.set(0)
        
        if PPset.spectra.call_abk["kmax"]: self._skmax.set(PPset.spectra.call_abk["kmax"]) 
        else:      self._skmax.set("default") 
        
        if PPset.spectra.call_abk["rbkg"]: self._rbkg.set(PPset.spectra.call_abk["rbkg"]) 
        else:      self._rbkg.set(1)         
              
        if PPset.spectra.call_abk["kweight"]: self.kweigth.set(PPset.spectra.call_abk["kweight"])
        else:      self.kweigth.set(1) 
        
        self.kweigthp.set(1)
       #------------------------------------------------------
        self.param_win = Frame(genitore)
        self.param_win.pack(side=LEFT)
        
        self.quadro_Eop = LabelFrame(self.param_win, text = "Eo")
        self.quadro_Eop.pack(side = TOP,  fill = X)
        self._entry_Eop= Entry(self.quadro_Eop, width = 10, textvariable=self._Eop)
        self._entry_Eop.pack(side = LEFT, padx = 5, ipady = 3, fill = X)

        self.quadro_skmin = LabelFrame(self.param_win, text = "skmin")
        self.quadro_skmin.pack(side = TOP,  fill = X)
        self._entry_skmin= Entry(self.quadro_skmin, width = 10, textvariable=self._skmin)
        self._entry_skmin.pack(side = LEFT, padx = 5, ipady = 3, fill = X)

        self.quadro_skmax = LabelFrame(self.param_win, text = "skmax")
        self.quadro_skmax.pack(side = TOP,  fill = X)
        self._entry_skmax= Entry(self.quadro_skmax, width = 10, textvariable=self._skmax)
        self._entry_skmax.pack(side = LEFT, padx = 5, ipady = 3, fill = X)
        
        self.quadro_rbkg = LabelFrame(self.param_win, text = "rbkg")
        self.quadro_rbkg.pack(side = TOP,  fill = X)
        self._entry_rbkg= Entry(self.quadro_rbkg, width = 10, textvariable=self._rbkg)
        self._entry_rbkg.pack(side = LEFT, padx = 5, ipady = 3, fill = X)
        
        self.quadro_spin_kweigth = LabelFrame(self.param_win, text = "k_wgt  k_plot")
        self.quadro_spin_kweigth.pack(side = TOP,  fill = X, ipady=2, anchor = W, padx=2)
        self.spin_kweigth = Spinbox(self.quadro_spin_kweigth, from_ = 0, to = 3, textvariable= self.kweigth, width = 2)
        self.spin_kweigth.pack(side = LEFT ,anchor = W, padx = 5, ipadx = 1, ipady = 3) #, expand = YES,  fill = BOTH

        self.spin_kweigthp = Spinbox(self.quadro_spin_kweigth, from_ = 0, to = 3, textvariable= self.kweigthp, width = 2)
        self.spin_kweigthp.pack(side = LEFT ,anchor = W, padx = 8, ipadx = 2, ipady = 3) #, expand = YES,  fill = BOTH
        self.rerefresh = Button(self.param_win,
                                     command = self.refresh,#lambda x= self.num: self.refresh(x),
                                      text = "refresh",
                                      background = "violet",
                                      width = 8,
                                      padx = "3m",
                                      pady = "2m")
        self.rerefresh.pack(side = TOP, anchor = W, padx = 5, pady = 3)

        self.resave = Button(self.param_win,
                                      command = self.saveparam,
                                      text = "Save param",
                                      background = "green",
                                      width = 8,
                                      padx = "3m",
                                      pady = "2m")
        self.resave.pack(side = TOP, anchor = W, padx = 5, pady = 3)
        
       #--------------------------   Graphic win  --------------------------------------------------
        self.graphframeM = Frame(genitore)        
        self.graphframeM.pack(side = LEFT, fill=BOTH, expand=YES)
        self.graphframeE = Frame(genitore)        
        self.graphframeE.pack(side = LEFT, fill=BOTH, expand=YES)
        self.graphframeF = Frame(genitore)        
        self.graphframeF.pack(side = LEFT, fill=BOTH, expand=YES)
        self.grap_winM=ut.ParamGraph(self.graphframeM, PPset.spectra,
                                     "energy", ["mu", "bkg"], 
                                     xlabel= '$energy (eV)$',
                                     ylabel= '$mu (abs. unit)$' )
        self.grap_winE=ut.ParamGraph(self.graphframeE, PPset.spectra, 
                                     "k", ["chiw"], 
                                     xlabel= '$k(\AA^{-1})$',
                                     ylabel= 'kchi(k)' )
        self.grap_winF=ut.ParamGraph(self.graphframeF, PPset.spectra, 
                                     "r", ["chir_mag"], 
                                     xlabel= '$R(\AA)$',
                                     ylabel= 'FT' )
        if (len(PPset.spectra)>1):
            self.grap_winF.slider.pack_forget()
            self.grap_winE.slider.pack_forget()
            self.grap_winM.slider.pack_forget()
            self.slider = Scale(genitore, from_= 0, to=len(PPset.spectra)-1,
                                         command =self.panor2, 
                                         orient=VERTICAL,
                                         label= "Spectra"
                                         )
            self.slider.pack(side = LEFT,fill = Y, anchor = N,pady = 5, ipady = 0)
        self.grap_winE.pick=self.grap_winE.canvas.mpl_connect('pick_event', self.onpick)                     # new pick release link
        self.grap_winE.release=self.grap_winE.canvas.mpl_connect('button_release_event', self.onrelease)
        self.grap_winE.canvas.mpl_connect('figure_leave_event', self.onout)
        self.grap_winF.pick=self.grap_winF.canvas.mpl_connect('pick_event', self.onpick)                     # new pick release link
        self.grap_winF.release=self.grap_winF.canvas.mpl_connect('button_release_event', self.onrelease)
        self.grap_winF.canvas.mpl_connect('figure_leave_event', self.onout) 
        self.grap_winM.pick=self.grap_winM.canvas.mpl_connect('pick_event', self.onpick)                     # new pick release link
        self.grap_winM.release=self.grap_winM.canvas.mpl_connect('button_release_event', self.onrelease)
        self.grap_winM.canvas.mpl_connect('figure_leave_event', self.onout) 
        self.out=False
        self.press=False        
        #self.preposted()  
        #self.onrelease("pippo")
        #self.refresh()
        self.refresh()

        # new pick release link

        genitore.wait_window()            
        
   #--------------------------  mouse Function  ----------------------------------------------------- 
    def onout(self,event_p):
        pass
        #self.out=True
        
    def onpick(self,event_p):
        if event_p.artist in self.grap_winE.parmlines: 
            self.out=False
            self.grap_winE.param_num= self.grap_winE.parmlines.index(event_p.artist)            
            self.grap_winE.mov_link=self.grap_winE.canvas.mpl_connect(
                                           'motion_notify_event', self.onmovingE)
        if event_p.artist in self.grap_winF.parmlines: 
            self.out=False
            self.grap_winF.param_num= self.grap_winF.parmlines.index(event_p.artist)            
            self.grap_winF.mov_link=self.grap_winF.canvas.mpl_connect(
                                           'motion_notify_event', self.onmovingF) 
        if event_p.artist in self.grap_winM.parmlines: 
            self.out=False
            self.grap_winM.param_num= self.grap_winM.parmlines.index(event_p.artist)            
            self.grap_winM.mov_link=self.grap_winM.canvas.mpl_connect(
                                           'motion_notify_event', self.onmovingM)         
        else:
            return 
        return 
        
    def onrelease(self,event_r):
        #print "release"
        if hasattr(self.grap_winE, "mov_link"):
            self.grap_winE.canvas.mpl_disconnect(self.grap_winE.mov_link)
        if hasattr(self.grap_winF, "mov_link"):
            self.grap_winF.canvas.mpl_disconnect(self.grap_winF.mov_link)
        if hasattr(self.grap_winM, "mov_link"):
            self.grap_winM.canvas.mpl_disconnect(self.grap_winM.mov_link)    
        #if self.out:
        #    return
        string_params= [self._Eop, self._skmin, self._skmax, 
                                    self._rbkg, self.kweigth]
                          
        for item in zip(self.parN,string_params):
            value=PPset.spectra[self.num].autobk_details.call_args[item[0]]
            if value is None:
                item[1].set('default')
            else: 
              item[1].set(round(value,2))
        self.refresh()   


    def onmovingE(self, event):
        if self.out:
           onrelease(self,"pippo")
           return
        param_n=self.grap_winE.param_num
        Epar=['kmin','kmax']
        PPset.spectra.call_abk[Epar[param_n]]=round(event.xdata,2)
        Epar=['Fkmin','Fkmax']
        PPset.spectra.call_abk[Epar[param_n]]=round(event.xdata,2)        
        self.panor2(self.num)
        
    def onmovingF(self, event):
        param_n=self.grap_winF.param_num
        Epar=['rbkg']
        PPset.spectra.call_abk[Epar[param_n]]=round(event.xdata,2)
        self.panor2(self.num)        
        
    def onmovingM(self, event):
        param_n=self.grap_winM.param_num
        Epar=['e0']
        PPset.spectra.call_abk[Epar[param_n]]=round(event.xdata,2)
        self.panor2(self.num)         
   #--------------------------  Function  -----------------------------------------------------         
    
    def preposted(self):
        """ perform EXAFS calc"""
        #print"pass form prposted"
        if len(PPset.spectra)>0:
            spectrum=PPset.spectra[self.num]
            #try:
            spectrum.EXAFS_EX(**PPset.spectra.call_abk)
            spectrum.FT_F(**PPset.spectra.call_abk)
            spectrum.chiw=spectrum.chi*spectrum.k**int(self.kweigthp.get())
        return
            
    def refresh(self):
        """refresh picture when parameter are change in the textbox\n\n"""
        self.saveparam(destroy=False)
        self.preposted()              #perform calc#
        
        self.grap_winE.figsub.clear()
        self.grap_winE.plot(self.num)
        e0=PPset.spectra[self.num].e0
        k1=PPset.spectra[self.num].autobk_details.kmin
        k2=PPset.spectra[self.num].autobk_details.kmax
        rbkg=PPset.spectra[self.num].autobk_details.call_args['rbkg']
        
        w = self.kweigthp.get()
        valuesE = numpy.array((k1,k2))
        self.grap_winE.paramplot(valuesE, ["g"]*2, ["kmin", "kmax"])
        self.grap_winE.panor(self.num)
        self.grap_winE.figsub.set_ylabel('$k\chi(k) (\AA^{-%d})$' %w)        
        
        w1 = self.kweigth.get()
        self.grap_winF.figsub.clear()        
        self.grap_winF.plot(self.num)
        self.grap_winF.figsub.set_xlim(0,6)
        self.grap_winF.figsub.set_ylim(0,None)        
        self.grap_winF.paramplot([PPset.spectra.call_abk["rbkg"]], ["r"],["rbkg"])
        self.grap_winF.panor(self.num)
        self.grap_winF.figsub.set_ylabel('$FT(k^%d\chi(k)) (\AA^{-%d})$'%(w1,w1+1))
        
        self.grap_winM.figsub.clear()        
        self.grap_winM.plot(self.num) 
        self.grap_winM.paramplot([e0], ["r"],["e0"])        
        self.grap_winM.panor(self.num) 
        
            
    def panor2(self,event):
        """when the params are moved slider is moved"""
        self.num=int(event)
        self.preposted()
        self.grap_winE.panor(self.num)
        self.grap_winF.panor(self.num)
        self.grap_winM.panor(self.num) 
            
           
            
    
    def saveparam(self, destroy=True):
        ##########################################################################
        def error_message(Name):
            print "\nPlease write a numerical value for "+ Name +"\n" +  \
                     "for Larch default, write \"None\" or \"default\" \n"
        ##########################################################################
        def check_input(Name, variable, default):
            xxx=variable.get()
            if "default" in xxx:PPset.spectra.call_abk[Name]=default
            elif xxx=='None':PPset.spectra.call_abk[Name]=default  
            else:
                try:   PPset.spectra.call_abk[Name] = round(float(variable.get()),2)
                except SyntaxError:error_message(Name)
        ##########################################################################        
        check_input("e0",self._Eop,None)
        check_input("kmin",self._skmin,0)
        check_input("kmax",self._skmax,None)
        check_input("Fkmin",self._skmin,0)
        check_input("Fkmax",self._skmax,None)        
        check_input("rbkg",self._rbkg,1)
        PPset.spectra.call_abk["kweight"] = self.kweigth.get()
        if destroy:
            self.genitore.destroy()
        return
        


    ##################
       



###########################################################################################clas####
class FTparam(object):
    def __init__(self, genitore):
        self.genitore=genitore
       #--------------------------   Declare--------------------------------------------------
        self._kstart      = StringVar()
        self._kend        = StringVar()
        self.FTweigth     = IntVar()
        self._FTWind      = StringVar()
        self._dk          = StringVar()
        self.kweigthp= IntVar()
        


       #--------------------------   Define--------------------------------------------------
        packLabelFrame = {"side" : TOP,  "expand" : YES, "anchor" : W, "pady" : 3}
        packEntry      = {"side" : LEFT,   "anchor" : W, "pady" : 6, "padx" : 3, "fill" : X }  
        self.num=0
        self.kweigthp.set(1)

        
        if PPset.spectra.call_xftf["dk"]:      self._dk.set(PPset.spectra.call_xftf["dk"]) 
        else:      self._dk.set("default")   
        
        if PPset.spectra.call_xftf["kmin"]:   self._kstart.set(PPset.spectra.call_xftf["kmin"])
        else:      self._kstart.set(0)
        
        if PPset.spectra.call_xftf["kmax"]:   self._kend.set(PPset.spectra.call_xftf["kmax"]) 
        else:      self._kend.set("default") 
              
        if PPset.spectra.call_xftf["kweight"]:self.FTweigth.set(PPset.spectra.call_xftf["kweight"])
        else:      self.FTweigth.set(1) 

        if PPset.spectra.call_xftf["window"]:  self._FTWind.set(PPset.spectra.call_xftf["window"])
        else:     self._FTWind.set('kaiser')
        
       #------------------------------------------------------
        self.param_win = Frame(genitore)
        self.param_win.pack(side=LEFT)
        
        self.quadro_FT = LabelFrame(self.param_win, text = "Foward FT")    #,text = "Correction"
        self.quadro_FT.pack(side = TOP,  fill = X, pady= 3, ipadx = 5, ipady = 3)
        self.quadro_FT1 = Frame(self.quadro_FT)
        self.quadro_FT1.pack(side = TOP,  fill = X)
        self.quadro_FTweigth = LabelFrame(self.quadro_FT1, text = "FT_wgt Plot_wgt")
        self.quadro_FTweigth.pack(**packLabelFrame)
        self.spin_FTweigth = Spinbox(self.quadro_FTweigth, from_ = 0, to = 3, textvariable= self.FTweigth, width = 3)
        self.spin_FTweigth.pack(side = LEFT ,anchor = S, pady=5, padx = 5, ipadx = 1)
        self.spin_kweigthp = Spinbox(self.quadro_FTweigth, from_ = 0, to = 3, textvariable= self.kweigthp, width = 2)
        self.spin_kweigthp.pack(side = LEFT ,anchor = W, padx = 8, ipadx = 2, ipady = 3) #, expand = YES,  fill = BOTH
        #Label(self.quadro_FT1, text = "FT_weigth", justify = LEFT).pack(side = LEFT, anchor = S, pady=10)
        self.quadro_FTwin = LabelFrame(self.quadro_FT1, text = "FT_win")
        self.quadro_FTwin.pack(**packLabelFrame)
        self.combo_FTw= ttk.Combobox(self.quadro_FTwin , state="readonly",   
                     textvariable=self._FTWind, width=5,
                     values=('kaiser', 'hanning', 'welch', 'sine'))
        self.combo_FTw.pack(side = LEFT ,anchor = S, pady=5, padx = 5, ipadx = 1)
        self.quadro_FT_lim1 = LabelFrame(self.quadro_FT1, text = "k start")
        self.quadro_FT_lim1.pack(**packLabelFrame)
        self._entry_FT_kstart= Entry(self.quadro_FT_lim1, width = 7, textvariable=self._kstart)
        self._entry_FT_kstart.pack(**packEntry)
        self.quadro_FT_lim2 = LabelFrame(self.quadro_FT1, text = "k end")
        self.quadro_FT_lim2.pack(**packLabelFrame)        
        self._entry_FT_kend= Entry(self.quadro_FT_lim2, width = 7, textvariable=self._kend)
        self._entry_FT_kend.pack(**packEntry)
        self.quadro_FT_dk = LabelFrame(self.quadro_FT1, text = "dk")
        self.quadro_FT_dk.pack(**packLabelFrame)
        self._entry_FT_dk= Entry(self.quadro_FT_dk, width = 7, textvariable=self._dk)
        self._entry_FT_dk.pack(**packEntry)
        self.quadro_FT2 = Frame(self.quadro_FT)
        self.quadro_FT2.pack(side = TOP,  fill = BOTH, expand= YES,)
        self.quadro_FTMg = LabelFrame(self.quadro_FT2, text = "FT Mag.")
        self.quadro_FTMg.pack(fill= X, **packLabelFrame)
        self.quadro_FTIm = LabelFrame(self.quadro_FT2, text = "FT Im.")
        self.quadro_FTIm.pack(fill= X, **packLabelFrame)

        self.rerefresh = Button(self.param_win,
                                     command = self.refresh,#lambda x= self.num: self.refresh(x),
                                      text = "refresh",
                                      background = "violet",
                                      width = 8,
                                      padx = "3m",
                                      pady = "2m")
        self.rerefresh.pack(side = TOP, anchor = W, padx = 5, pady = 3)

        self.resave = Button(self.param_win,
                                      command = self.saveparam,
                                      text = "Save param",
                                      background = "green",
                                      width = 8,
                                      padx = "3m",
                                      pady = "2m")
        self.resave.pack(side = TOP, anchor = W, padx = 5, pady = 3)
        
       #--------------------------   Graphic win  --------------------------------------------------
        #self.graphframeM = Frame(genitore)        
        #self.graphframeM.pack(side = LEFT, fill=BOTH, expand=YES)
        self.graphframeE = Frame(genitore)        
        self.graphframeE.pack(side = LEFT, fill=BOTH, expand=YES)
        self.graphframeF = Frame(genitore)        
        self.graphframeF.pack(side = LEFT, fill=BOTH, expand=YES)
        self.grap_winE=ut.ParamGraph(self.graphframeE, PPset.spectra, "k", ["chiw","kwin"])
        self.grap_winF=ut.ParamGraph(self.graphframeF, PPset.spectra, "r", ["chir_mag"])
        if (len(PPset.spectra)>1):
            self.grap_winF.slider.pack_forget()
            self.grap_winE.slider.pack_forget()
            self.slider = Scale(genitore, from_= 0, to=len(PPset.spectra)-1,
                                         command =self.panor2, 
                                         orient=VERTICAL,
                                         label= "Spectra"
                                         )
            self.slider.pack(side = LEFT,fill = Y, anchor = N,pady = 5, ipady = 0)
        self.grap_winE.pick=self.grap_winE.canvas.mpl_connect('pick_event', self.onpick)                     # new pick release link
        self.grap_winE.release=self.grap_winE.canvas.mpl_connect('button_release_event', self.onrelease)
        self.grap_winE.canvas.mpl_connect('figure_leave_event', self.onout)
        self.out=False
        self.refresh()
        genitore.wait_window()            
        
   #--------------------------  mouse Function  ----------------------------------------------------- 
    def onout(self,event_p):
        self.out=True
        
    def onpick(self,event_p):
        if event_p.artist in self.grap_winE.parmlines: 
            self.out=False
            self.grap_winE.param_num= self.grap_winE.parmlines.index(event_p.artist)            
            self.grap_winE.mov_link=self.grap_winE.canvas.mpl_connect(
                                           'motion_notify_event', self.onmovingE)
        else:
            return True
        return True    
        
    def onrelease(self,event_r):
        #print "release"
        if hasattr(self.grap_winE, "mov_link"):
            self.grap_winE.canvas.mpl_disconnect(self.grap_winE.mov_link)
        if hasattr(self.grap_winF, "mov_link"):
            self.grap_winF.canvas.mpl_disconnect(self.grap_winF.mov_link)
        if self.out:
            return
        string_params= [self._kstart, self._kend]
                          
        for item in zip(['kmin','kmax'],string_params):
            value=PPset.spectra[self.num].xftf_details.call_args[item[0]]
            if value is None:
                item[1].set('default')
            else: 
                item[1].set(round(value,2))    
        self.refresh()   


    def onmovingE(self, event):
        if self.out:
           onrelease(self,"pippo")
           return
        param_n=self.grap_winE.param_num
        Epar=['kmin','kmax']
        PPset.spectra.call_xftf[Epar[param_n]]=round(event.xdata,2)
        self.panor2(self.num)
        
      
        

   #--------------------------  Function  -----------------------------------------------------         
    def preposted(self):
        """ perform EXAFS calc"""
        #print"pass form prposted"
        if len(PPset.spectra)>0:
            spectrum=PPset.spectra[self.num]
            if not(hasattr(spectrum, 'chi')):
                spectrum.EXAFS_EX(**PPset.spectra.call_abk)
            spectrum.chiw=spectrum.chi*spectrum.k**int(self.kweigthp.get())    
            ##try:
            spectrum.FT_F(**PPset.spectra.call_xftf)
            ##except Exception as wert:    
              #print "proposted bad", PPset.spectra.call_xftf    
              #print wert, "\n"
        return
            
    def refresh(self):
        """refresh picture when parameter are change in the textbox\n\n"""
        self.saveparam(destroy=False)
        self.preposted()              #perform calc#
        spectrum=PPset.spectra[self.num]
        
        k1=PPset.spectra[self.num].xftf_details.call_args['kmin']
        k2=PPset.spectra[self.num].xftf_details.call_args['kmax']
        if not(k2): k2=spectrum.k[-1]
        
        self.grap_winE.figsub.clear()
        self.grap_winE.plot(self.num)
        valuesE = numpy.array([k1,k2])
        maxy=max(max(spectrum.chiw),max(spectrum.kwin))*1.05
        self.grap_winE.figsub.set_ylim(None,maxy)
        self.grap_winE.paramplot(valuesE, ["g"]*2, ["kmin", "kmax"])
        self.grap_winE.panor(self.num)
        
        self.grap_winF.figsub.clear()  
        self.grap_winF.plot(self.num)
        self.grap_winF.figsub.set_xlim(0,6)
        self.grap_winF.figsub.set_ylim(0,None) 
        self.grap_winF.panor(self.num)
        
        
            
    def panor2(self,event):
        """when the params are moved slider is moved"""
        self.num=int(event)
        self.preposted()
        self.grap_winE.panor(self.num)
        self.grap_winF.panor(self.num)
            
           
            
    
    def saveparam(self, destroy=True):
        ##########################################################################
        def error_message(Name):
            print "\nPlease write a numerical value for "+ Name +"\n" +  \
                     "for Larch default, write \"None\" or \"default\" \n"
        ##########################################################################
        def check_input(Name, variable, default):
            xxx=variable.get()
            if "default" in xxx:PPset.spectra.call_xftf[Name]=default
            elif xxx=='None':PPset.spectra.call_xftf[Name]=default  
            else:
                try:   PPset.spectra.call_xftf[Name] = round(float(variable.get()),2)
                except SyntaxError:error_message(Name)
        ##########################################################################        
        check_input("kmin",self._kstart,0)
        check_input("kmax",self._kend,None)
        check_input("dk",self._dk,1)
        PPset.spectra.call_xftf["window"] = self._FTWind.get()        
        PPset.spectra.call_xftf["kweight"] = self.FTweigth.get()
        if destroy:
            self.genitore.destroy()
        return
        


    ##################


###########################################################################################clas####
class EXAFT():
    def __init__(self, genitore):
      #-------------------------------    declare    ----------------------------------------------
        self._check_FT    = IntVar()
        self._check_exa   = IntVar()
        self.kweigthplot  = IntVar()
        packLabelFrame = {"side" : LEFT,  "expand" : YES, "anchor" : W, "pady" : 3}
        packEntry      = {"side" : LEFT,   "anchor" : W, "pady" : 6, "padx" : 3, "fill" : X }   # "expand" : YES,
      #---------------------------------  set      ------------------------------------------

        self._check_exa.set(1)
        self.kweigthplot.set(1)
        #---------------------------------  set      ------------------------------------------

        self.Eop  =    0
        self.rbkg =    0
        self.pr_es=    0
        self.pr_ee=    0
        self.po_es=    0
        self.po_ee=    0
        self.skmax=    0
        self.skmin=    0
      #--------------------------------EXAFS--------------------------------------------------------
        self.quadro_exafs = LabelFrame(genitore, text = "EXAFS extraction")    #,text = "Correction"
        self.quadro_exafs.pack(side = TOP,  fill = X, pady= 3, ipadx = 5, ipady = 3)
        self.quadro_exafs1 = Frame(self.quadro_exafs)    #,text = "Correction"
        self.quadro_exafs1.pack(side = TOP,  fill = X, pady=5)
        #Label(self.quadro_exafs1, text = "k_weigth", justify = LEFT).pack(side = LEFT, anchor = W, expand =Y)
        self.button_exafs_default = Button(self.quadro_exafs1,
                                        command = self.EXAFSparam,
                                        text = "EXAFS param.",
                                        background = "violet",
                                        width = 10,
                                        padx = "3m",
                                        pady = "2m")
        self.button_exafs_default.pack(side = LEFT, anchor = W, padx = 5, pady = 2)
        self.quadro_exafs2 = Frame(self.quadro_exafs)    #,text = "Correction"
        self.quadro_exafs2.pack(side = TOP,  fill = BOTH, pady=2,expand= YES,)
        self.quadro_EXA_bkg = LabelFrame(self.quadro_exafs2, text = "EXA_bkg")
        self.quadro_EXA_bkg.pack(fill= X, **packLabelFrame)
        self.quadro_EXA_chi= LabelFrame(self.quadro_exafs2, text = "EXAFS signal k")
        self.quadro_EXA_chi.pack(fill= X, **packLabelFrame)
        self.spin_kweigthplot = Spinbox(self.quadro_EXA_chi, from_ = 0, to = 3,
            textvariable= self.kweigthplot, width = 1, command= self.kwrefresh)
        self.spin_kweigthplot.pack(side =LEFT, ipady =3)
        self.bkg_PlSa_But=ut.PloteSaveB(self.quadro_EXA_bkg, ext=".bkg" ,
                                        comment= None, title="background" )
        self.bkg_PlSa_But.Button_plot.configure(command = self.plot2)
        self.exa_PlSa_But=ut.PloteSaveB(self.quadro_EXA_chi, ext=".chi", 
                                        xlabel= '$k(\AA^{-1})$',
                                        ylabel='$k\chi(k) (\AA^{-1})$', 
                                        comment= None, title="Exafs")

      #-------------------------------------FT------------------------------------------------------------------------
        self.quadro_FT = LabelFrame(genitore, text = "Foward FT")    #,text = "Correction"
        self.quadro_FT.pack(side = TOP,  fill = X, pady= 3, ipadx = 5, ipady = 3)
        self.quadro_FT1 = Frame(self.quadro_FT)
        self.quadro_FT1.pack(side = TOP,  fill = X)
        self.button_FT_default = Button(self.quadro_FT1,
                                        command = self.FTparam,
                                        text = "FT param.",
                                        background = "violet",
                                        width = 10,
                                        padx = "3m",
                                        pady = "2m")
        self.button_FT_default.pack(side = LEFT, anchor = W, padx = 5, pady = 2)
        self.quadro_FT2 = Frame(self.quadro_FT)    #,text = "Correction"
        self.quadro_FT2.pack(side = TOP,  fill = BOTH, pady=2,expand= YES,)

        self.quadro_FT2 = Frame(self.quadro_FT)
        self.quadro_FT2.pack(side = TOP,  fill = BOTH, expand= YES,)
        self.quadro_FTMg = LabelFrame(self.quadro_FT2, text = "FT Mag.")
        self.quadro_FTMg.pack(fill= X, **packLabelFrame)
        self.quadro_FTIm = LabelFrame(self.quadro_FT2, text = "FT Im.")
        self.quadro_FTIm.pack(fill= X, **packLabelFrame)
        self.FTMg_PlSa_But=ut.PloteSaveB(self.quadro_FTMg, ext=".ftmg" ,comment= None, title="FT Mag")
        self.FTIm_PlSa_But=ut.PloteSaveB(self.quadro_FTIm, ext=".ftim" ,comment= None, title="FT Im")
      #--------------------------------------Perform----------------------------------------------------
        self.quadro_perform = LabelFrame(genitore)    #,text = "Correction"
        self.quadro_perform.pack(side = BOTTOM,  fill = X, expand =YES)
        self.button_exa_per = Button(self.quadro_perform, #
                                      command = self.Perform,
                                      text = "Perform" ,
                                      background = "green",
                                      width = 10,
                                      padx = "3m",
                                      pady = "2m")
        self.button_exa_per.pack(side = LEFT, anchor = W, padx = 5, pady = 5)
        self.check_exa=Checkbutton(self.quadro_perform, text="EXAFS" ,variable=self._check_exa )
        self.check_exa.pack(side = LEFT,  fill = Y ,anchor = W, ipady = 1, padx = 5)
        self.check_FT=Checkbutton(self.quadro_perform, text="FT"    ,variable=self._check_FT)
        self.check_FT.pack(side = LEFT,  fill = Y ,anchor = W, ipady = 1, padx = 5)
      #---------------------------------Function--------------------------------------------------------
    def kwrefresh(self):
        w = self.kweigthplot.get()
        c1="#L k  chik**"+ str(w)+"\n"
        for item in self.exa_PlSa_But.comments: item.pop(); item.append(c1)
        self.exa_PlSa_But.title = "EXAFS chi*k**"+str(w)
        self.exa_PlSa_But.figsub.set_ylabel('$k\chi(k) (\AA^{-%d})$' %w)
        self.exa_PlSa_But.y_array= [item.chi*item.k**w for item in PPset.spectra]

    def plot2(self):
        self.bkg_PlSa_But.plot(self.quadro_EXA_chi, ext=".bkg", 
                                        xlabel= 'mu (abs. unit)' u'k (\u207B\u00B9)',
                                        ylabel='energy (eV)'   'chi(k)', 
                                       comment= None, title="background")
        self.bkg_PlSa_But.graph.clear()
        self.bkg_PlSa_But.graph.plot([i.E   for i in PPset.spectra],
                                           [i.Mu  for i in PPset.spectra])
        self.bkg_PlSa_But.graph.plot( self.bkg_PlSa_But.x_array,
                                        self.bkg_PlSa_But.y_array)

    def Perform(self):
        self._check_exa.get()
        self._check_FT.get()
        #-----------------         EXAFS      ---------------------
        if self._check_exa.get():
            w = int(self.kweigthplot.get())
            pb_label=Label(self.quadro_perform, text='EXAFS')
            pb_label.pack(side = LEFT,anchor = W, expand = 0, fill = None)            
            pb = ttk.Progressbar(self.quadro_perform, orient='horizontal', 
                                             mode='determinate',
                                             maximum=len(PPset.spectra))
            pb.pack(side = LEFT,anchor = W, expand = 1, fill = X)
            for item in PPset.spectra:
                ceck=item.EXAFS_EX(**PPset.spectra.call_abk)
                pb.step() ; pb.update_idletasks()
            pb_label.destroy()
            pb.destroy()
            self.exa_PlSa_But.x_array= [item.k for item in PPset.spectra]
            self.exa_PlSa_But.y_array= [item.chi*item.k**w for item in PPset.spectra]
            self.bkg_PlSa_But.x_array= [item.E for item in PPset.spectra]
            self.bkg_PlSa_But.y_array= [item.bkg for item in PPset.spectra]
            #-------------------- Define Comments
            exaheader=list(PPset.spectra.header)
            self.exa_PlSa_But.comments= [exaheader for item in PPset.spectra]
            self.exa_PlSa_But.title = "EXAFS chi*k**%i" %w
            xLabel="\n# k  chik**%i\n" %w
            c1='# autobk '
            for i,key in enumerate(PPset.spectra.call_abk.keys()):
               if i>0 and i%5==0: c1+='\n#'
               c1+=' {kkey}:{value}'.format(kkey=key,value= PPset.spectra.call_abk[key])
            self.exa_PlSa_But.comments[0].append(c1+xLabel)
            bkheader=exaheader[:-1].append("# E  bkg\n")
            self.bkg_PlSa_But.comments= [bkheader for item in PPset.spectra]
        #-----------------         FT      ---------------------
        if self._check_FT.get():
            w = PPset.spectra.call_xftf['kweight']
            #---------------progress bar
            pb_label=Label(self.quadro_perform, text='FT')
            pb_label.pack(side = LEFT,anchor = W, expand = 0, fill = None)            
            pb = ttk.Progressbar(self.quadro_perform, orient='horizontal', 
                                             mode='determinate',
                                             maximum=len(PPset.spectra))
            pb.pack(side = LEFT,anchor = W, expand = 1, fill = X)
            #---------------main cycle
            for item in PPset.spectra:
                item.FT_F(**PPset.spectra.call_xftf)
                pb.step() ;pb.update_idletasks()
            pb_label.destroy()
            pb.destroy()    
            self.FTMg_PlSa_But.x_array= [item.r for item in PPset.spectra]
            self.FTMg_PlSa_But.y_array= [item.chir_mag for item in PPset.spectra]
            self.FTIm_PlSa_But.x_array= [item.r for item in PPset.spectra]
            self.FTIm_PlSa_But.y_array= [item.chir_im for item in PPset.spectra]
            self.FTMg_PlSa_But.title = "FT chi*k**%i" %w
            self.FTIm_PlSa_But.title = "FT chi*k**%i" %w
            #---------------comments
            ftheader=list(PPset.spectra.header)
            xLabel= "\n# R  FT_Mg%i\n" %w
            c1='# autobk '
            for i,key in enumerate(PPset.spectra.call_abk.keys()):
               if i>0 and i%5==0: c1+='\n#'
               c1+=' {kkey}:{value}'.format(kkey=key,value= PPset.spectra.call_abk[key])
            c1+='\n# xfft'
            for i,key in enumerate(PPset.spectra.call_xftf.keys()):
               if i>0 and i%5==0: c1+='\n#'
               c1+=' {kkey}:{value}'.format(kkey=key,value= PPset.spectra.call_xftf[key])            
            ftheader.append(c1+xLabel)
            self.FTMg_PlSa_But.comments= [ftheader for item in PPset.spectra]
            ftiheader=ftheader[:-1].append("\n# R  FT_I%i\n" %w)
            self.FTIm_PlSa_But.comments= [ftheader for item in PPset.spectra]
        print "\n---module EXAFS done\n"    
            
            
        return

    def EXAFSparam(self):
        if hasattr(self, "topX"): return
        self.topX = Toplevel()
        self.topX.title("EXAFS PARAMETER") 
        self.EXE_par=EXAFSparam(self.topX)
        del self.EXE_par
        del self.topX
        
    def FTparam(self):
        if hasattr(self, "topX"): return
        self.topX = Toplevel()
        self.topX.title("FT PARAMETER") 
        self.FT_par=FTparam(self.topX)
        del self.FT_par
        del self.topX

        #root.protocol("WM_DELETE_WINDOW", callback)







if __name__ == "__main__":
   import bm29  
   filenames=["D:/home/cprestip/mes documents/data_fit/bordeaux/Run4_bordeax/Ca2Mn3O8/raw/Ca2Mn3O8_ramp1_H2_0000_0.up",
              "D:/home/cprestip/mes documents/data_fit/bordeaux/Run4_bordeax/Ca2Mn3O8/raw/Ca2Mn3O8_ramp1_H2_0001_0.up",
              "D:/home/cprestip/mes documents/data_fit/bordeaux/Run4_bordeax/Ca2Mn3O8/raw/Ca2Mn3O8_ramp1_H2_0002_0.up",
              "D:/home/cprestip/mes documents/data_fit/bordeaux/Run4_bordeax/Ca2Mn3O8/raw/Ca2Mn3O8_ramp1_H2_0003_0.up",
              "D:/home/cprestip/mes documents/data_fit/bordeaux/Run4_bordeax/Ca2Mn3O8/raw/Ca2Mn3O8_ramp1_H2_0004_0.up",
              "D:/home/cprestip/mes documents/data_fit/bordeaux/Run4_bordeax/Ca2Mn3O8/raw/Ca2Mn3O8_ramp1_H2_0005_0.up",
              "D:/home/cprestip/mes documents/data_fit/bordeaux/Run4_bordeax/Ca2Mn3O8/raw/Ca2Mn3O8_ramp1_H2_0006_0.up",
              "D:/home/cprestip/mes documents/data_fit/bordeaux/Run4_bordeax/Ca2Mn3O8/raw/Ca2Mn3O8_ramp1_H2_0007_0.up",
              "D:/home/cprestip/mes documents/data_fit/bordeaux/Run4_bordeax/Ca2Mn3O8/raw/Ca2Mn3O8_ramp1_H2_0008_0.up",
              "D:/home/cprestip/mes documents/data_fit/bordeaux/Run4_bordeax/Ca2Mn3O8/raw/Ca2Mn3O8_ramp1_H2_0009_0.up",
              "D:/home/cprestip/mes documents/data_fit/bordeaux/Run4_bordeax/Ca2Mn3O8/raw/Ca2Mn3O8_ramp1_H2_0010_0.up",
              "D:/home/cprestip/mes documents/data_fit/bordeaux/Run4_bordeax/Ca2Mn3O8/raw/Ca2Mn3O8_ramp1_H2_0011_0.up",
              "D:/home/cprestip/mes documents/data_fit/bordeaux/Run4_bordeax/Ca2Mn3O8/raw/Ca2Mn3O8_ramp1_H2_0012_0.up",
              "D:/home/cprestip/mes documents/data_fit/bordeaux/Run4_bordeax/Ca2Mn3O8/raw/Ca2Mn3O8_ramp1_H2_0013_0.up"]
   filenames=filenames*2           
   for i in filenames:
       PPset.spectra.append(bm29.bm29file(i))
   PPset.spectra.header=['pippo\n']    
   x=range(1,len(PPset.spectra)+1)    
   radice = Tk()
   radice.title("EXAFS GUI")
   pippo = EXAFT(radice)
   radice.mainloop()