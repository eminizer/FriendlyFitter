###################################################################################################
### This file contains the Parameter class for the FriendlyFitter package. ########################
### copyright 2019/contact margaret.eminizer@gmail.com ############################################
###################################################################################################

#imports
import numpy as np

#Parameter classes 
class Parameter(object) :

	def __init__(self,shortname) :
		self._shortname=shortname

	def shortname(self) :
		return self._shortname
		
#FitParameters are minimized in the fit
class FitParameter(Parameter) :

	def __init__(self,fullname,shortname,init_value) :
		print('		Adding fit parameter "'+fullname+'" ("'+shortname+
			  '") with initial value '+str(init_value))
		Parameter.__init__(self,shortname)
		self._fullname = fullname
		self._init_value = init_value
		self._best_fit_value = 0.
		self._postfit_error = 0.

	def fullname(self) :
		return self._fullname
	def init_value(self) :
		return self._init_value
	def best_fit_value(self) :
		return self._best_fit_value
	def getPrintFields(self) :
		returnlist = []
		returnlist.append(self._fullname)
		returnlist.append(self._shortname)
		returnlist.append('{0:e}'.format(self._init_value))
		returnlist.append('{0:e}'.format(self._best_fit_value))
		returnlist.append('{0:e}'.format(self._postfit_error))
		return returnlist
	def setPostfitValueAndError(self,val,err) :
		print('		Fit parameter "'+self._fullname+'" ("'+self._shortname+
			  '") postfit value = '+str(val)+' +/- '+str(err))
		self._best_fit_value = val
		self._postfit_error = err

#ParameterList class 
class ParameterList(object) :

	def __init__(self) :
		self._dict = {}
		self._list = []

	def addFitParameter(self,fullname,shortname,init_value) :
		if shortname in self._dict :
			print('ERROR: a parameter with shortname '+shortname+' has already been defined!!')
			exit()
		self._dict[shortname] = FitParameter(fullname,shortname,init_value)
		self._list.append(self._dict[shortname])
	def prefitValueList(self) :
		return [p.init_value() for p in self._list if isinstance(p,FitParameter)]
	def bestFitValueList(self) :
		return [p.best_fit_value() for p in self._list if isinstance(p,FitParameter)]
	def setParametersPostfit(self,pvalues,perrors) :
		if len(pvalues)!=len(perrors) or len(pvalues)!=len(self._list) :
			print('ERROR: mismatched numbers of parameters pre to post fit!!')
			exit()
		for i in range(len(self._list)) :
			self._list[i].setPostfitValueAndError(pvalues[i],perrors[i])
	def getFitParamPrintFieldsList(self) :
		returnlist = []
		for i in range(len(self._list)) :
			thisparam=self._list[i]
			if not isinstance(thisparam,FitParameter) :
				continue
			newparamfields = [str(i)]+thisparam.getPrintFields()
			returnlist.append(newparamfields)
		return returnlist
