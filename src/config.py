###################################################################################################
### This file contains the Config class for the FriendlyFitter package. ###########################
### copyright 2019/contact margaret.eminizer@gmail.com ############################################
###################################################################################################

#imports

#constants
KW_FORMATS = {}
KW_FORMATS['x_y_defs'] = ['## x name ##','## x units ##','## y name ##','## y units ##']
KW_FORMATS['x_y_data_block'] = ['## x values ##','## x uncertainties ##',
								'## y values ##','## y uncertainties ##']

#Config class
class Config(object) :

	#initialize from path to input file
	def __init__(self,inputfilepath,fit_type_override=None) :
		#set all configuration possibilities to None to start
		self._x_name,self._x_unit,self._y_name,self._y_unit = None,None,None,None
		self._x_values,self._x_uncertainties=None,None
		self._y_values,self._y_uncertainties=None,None
		self._n_points=None
		self._fit_type=fit_type_override
		#get the lines relevant to the fit stuff from the input file
		fitterlines = get_fitter_lines_from_filepath(inputfilepath)
		#make the dictionary of keyword lines
		keywordlinesdict = get_keyword_dict_from_fitter_lines(fitterlines)
		#set configuration from the keywordlines dictionary
		self._set_configuration_from_keyword_lines_dict_(keywordlinesdict)
		if self._fit_type==None : #set fit type automatically if not already done
			self._set_fit_type_automatically_()

	#public functions
	def x_name(self) :
		return self._x_name
	def x_unit(self) :
		return self._x_unit
	def y_name(self) :
		return self._y_name
	def y_unit(self) :
		return self._y_unit
	def x_values(self) :
		return self._x_values
	def x_uncertainties(self) :
		return self._x_uncertainties
	def y_values(self) :
		return self._y_values
	def y_uncertainties(self) :
		return self._y_uncertainties	
	def n_points(self) :
		return self._n_points
	def fit_type(self) :
		return self._fit_type

	#private functions
	#to set the type of fit that will be done automatically
	def _set_fit_type_automatically_(self) :
		#first check if there's a linear regression possible (need x/y dataset)
		if self._n_points==None :
			print('ERROR: did not find any datapoints to fit in input file!')
			exit()
		if ( self._y_values!=None and self._x_values!=None and 
			 len(self._x_values)==self._n_points and len(self._y_values)==self._n_points ) :
			#if there are the same number of x and y datapoints, check which errors we have
			if self._x_uncertainties==None and self._y_uncertainties==None :
				#if there are no errors it's just linear least squares
				self._fit_type='linear_least_squares'
			if self._y_uncertainties!=None and len(self._y_uncertainties)==self._n_points :
				#if every datapoint has a y uncertainty, it's y-weighted linear least squares
				self._fit_type='linear_least_squares_y_weighted'
			if ( self._x_uncertainties!=None and len(self._x_uncertainties)==self._n_points and 
				 self._y_uncertainties!=None and len(self._y_uncertainties)==self._n_points ) :
				#if every datapoint has x and y uncertainties, it's weighted linear least squares
				self._fit_type='linear_least_squares_weighted'

	#to set the configuration from the dictionary of keyword lines
	def _set_configuration_from_keyword_lines_dict_(self,keywordlinesdict) :
		#set x and y variable names and units
		if 'x_y_defs' in keywordlinesdict :
			[self._x_name,self._x_unit,self._y_name,self._y_unit] = keywordlinesdict['x_y_defs']
		#set x and y value/uncertainty arrays and number of points
		if 'x_y_data_block' in keywordlinesdict :
			self._x_values = [e[0] for e in keywordlinesdict['x_y_data_block']]
			self._x_uncertainties = [e[1] for e in keywordlinesdict['x_y_data_block']]
			if self._x_uncertainties.count(0.)==len(self._x_uncertainties) :
				print('INFO: all x uncertainties set to 0; will ignore x uncertainties.')
				self._x_uncertainties=None
			self._y_values = [e[2] for e in keywordlinesdict['x_y_data_block']]
			self._y_uncertainties = [e[3] for e in keywordlinesdict['x_y_data_block']]
			if self._y_uncertainties.count(0.)==len(self._y_uncertainties) :
				print('INFO: all y uncertainties set to 0; will ignore y uncertainties.')
				self._y_uncertainties=None
			if self._x_uncertainties!=None and self._x_uncertainties.count(0.)>0 :
				print('WARNING: missing x uncertainties for one or more datapoints')
				print('         will ignore x errors.')
				self._x_uncertainties=None
			if self._y_uncertainties!=None and self._y_uncertainties.count(0.)>0 :
				print('WARNING: missing y uncertainties for one or more datapoints')
				print('         will ignore y errors.')
				self._y_uncertainties=None
			self._n_points = len(self._x_values)
			if ( (self._x_uncertainties!=None and len(self._x_uncertainties)!=self._n_points) or
				 len(self._y_values)!=self._n_points or
				 (self._y_uncertainties!=None and len(self._y_uncertainties)!=self._n_points) ) :
				print("ERROR: numbers of x,y points/uncertainties don't match!")
				print("       Does every line in the list of points have an x and y value?")
				exit()		

# file-scope functions
#returns dictionary of information from file indexed by keyword given list of fit-related lines
def get_keyword_dict_from_fitter_lines(fls) :
	#dictionary to return
	kwlinesdict = {}
	#loop over the fitterlines looking for keyword lines and populate the dictionary
	i=0; current_kw = ''
	while i < len(fls) :
		flsplit = fls[i].split(',')
		#if this line is a special keyword line
		if flsplit[0].startswith('##') :
			for kw,patternlist in KW_FORMATS.items() :
				if ( len(flsplit)>=len(patternlist) and 
					 [f.lower() for f in flsplit][:len(patternlist)]==patternlist ) :
					current_kw=kw
					if current_kw in kwlinesdict.keys() :
						print('ERROR: more than one %s line in input file!'%(kw))
						exit()
					break
		#x_y_defs just has the one line after it to copy verbatim
		elif current_kw=='x_y_defs' :
			kwlinesdict[current_kw]=flsplit[:len(KW_FORMATS[current_kw])]
			if ( len(kwlinesdict[current_kw])!=len(KW_FORMATS[current_kw]) or
				 kwlinesdict[current_kw].count('')!=0 or
				 [kwl.startswith('##') for kwl in kwlinesdict[current_kw]].count(True)!=0 ) :
				print('ERROR: x/y def keyword line %s is invalid!'%(kwlinesdict[current_kw]))
				exit()
			current_kw=''
		#x_y_data_block should have four floats added to it on each line
		elif current_kw=='x_y_data_block' :
			if current_kw not in kwlinesdict :
				kwlinesdict[current_kw]=[]
			newvalues = []
			for k in range(len(KW_FORMATS[current_kw])) :
				if flsplit[k]=='' : flsplit[k]=0.
				try :
					newvalues.append(float(flsplit[k]))
				except ValueError :
					print('ERROR: x/y data block line %s contains non-float value(s)!!'%(flsplit))
			kwlinesdict[current_kw].append(newvalues)
		i+=1
	return kwlinesdict

#returns list of fit-related lines in input csv file
def get_fitter_lines_from_filepath(ifp) :
	#open the input file and get its lines
	rawinputfilelines = [line.rstrip() for line in open(ifp,'r').readlines()]
	if len(rawinputfilelines)==1 and rawinputfilelines[0].count('\r')>0 :
		rawinputfilelines = rawinputfilelines[0].split('\r')
	#slice off the input lines up to the indicator line
	fitterlines = []; i=0
	for rifl in rawinputfilelines :
		riflsplit = rifl.split(',')
		if ( len(riflsplit)>=3 and 
			 len(riflsplit[0])==riflsplit[0].count('#') and 
			 riflsplit[1].lower()=='friendly fit input' and
			 len(riflsplit[2])==riflsplit[2].count('#') ) :
			fitterlines = [l for l in rawinputfilelines[i+1:] if l]
		else :
			i+=1
	return fitterlines