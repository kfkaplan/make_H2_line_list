#Program creates H2 ground state rovibrational line list from the ground state rovibrational state energies given in 
#Table 1 of Komasa et al. (2011).  This should be more accurate than the previous version which used the Energy Levels from Dabrowski (1984)
#
#Created by Kyle Kaplan
#Modifed by kyle Kaplan on Sep. 06, 2016 to test the wavelengths of the calculated levels in Drabrowski (1984)
#Modifed by kyle Kaplan on Oct. 29, 2016 to use the much more accurate theoretical energy levels from Komasa et al. (2011)

from pylab import *

J_max = 40 #Maximum J level to save, to cut down on extraneous lines

#wave_range = [1.4, 2.6] #Set wavlelength range in microns
wave_range = [0.0001, 50000000.0] #Set wavlelength range in microns
J_label = array(['Q', 'S', 'O']) #Set labels for J transitions
J_transitions = array([0, 2, -2]) #Set allowed J transitions

file_name = 'kosama_2011_energy_levels.dat' #Name of data file storing energy level data
V, J = loadtxt(file_name, usecols=(0,1), unpack=True, dtype='int') #Read in energy level data
energy = loadtxt(file_name, usecols=(2,), unpack=True, dtype='float')

wavelengths = array([], dtype='float') #Set up lists to store wavelengths and labels of found lines
labels = array([], dtype='S')

n_levels = len(V) #number of rovibrational energy levels
n_level_range = range(n_levels)
for i in n_level_range: #Loop through each energy level
	for j in n_level_range: #Loop through each other energy level to compare the first level to the second
		J_diff = int(J[i] - J[j]) #Calculate delta J
		V_diff = int(V[i] - V[j]) #Calculate delta V
		energy_diff = energy[j] - energy[i] #Calculate difference in energy between levels levels (in units of inverse cm)
		wavelength = energy_diff**(-1) * 10000.0 #Convert energy in units of inverse cm into wavelength in units of microns
		if (J[i] <= J_max and J[j] <= J_max) and (J_diff == 0 or J_diff == -2 or J_diff == 2) and (J[i]!=0 or J[j] != 0) and energy_diff != 0.0 and wavelength > wave_range[0] and wavelength < wave_range[1]: #Check to make sure quantum selection rules are followed and no duplicate lines or backwards transitions are saved, and that we are in the right wave range
			label = str(V[i]) + '-' +  str(V[j]) + ' ' + J_label[J_diff == J_transitions][0] + '(' + str(J[j]) + ')' #Set up label for spectroscopic notation
			labels = append(labels, label) #Store label of line found
			wavelengths = append(wavelengths, wavelength) #Stire wavelength of line found

s = argsort(wavelengths) #sort results by wavelength
labels = labels[s]
wavelengths = wavelengths [s]

#utput = open("H2_line_list_2-4um.dat", "w") #Save example line list
output = open("H2_line_list_calcualted.dat", "w") #Save example line list
for i in range(len(labels)): #Loop through each line to save to line list
	output.write(str(wavelengths[i]) + '\t' + labels[i] + '\n') #and write each line to to the line list file in the format of (wavelength) <tab> (spectroscopic notation label)
	#output.write('<TR> <TD>' + str(wavelengths[i]) + '</TD> <TD>' + labels[i] + '</TD> </TR> \n') #Format for making html table
output.close() #Close line list file, now you are done!