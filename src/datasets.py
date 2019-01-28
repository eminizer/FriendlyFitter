###################################################################################################
### This file contains the "Data" classes for the FriendlyFitter package. #########################
### copyright 2019/contact margaret.eminizer@gmail.com ############################################
###################################################################################################

#imports
import numpy as np

#Data classes

#LinearData class: x-y data that will be fit with a line
class LinearData(object) :

	def __init__(self,x_name,x_unit,y_name,y_unit,n_points,x_values,y_values) :
		#copy info over
		self._x_name = x_name
		self._x_unit = x_unit
		self._y_name = y_name
		self._y_unit = y_unit
		self._n_points = n_points
		#start with a list of datapoints holding just the values
		self._data_points = []
		self._initialize_data_point_values_(x_values,y_values)

	def firstpoint(self) :
		return self._data_points[0]
	def lastpoint(self) :
		return self._data_points[self._n_points-1]
	def n_points(self) :
		return self._n_points
	def xArray(self) :
		return np.array([dp.x() for dp in self._data_points])
	def yArray(self) :
		return np.array([dp.y() for dp in self._data_points])
	def xErrArray(self) :
		return np.array([dp.xunc() for dp in self._data_points])
	def yErrArray(self) :
		return np.array([dp.yunc() for dp in self._data_points])
	def weightArray(self) :
		return np.array([dp.weight() for dp in self._data_points])
	def xMin(self) :
		return min([dp.x() for dp in self._data_points])
	def xMax(self) :
		return max([dp.x() for dp in self._data_points])
	def xAxisLabel(self) :
		return self._x_name+' ['+self._x_unit+']'
	def yAxisLabel(self) :
		return self._y_name+' ['+self._y_unit+']'

	#set the normalized weight for each datapoint
	def _set_datapoint_weights_(self) :
		unnormalized_weights = []
		for i in range(self._n_points) :
			#calculate total variance at each point by summing fractional x/y errors in quadrature
			x_var = (self._data_points[i].xunc()/self._data_points[i].x())**2
			y_var = (self._data_points[i].yunc()/self._data_points[i].y())**2
			#unnormalized weight is 1/variance if there are errors, or 1. otherwise
			if x_var!=0. or y_var!=0. :
				unnormalized_weights.append(1./(x_var+y_var))
			else :
				unnormalized_weights.append(1.)
		if unnormalized_weights.count(1.)==len(unnormalized_weights) :
			print('		Setting all datapoint weights equal')
		else :
			print('		Setting unique datapoint weights')
		#normalize by sum of weights and set datapoint weight
		sumunnormalizedweights=sum(unnormalized_weights)
		for i in range(self._n_points) :
			self._data_points[i].setWeight(unnormalized_weights[i]/sumunnormalizedweights)
	def _add_datapoint_x_errors_(self,x_uncertainties) :
		print('		Adding x uncertainties')
		for i in range(self._n_points) :
			self._data_points[i].setXUnc(x_uncertainties[i])
	def _add_datapoint_y_errors_(self,y_uncertainties) :
		print('		Adding y uncertainties')
		for i in range(self._n_points) :
			self._data_points[i].setYUnc(y_uncertainties[i])
	def _initialize_data_point_values_(self,x_values,y_values) :
		print('		Initializing a linear x-y dataset with '+str(self._n_points)+' values')
		for i in range(self._n_points) :
			self._data_points.append(DataPoint(i,x_values[i],y_values[i]))

#LinearData with Y Error bars
class LinearDataYErrors(LinearData) :

	def __init__(self,x_name,x_unit,y_name,y_unit,n_points,x_values,y_values,y_uncertainties) :
		LinearData.__init__(self,x_name,x_unit,y_name,y_unit,n_points,x_values,y_values)
		self._add_datapoint_y_errors_(y_uncertainties)
		self._set_datapoint_weights_()

#LinearData with X and Y error bars
class LinearDataXYErrors(LinearData) :

	def __init__(self,x_name,x_unit,y_name,y_unit,n_points,x_values,y_values,
				 x_uncertainties,y_uncertainties) :
		LinearData.__init__(self,x_name,x_unit,y_name,y_unit,n_points,x_values,y_values)
		self._add_datapoint_x_errors_(x_uncertainties)
		self._add_datapoint_y_errors_(y_uncertainties)
		self._set_datapoint_weights_()

#DataPoint class
class DataPoint(object) :

	def __init__(self,n,x,y,x_unc=0.,y_unc=0.,weight=1.) :
		self._n = n
		self._x = x
		self._y = y
		self._x_unc=x_unc
		self._y_unc=y_unc
		self._weight = weight
	def x(self) :
		return self._x
	def y(self) :
		return self._y
	def xunc(self) :
		return self._x_unc
	def yunc(self) :
		return self._y_unc
	def weight(self) :
		return self._weight
	def setXUnc(self,xunc) :
		self._x_unc=xunc
	def setYUnc(self,yunc) :
		self._y_unc=yunc
	def setWeight(self,weight) :
		self._weight = weight
