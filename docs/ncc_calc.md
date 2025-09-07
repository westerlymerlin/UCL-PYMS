# None

<a id="ncc_calc"></a>

# ncc\_calc

Noble Gas Concentration Calculator (NCC) Module
Author: Gary Twinn

This module provides functionality for processing helium isotope measurement data and calculating
noble gas concentrations. It handles data file reading, blank correction, linear regression
analysis, and NCC (Nano Cubic Centimetre) calculation for mass spectrometry results.
e
Key Components:
- HeResults: Main class for processing helium isotope measurement data
- singlefilereader: Function for reading individual measurement files
- linbestfit: Linear regression analysis function

The module supports:
- Reading and parsing helium measurement data files
- Blank correction calculations
- Linear regression fitting for isotope ratios
- NCC (Noble Gas Concentration) calculations
- File output generation for processed results

<a id="ncc_calc.os"></a>

## os

<a id="ncc_calc.glob"></a>

## glob

<a id="ncc_calc.csv"></a>

## csv

<a id="ncc_calc.datetime"></a>

## datetime

<a id="ncc_calc.numpy"></a>

## numpy

<a id="ncc_calc.stats"></a>

## stats

<a id="ncc_calc.settings"></a>

## settings

<a id="ncc_calc.writesettings"></a>

## writesettings

<a id="ncc_calc.HeResults"></a>

## HeResults Objects

```python
class HeResults()
```

The `HeResults` class represents the helium results. It has various attributes and methods
to handle and process the results.

Attributes:
- `q_dep_factor`: The depletion factor for 4He (Q) Standard.
- `q_depletion_err`: The depletion error for 4He (Q) Standard.
- `s_dep_factor`: The depletion factor for 3He (spike) shots.
- `q_pipette_ncc`: The NCC value for the Q pipette.
- `q_pipette_err`: The error for the Q pipette NCC value.
- `s_pipette_ncc`: The NCC value for the S pipette.
- `s_offset`: The offset value for the 3He-pipette spike shots, used to account for lost 3He as determined during a depletion test
- `q_offset`: The offset value for the 4He-pipette standard shots, used to account for lost 4He as determined during a depletion test
- `blanks_he34ratios`: The HE34 ratios for the line blanks.
- `blanks_he34sterrs`: The HE34 standard errors for the line blanks.
- `blanks_mean`: The mean of all line blanks.
- `blanks_names`: The names of the line blanks.
- `blanks_sterr`: The standard error for the line blanks.
- `files_dates`: The dates of the files.
- `files_descriptions`: The descriptions of the files.
- `files_he34corrratios`: The corrected HE34 ratios for the files.
- `files_he34corrstderrs`: The corrected HE34 standard errors for the files.
- `files_he34ratios`: The HE34 ratios for the files.
- `files_he34stderrs`: The HE34 standard errors for the files.
- `files_he3_shots`: The HE3 shots for the files.
- `files_he4nccs`: The NCC values for the files.
- `files_he4nccstderrs`: The NCC standard errors for the files.
- `files_names`: The names of the files.
- `files_qnumbers`: The Q numbers for the files.
- `nccfilepath`: The filepath for the NCC files.
- `qs_he34corrratios`: The corrected HE34 ratios for the Q Shot.
- `qs_he34corrstderrs`: The corrected HE34 standard errors for the Q Shot.
- `qs_he34ratios`: The HE34 ratios for the Q Shot.
- `qs_he34sterrs`: The HE34 standard errors for the Q Standard.
- `qs_he3_shots`: The HE3 shots for the Q Standard.
- `qs_he4nccs`: The NCC values for the Q Standard.
- `qs_he4nccstderrs`: The NCC standard errors for the Q Standard.
- `qs_qnumbers`: The Q numbers for the Q Standard.

Methods:
- `reset()`: Resets the class.
- `readdirectory(filepath)`: Reads a directory for helium files.
- `calculate_blank_all()`: Calculates the mean of all line blanks.
- `set_blank(blank_mean, blank_sterr)`: Sets the blank values based on the mean and standard error
                                        of selected line blanks.
- `blankcorrect()`: Corrects the values for background helium levels based on the line blanks.
- `calculate_estimated_qbestfit(qshots, h3shots)`: Calculates the estimated value for a Q-Standard based
                                                   on depletion rates and Q number.
- `calculate_ncc()`: Calculates the NCC value.
- `write_ncc_file()`: Writes the NCC file.

<a id="ncc_calc.HeResults.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

<a id="ncc_calc.HeResults.reset"></a>

#### reset

```python
def reset()
```

Resets all internal state variables of the object to their default initial values.

<a id="ncc_calc.HeResults.readdirectory"></a>

#### readdirectory

```python
def readdirectory(filepath)
```

Reads and processes NCC files from a specified directory.

This method scans for files matching the pattern "HE*R" in the provided
directory and extracts specific data from them. It processes the HE3, HE4
data, timestamps, and other related metrics, such as HE3/HE4 ratios, using
linear best fit calculation. The processed data is then stored in the
attributes of the class instance.

The method also categorizes the processed files into Q (quantities) and blank
(Line Blank) files based on specific file descriptors. Results, such as HE3
shots, HE34 ratios, and other statistical measures, are stored accordingly for
further analysis or utilization.

Attributes Updated:
    files_names (list[str]): List of base filenames for the processed files.
    files_he3_shots (list[int]): List of shot values extracted for each file.
    files_dates (list[str]): List of timestamps when the files were last
        modified.
    files_descriptions (list[str]): List of descriptions extracted from
        filenames.
    files_he34ratios (list[float]): List of HE3/HE4 ratios calculated for each
        file.
    files_he34stderrs (list[float]): List of standard errors for HE3/HE4
        ratios.
    files_qnumbers (list[int]): List of Q-Standard Run numbers, defaulted to zero.
    files_he34corrratios (list[float]): List of corrected HE3/HE4 ratios,
        defaulted to zero.
    files_he34corrstderrs (list[float]): List of corrected standard errors for
        HE3/HE4 ratios.
    files_he4nccs (list[float]): List of HE4 NCC values, defaulted to zero.
    files_he4nccstderrs (list[float]): List of standard errors for HE4 NCC
        values.

    qs_he3_shots (list[int]): List of HE3 shots for Q files.
    qs_qnumbers (list[int]): List of quantity numbers for Q files.
    qs_he34ratios (list[float]): List of HE3/HE4 ratios for Q files.
    qs_he34sterrs (list[float]): List of standard errors for HE3/HE4 ratios in
        Q files.
    qs_he4nccs (list[float]): List of HE4 NCC values for Q files, defaulted to
        zero.
    qs_he34corrratios (list[float]): List of corrected HE3/HE4 ratios for Q
        files, defaulted to zero.

    blanks_names (list[str]): List of filenames for Line Blank files.
    blanks_he34ratios (list[float]): List of HE3/HE4 ratios for Line Blank
        files.
    blanks_he34sterrs (list[float]): List of standard errors for HE3/HE4
        ratios in Line Blank files.

<a id="ncc_calc.HeResults.calculate_blank_all"></a>

#### calculate\_blank\_all

```python
def calculate_blank_all()
```

Calculates the mean and standard error for line blank 3He/4He ratios.

This method computes the mean and standard error values for the given blank
ratios and their corresponding standard errors, storing the results in the
appropriate attributes.

<a id="ncc_calc.HeResults.set_blank"></a>

#### set\_blank

```python
def set_blank(blank_mean, blank_sterr)
```

Sets the blank mean and standard error values.

This method allows setting the mean and standard error of line blanks, which
are typically used for analytical or calibration purposes. These values
will be stored within the instance for further calculations or reference.

<a id="ncc_calc.HeResults.blankcorrect"></a>

#### blankcorrect

```python
def blankcorrect()
```

Adjusts provided helium-3 to helium-4 ratios by subtracting the mean of blank
measurements and recalculates their standard errors.

Modifies the lists of ratios and standard errors for both files and Q-Standards
by correcting them with respect to the mean of the blank measurements.

<a id="ncc_calc.HeResults.calculate_estimated_qbestfit"></a>

#### calculate\_estimated\_qbestfit

```python
def calculate_estimated_qbestfit(qshots, h3shots)
```

Calculates the estimated Q-best fit value based on Q-shots and H3-shots data.

This method computes the estimate of Q-best fit using provided Q-shots and
H3-shots values along with the internally defined scaling factors and offsets
for Q-pipette and 3He-pipette. It calculates the NCC (Nano Cubic Centimetres)
for both Q and H3 based on the respective parameters and then computes the ratio
scaled by a factor of 1000.

Parameters:
qshots (int): The number of Q-shots used so far, including the current one.
h3shots (int): The number of H3-shots used so far, including the current one
s_offset (int): The offset value for the 3He-pipette spike shots, used to account for lost 3He
    as determined during a depletion test
q_offset (int): The offset value for the 4He-pipette standard shots, used to account for lost 4He
    as determined during a depletion test
for the offsets: a poistive number indicates a loss of gas from the tank, a negative number that not as much
    helium as expected has been released

Returns:
float: The estimated Q-best fit value after calculating the corrections and ratio.

<a id="ncc_calc.HeResults.calculate_ncc"></a>

#### calculate\_ncc

```python
def calculate_ncc()
```

Calculates and assigns corrected Helium Gas Concentration in nano cubic centimetres (NCC) values and the
 standard errors for all the files in the directory and writes them to memory.

4HeSample = 4HeQstandard (4He/3He) * Spiked Sample / (4He/3He) Spiked Q-standard
    where:
     4HeSample is the NCC of helium extracted from the sample
     4HeQstandard is the amount of helium in ncc from the current Q shot calculated from:
                                            (Q pipette initial ncc) x (Q depletion factor ^ number of Q shots)
     Spiked Sample is the ratio of 3He/4He from the blank corrected 3He/4He ratio
     Spiked Q-standard is the ratio of 3He/4He from the blank corrected 3He/4He ratio from the current Q-Standard

This method iterates through file data to compute helium-4 normalized concentrations
and their associated errors based on predefined parameters, ratios, and correction factors.
The calculations incorporate adjustments for depletion effects and provide standardized
data for subsequent analysis.

<a id="ncc_calc.HeResults.write_ncc_file"></a>

#### write\_ncc\_file

```python
def write_ncc_file()
```

Writes the NCC (noble gas concentration) data to a CSV file.

This method generates a CSV file named 'PyMS_ncc.csv' in the specified path,
containing helium-related measurement information. The file includes columns
such as filename, date, description, q-standard, 3He/4He ratio, and relevant
statistical data.

<a id="ncc_calc.HeResults.filegenerator"></a>

#### filegenerator

```python
def filegenerator(filepath)
```

Generates and processes files based on specified operations.

This method is responsible for managing a sequence of operations on a
set of files provided through the specified file path. It includes
reading directories, performing blank corrections, calculating normalized
cross correlation (NCC), writing results, and finally resetting the
state for subsequent operations.

Args:
    filepath (str): Path to the directory or file to be processed.

<a id="ncc_calc.singlefilereader"></a>

#### singlefilereader

```python
def singlefilereader(filename)
```

Reads a single file and processes its data to extract specific graphs based on provided settings. The function parses a
tab-delimited file, processes its rows, and returns processed data in the form of several graphs. These graphs include
m1graph, m3graph, m4graph, and ratiograph. Each graph is a list of paired float values.

Parameters:
filename: str
    The name of the file to be read.

Returns:
tuple
    A tuple containing four lists (m1graph, m3graph, m4graph, ratiograph). Each list includes a series of paired float
    values extracted and computed from the file.

<a id="ncc_calc.linbestfit"></a>

#### linbestfit

```python
def linbestfit(sampletime, amu_1, amu_3, amu_4)
```

Fits a linear regression to the sample data and calculates relevant ratios.

This function processes measurement data to determine values needed for a linear
regression analysis. It filters the data based on a specified time threshold and
computes helium isotope ratios, storing them in lists for analysis. Using Scipy's
linear regression method, it calculates and returns the regression results.

Parameters:
sampletime : list[float]
    A list of sample times in seconds. The times are used to filter data for
    inclusion in the regression analysis.
amu_1 : list[float]
    A list of measurements corresponding to AMU 1, used to compute hd values.
amu_3 : list[float]
    A list of measurements corresponding to AMU 3, used to calculate helium-3
    values after subtracting calculated hd values.
amu_4 : list[float]
    A list of measurements corresponding to AMU 4, used to determine the ratio
    of helium-4 to helium-3.

Returns:
tuple[float, float, float, float, float]
    Returns a tuple containing the slope, intercept, r-value, p-value, and
    standard error of the linear regression. If an error occurs during the
    calculation (e.g., invalid data), a tuple of zeros is returned.

Raises:
ValueError
    If an invalid value is encountered during processing.

<a id="ncc_calc.ncc"></a>

#### ncc

