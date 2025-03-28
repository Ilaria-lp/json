#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__  = "Ilaria Carlomagno"
__license__ = "MIT"
__version__ = "1.0"
__email__ = "ilaria.carlomagno@elettra.eu"


import glob
import json
import numpy as np
import os

fluo_key = "Events_in_livetime"
EXT = 'json'
       
def extract_json_xrf(file_path):
 
    # Open and load the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)
    
        all_data = data["Data"]
        xrf_spectrum = np.array(all_data["Histograms"])
        xrf_spectrum = xrf_spectrum.reshape(-1,4096)
        elem, chan = np.shape(xrf_spectrum)
        
        xrf_spectrum = np.transpose(xrf_spectrum)

        out_file = open(file_path[:-5] + '_xrf_data.txt','w')
        
        out_file.write('# Total XRF \t')   
        for i in range(elem):
            out_file.write('Elem['+str(i+1)+']\t')
        out_file.write('\n')            
        
        for row in range(chan):
            for col in range(elem):
                out_file.write(str(np.sum(xrf_spectrum[row], axis=0))+'\t')
                out_file.write(str(xrf_spectrum[row][col])+'\t')
            out_file.write('\n')
        out_file.close()

if __name__ == "__main__":
    
    print('\t-------------------------------------------------\n')
    print('\t---------           Welcome!         ------------\n')
    print("\t---     Let's extract your XRF spectra!       ---\n")
    print('\t-------------------------------------------------\n')
    
    in_path = './'
    #out_path = in_path + 'xrf_spectra'
    
    # checks automatically all the h5 files in the in_path 
    file_list = glob.glob('{0}/*'.format(in_path)+EXT)
    print('\tI found '+str(len(file_list))+' files matching the extension '+EXT+':')
    print('\t' + str(file_list))
    print('\n')
    
    if len(file_list) == 0:
        print("\t⚠ Can't do much with 0 files! Sorry!")
        print("\tMove the maps in the same folder as the program and try again!")   
    else: 
        print("\tThe xrf spectra from all the files mentioned above will be saved in a txt file.\n")

        for filename, i in zip(file_list, range(len(file_list))):
            filename = filename[2:]
            extract_json_xrf(filename)
            print('\n- - - - XRF spectrum {0}/{1} successfully extracted.\n'.format(i+1, len(file_list)))

    print('\t ☆ Have a nice day ☆ \n')