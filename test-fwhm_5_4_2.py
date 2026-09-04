"""
This test example demonstrate plotting of phase map.
Two maps are constructed. First map of substracted baseline hyperspectral map. 
Second map without substraction
Class PhaseMapConstruction contains dictionaries:
###########################################################
dict_phase{} - spectra of founded different phases
dict_phase['phase'+str(self.i_tmp_map)]=[item_tmp,self.i_tmp_map,step_spectra,xmin,xmax,length]
Name of the dictionary element is phaseN (where is N - number of the phase)
item_tmp - y array of founded phase
self.i_tmp_map - global variable means number of phases
step_spectra - distance between x1
xmin - minimal x value
xmax - maximal x value
length - length of item_tmp
############################################################
foundedphases{} - spectra from database that are the most similar to dict_phase
foundedphases={'phaseN': {'x': [array([]),array([])...],'y': [array([]),array([])...], 'name':['   ', ' '....]}}
x - x array
y - y array
name - name of database element
#############################################################
In the bottom of the script the example of using these dictionaries is given
"""
import sys
import copy
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cm
import numpy as np 
import micromap as mm
 
def main():
  fname='.//sample_tomsk202604_transm.floats'

  GetMapData=mm.MapEdit(fname,2000,4000)

  mapS=GetMapData.read()
  TransformMap=mm.TransformData()
  TransformMap.AbsorbanceConvert_map(mapS)
  mapS_init=copy.deepcopy(mapS)
  TransformMap.clean_co2(mapS, num_proc = 8)
  array_dict = mapS
  x, y, z_dict, array_dict_, params = GetMapData.load_fit_results('fit_zone_5_202604.pkl')
  #z is array of dictionaries {'amplitude': A, 'FWHM': FWHM, 'center': C, 'height': H, 'r-square': Rsq}
  #Fit map of FWHMs of first peak 781 cm-1
  array_bad = []
  intensities = [{'vmin':0, 'vmax':0.4},{'vmin':0.1, 'vmax':0.4},{'vmin':0.1, 'vmax':0.4},{'vmin':0.1,'vmax':0.3},{'vmin':0.1, 'vmax':0.9},{'vmin':2.2, 'vmax':16},{'vmin':2.2, 'vmax':16},{'vmin':0.22, 'vmax':0.8}]
  z_333 = []
  z_222 = []
  for i in [0,1,2,3,4,5,6,7,8,9]:
    counter_ = 0
    z=[]
    for it in z_dict:
        if i==1:
            if counter_ in array_bad:
                z.append(np.nan)
            else:
                if it['FWHM'][1]<70:  
                    z_333.append(it['FWHM'][1])
                else:
                    z_333.append(np.nan)

        if i == 0:
            z_222.append(it['amplitude'][0])
            if it['amplitude'][i]<60:
                array_bad.append(counter_)
                z.append(np.nan)
        else:
            if counter_ in array_bad:
                z.append(np.nan)
            else:                  
                z.append(it['amplitude'][i]/it['amplitude'][1])
        counter_=counter_+1
    z=np.array(z)
    drawMap=mm.PlotMap(array_dict,x,y,z)
    if i>0:
      drawMap.plot_color_map_with_spectra(array_dict_,'jet',resolution=255,vmin = intensities[i-2]['vmin'],vmax = intensities[i-2]['vmax'])
    #plt.hist(z, bins=100)
  drawMap=mm.PlotMap(array_dict,x,y,z_333) 
  drawMap.plot_color_map_with_spectra(array_dict_,'jet',resolution=255)
  drawMap=mm.PlotMap(array_dict,x,y,z_222) 
  drawMap.plot_color_map_with_spectra(array_dict_,'jet',resolution=255)  
  drawMap.show()
  

  #Сохраняем спектры в выделенных точках в файл
  a=drawMap.save_selected('spectra_fwhm12_2.dat')
  for it in z_dict:
    for it_ in a['key']:
        if it['key']==it_:
            print(it_,'\t R-square=',str(it['r-square']))
            print('Center, cm-1','\t','Amplitude, cm-1','\t','FWHM, cm-1')
            for i in range(len(params['center'])):
                print(str(it['center'][i]),'\t',str(it['amplitude'][i]), '\t',str(it['FWHM'][i]))
    
  
if __name__ == "__main__":
    main()