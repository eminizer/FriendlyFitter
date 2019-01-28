# Introduction

This project is a lightweight, user-friendly fitting package developed for use in the Advanced Lab class taken by most physics students at Johns Hopkins University. 

# Installation

The project relies on the numpy, scipy, and matplotlib packages. In other words, in order to make sure you can run the program, open up python in a terminal and type:

```python
import numpy
import scipy
import matplotlib
```

If that doesn't crash you should be good. To get this code you can either download or clone the respository.

## How I installed everything on Mac OSX

Probably the easiest way to get everything needed is to use pip, which comes with new installations of python. To set up on my system I installed python3 through [homebrew](https://brew.sh/) (click link for simple installation instructions) and then installed the necessary packages with the included pip3:

```
brew install python3
pip3 install numpy
pip3 install scipy
pip3 install matplotlib
```

# Running Fits

Running the different fits is configured through an input .csv file that has a section specifically syntaxed to interface with the FriendlyFitter project. This way you can add a specially-formatted block at the end of your regular data-taking spreadsheet, save it as a .csv, and run it through the FriendlyFitter with the resulting output stored in a new file. 

To run the FriendlyFitter from the command line with the example input file, open up a terminal, cd to this project's 'test' directory, and type:

```
python ../src/run_fitter.py -I speed_of_light_example_input.csv
```

This will produce an output .txt file listing the prefit/postfit parameter values with uncertainties, and a simple plot of the fit in .png form.

## Input file lines common to all fit methods

Some lines in the .csv input file don't depend on the type of fit you want to run. Generally if a line starts with at least two hashes ("##") the code will recognize that as a specially-formatted line.

### The FriendlyFitter indicator line (mandatory)

The specially-formatted block in your .csv begins with three cells on a single line; one cell reading "friendly fit input" in between two cells including only hashes, something like:

| ##### | friendly fit input | ##### |
| ----- | ------------------ | ----- |

in your spreadsheet. Everything in the file before that line will be ignored, and the code will try to configure a fit from the lines after it in the file, some of which are also specially-formatted depending on the type of fit you want to perform

## Linear Least Squares

This algorithm fits a set of x and y datapoints (possibly including uncertainties) with a line and reports the best-fit line's slope and intercept. The included speed of light data example is a fit of this type. If the datapoints you put in have uncertainties associated with them the fit will weight each datapoint according to its uncertainty.

### Input file parameters

There are two sections needed in your input file to run a linear least squares fit. The first section is two lines long and defines the variables standing in for your x and y. It will set the axes on the plot that gets made, and It looks like this in your spreadsheet:

| ## x name ## | ## x units ## | ## y name ## | ## y units ## |
| ------------ | ------------- | ------------ | ------------- |
| x variable name | x units | y variable name | y units |

The fields in this line will just be put together to make the legend on the plot; they can be any string.

The other section needed to run a linear least squares fit is your data. It will look like this in your spreadsheet:

| ## x values ## | ## x uncertainties ## | ## y values ## | ## y uncertainties ## |
| --- | --- | --- | --- |
| first x value | first x uncertainty | first y value | first y uncertainty |
| second x value | second x uncertainty | second y value | second y uncertainty |
| ... | ... | ... | ... |

The values you put in should be numbers. You can also fill one or both of the "uncertainties" columns with zeroes or leave them empty if the datapoints you're fitting don't have associated uncertainties. The number of rows below the indicator line is the number of datapoints.

