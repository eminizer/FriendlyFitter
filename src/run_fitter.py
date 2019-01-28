###################################################################################################
### This is the main script to run the FriendlyFitter package I'm writing for the Advanced Lab ####
### class at Johns Hopkins University. ############################################################
### copyright 2019/contact margaret.eminizer@gmail.com ############################################
###################################################################################################

#imports
from optparse import OptionParser
from os import path, system
from config import Config
from fit import Fit
from datetime import date

#User Options
parser = OptionParser()
#Run with what input file?
parser.add_option('-I','--input', type='string', action='store', dest='inputfilepath',
				  default='speed_of_light_example_input.csv', 
				  help='Path to input csv file')
#Run with what output file name?
parser.add_option('-O','--output', type='string', action='store', dest='outputfilename',
				  default='', 
				  help='Name of file to store output')
#parser.add_option('--saveToys',  action='store_true', dest='savetoys')
(options, args) = parser.parse_args()

#Main script
print('Running FriendlyFitter with input file '+options.inputfilepath+'...')

#Get the fit configuration from the config file parser
print('	Building fit configuration...')
if not path.isfile(options.inputfilepath) :
	print('ERROR: file '+options.inputfilepath+' does not exist!')
	exit()
thisfitconfig = Config(options.inputfilepath)
print('	Done.')

#Initialize the fit with the configuration
print('	Initializing fit object...')
thisfit = Fit(thisfitconfig)
print('	Done.')

#perform the fit
print('	Minimizing...')
thisfit.minimize()
print('	Done.')

#write the output file
outfilename = ( 'FriendlyFitter_output_'+str(date.today())+'.txt' if options.outputfilename=='' 
				else options.outputfilename )
if not outfilename.endswith('.txt') : outfilename+='.txt'
print('	Writing output of fit to file '+outfilename+'...')
thisfit.writeOutput(outfilename)
print('	Done.')

#save a plot of the fit
plotfilename = ( 'FriendlyFitter_plot_'+str(date.today())+'.png' if options.outputfilename=='' 
				else options.outputfilename )
if not plotfilename.endswith('.png') : plotfilename+='.png'
print('	Saving fit plot to file '+plotfilename+'...')
thisfit.savePlot(plotfilename)
print('	Done.')

print('All done!')

print('Output file:')
system('cat '+outfilename)
