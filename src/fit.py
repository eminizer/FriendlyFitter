###################################################################################################
### This file contains the Fit class for the FriendlyFitter package. ##############################
### copyright 2019/contact margaret.eminizer@gmail.com ############################################
###################################################################################################

#imports
from scipy import optimize
import numpy as np
import matplotlib.pyplot as plt
from datasets import LinearData, LinearDataYErrors, LinearDataXYErrors
from parameter import ParameterList

#Fit class
class Fit(object) :

	#initialize from configuration object
	def __init__(self, config) :
		#set everything to None or empty to begin
		self._data=None
		self._parameters=ParameterList()
		self._fit_function=None
		self._resid_function, self._resid_function_args=None,None
		#copy the configuration
		self._config = config
		#make the data objects from the config
		self._populate_data_object_from_config_()
		#make the list of parameters from the config and the data object
		self._make_parameterlist_from_config_and_data_()
		#set the fit function
		self._set_fit_function_and_params_()
		#set the residuals function
		self._set_resid_function_and_args_()

	#public functions
	#run the minimizer for the fit
	def minimize(self) :
		#run leastsq 
		pfit, pcov, infodict, errmsg, success = optimize.leastsq(self._resid_function, 
																 self._initial_parameters_list, 
																 args=self._resid_function_args,
																 full_output=True)
		#crash if the fit failed
		if success not in range(1,5) :	
			print('		Fit failed. Message: '+errmsg)
			exit()
		print('		Fit success; returned with flag '+str(success))
		print('		Fit function evaluated '+str(infodict['nfev'])+' times')
		print('		Final total residual value: '+str(infodict['fvec'].sum()))
		#calculate parameter uncertainties
		s_sq = (infodict['fvec']**2).sum()/(self._data.n_points()-len(pfit))
		pcov *= s_sq
		perrors = [] 
		for i in range(len(pfit)):
			try:
			  perrors.append(np.absolute(pcov[i][i])**0.5)
			except:
			  perrors.append( 0.00 )
		#set postfit parameter values/uncertainties
		self._parameters.setParametersPostfit(pfit,perrors)

	#save a plot of the raw data with the fit
	def savePlot(self,plotfilename) :
		#only generates plots for linear x-y fits at the moment
		if self._config.fit_type().startswith('linear_least_squares') :
			#make the x range space for the fit function line
			fitxspace = np.linspace(self._data.xMin(),self._data.xMax(),100)
			plt.figure()
			#plot the data
			plt.errorbar(self._data.xArray(),
						 self._data.yArray(),
						 xerr=self._data.xErrArray(),
						 yerr=self._data.yErrArray(),
						 fmt='o')
			#plot the fit
			plt.plot(fitxspace,
					 self._fit_function(self._parameters.bestFitValueList(),fitxspace),
					 'r-')
			#label the axes
			plt.xlabel(self._data.xAxisLabel())
			plt.ylabel(self._data.yAxisLabel())
			#nudge the left side and bottom into the frame a lil more
			plt.gcf().subplots_adjust(left=0.15,bottom=0.15)
			plt.savefig(plotfilename)

	#write results of fit to output file
	def writeOutput(self,outputfilename) :
		#labels for table columns
		fieldlabels = ['Parameter number','Full name','Short name',
					  'Initial value','Best Fit Value','Uncertainty']
		#values for table, one list per fit parameter
		paramfields = self._parameters.getFitParamPrintFieldsList()
		#dot separator line (also for formatting)
		dotlinefields = []
		for i in range(len(fieldlabels)) :
			maxlen = max([len(fieldlabels[i])]+[len(fl[i]) for fl in paramfields])
			dotlinefields.append('.'*maxlen)
		dotline='|'
		#the table header line
		tableheader = '|'
		for i in range(len(fieldlabels)) :
			dotline+='{0}|'.format(dotlinefields[i])
			tableheader+='{0:^{1}}|'.format(fieldlabels[i],len(dotlinefields[i]))
		#dash separator line to flank the table above/below
		dashesline = '-'*(sum([len(df) for df in dotlinefields])+len(fieldlabels)+1)
		#make the final list of lines to write to the file
		lines_to_write = ['FIT PARAMETERS:'] #first line is just a label haha
		lines_to_write.append(dashesline) #then the line of dashes
		lines_to_write.append(tableheader) #then the table header
		lines_to_write.append(dotline) #then the dot line separator
		for i in range(len(paramfields)) : #then the lines for the fit parameters
			newline='|'
			for j in range(len(paramfields[i])) :
				newline+='{0:^{1}}|'.format(paramfields[i][j],len(dotlinefields[j]))
			lines_to_write.append(newline)
			lines_to_write.append(dotline)
		lines_to_write.append(dashesline) #last another dashes line to close out the table
		#write all lines to the file
		with open(outputfilename,'w') as fp :
			for line in lines_to_write :
				fp.write(line+'\n')

	#set the lamdba residuals function and its arguments
	def _set_resid_function_and_args_(self) :
		if self._config.fit_type()=='linear_least_squares' :
			print('		Function to minimize is unweighted y-distance')
			self._resid_function = lambda p, x, y : self._fit_function(p,x)-y
			self._resid_function_args = ( self._data.xArray(),
										  self._data.yArray() ) 
		elif self._config.fit_type() in ['linear_least_squares_y_weighted',
										 'linear_least_squares_weighted'] :
			print('		Function to minimize is weighted y-distance')
			self._resid_function = lambda p, x, y, w : w*(self._fit_function(p,x)-y)
			self._resid_function_args = ( self._data.xArray(),
										  self._data.yArray(),
										  self._data.weightArray() ) 

	#set the lambda fit function and its arguments
	def _set_fit_function_and_params_(self) :
		if self._config.fit_type().startswith('linear_least_squares') :
			print('		Fit function is linear (y=mx+b)')
			self._fit_function = lambda p, x : p[0]*x+p[1]
			self._initial_parameters_list = self._parameters.prefitValueList()

	#populate the list of parameters from the config
	def _make_parameterlist_from_config_and_data_(self) :
		#all the linear least squares fits just have m and b (slope/intercept)
		if self._config.fit_type().startswith('linear_least_squares') :
			#find the initial guesses for the slope/intercept
			firstpoint = self._data.firstpoint()
			lastpoint  = self._data.lastpoint()
			rise = lastpoint.y()-firstpoint.y()
			run  = lastpoint.x()-firstpoint.x()
			init_slope=1
			if run!=0. :
				init_slope = rise/run
			self._parameters.addFitParameter('slope','m',init_slope)
			init_intercept=0.
			self._parameters.addFitParameter('intercept','b',init_intercept)

	#populate the data object for the fit depending on the config/data
	def _populate_data_object_from_config_(self) :
		if self._config.fit_type()=='linear_least_squares' :
			print('		Found x-y data for a linear fit')
			self._data = LinearData(self._config.x_name(),self._config.x_unit(),
									self._config.y_name(),self._config.y_unit(),
									self._config.n_points(),
									self._config.x_values(),self._config.y_values())
		elif self._config.fit_type()=='linear_least_squares_y_weighted' :
			print('		Found x-y data for a linear fit with weighted y errors')
			self._data = LinearDataYErrors(self._config.x_name(),self._config.x_unit(),
										   self._config.y_name(),self._config.y_unit(),
										   self._config.n_points(),
										   self._config.x_values(),self._config.y_values(),
										   self._config.y_uncertainties())
		elif self._config.fit_type()=='linear_least_squares_weighted' :
			print('		Found x-y data for a linear fit with weighted x-y errors')
			self._data = LinearDataXYErrors(self._config.x_name(),self._config.x_unit(),
											self._config.y_name(),self._config.y_unit(),
											self._config.n_points(),
											self._config.x_values(),self._config.y_values(),
											self._config.x_uncertainties(),
											self._config.y_uncertainties())
