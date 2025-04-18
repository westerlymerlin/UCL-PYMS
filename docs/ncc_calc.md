# Contents for: ncc_calc

* [ncc\_calc](#ncc_calc)
  * [os](#ncc_calc.os)
  * [glob](#ncc_calc.glob)
  * [csv](#ncc_calc.csv)
  * [datetime](#ncc_calc.datetime)
  * [numpy](#ncc_calc.numpy)
  * [stats](#ncc_calc.stats)
  * [settings](#ncc_calc.settings)
  * [writesettings](#ncc_calc.writesettings)
  * [HeResults](#ncc_calc.HeResults)
    * [\_\_init\_\_](#ncc_calc.HeResults.__init__)
    * [reset](#ncc_calc.HeResults.reset)
    * [readdirectory](#ncc_calc.HeResults.readdirectory)
    * [calculate\_blank\_all](#ncc_calc.HeResults.calculate_blank_all)
    * [set\_blank](#ncc_calc.HeResults.set_blank)
    * [blankcorrect](#ncc_calc.HeResults.blankcorrect)
    * [calculate\_estimated\_qbestfit](#ncc_calc.HeResults.calculate_estimated_qbestfit)
    * [calculate\_ncc](#ncc_calc.HeResults.calculate_ncc)
    * [write\_ncc\_file](#ncc_calc.HeResults.write_ncc_file)
    * [filegenerator](#ncc_calc.HeResults.filegenerator)
  * [singlefilereader](#ncc_calc.singlefilereader)
  * [linbestfit](#ncc_calc.linbestfit)
  * [ncc](#ncc_calc.ncc)

<a id="ncc_calc"></a>

# ncc\_calc

Ncc Calculator
Author: Gary Twinn

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
- `q_dep_factor`: The depletion factor for Q samples.
- `q_depletion_err`: The depletion error for Q samples.
- `s_dep_factor`: The depletion factor for S samples.
- `q_pipette_ncc`: The NCC value for the Q pipette.
- `q_pipette_err`: The error for the Q pipette NCC value.
- `s_pipette_ncc`: The NCC value for the S pipette.
- `s_offset`: The offset for S samples.
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
- `qs_he34corrratios`: The corrected HE34 ratios for the Q samples.
- `qs_he34corrstderrs`: The corrected HE34 standard errors for the Q samples.
- `qs_he34ratios`: The HE34 ratios for the Q samples.
- `qs_he34sterrs`: The HE34 standard errors for the Q samples.
- `qs_he3_shots`: The HE3 shots for the Q samples.
- `qs_he4nccs`: The NCC values for the Q samples.
- `qs_he4nccstderrs`: The NCC standard errors for the Q samples.
- `qs_qnumbers`: The Q numbers for the Q samples.

Methods:
- `reset()`: Resets the class.
- `readdirectory(filepath)`: Reads a directory for helium files.
- `calculate_blank_all()`: Calculates the mean of all line blanks.
- `set_blank(blank_mean, blank_sterr)`: Sets the blank values based on the mean and standard error
                                        of selected line blanks.
- `blankcorrect()`: Corrects the values for background helium levels based on the line blanks.
- `calculate_estimated_qbestfit(qshots, h3shots)`: Calculates the estimated value for a Q-Shut based
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

Reset class

<a id="ncc_calc.HeResults.readdirectory"></a>

#### readdirectory

```python
def readdirectory(filepath)
```

Read Directory for Helium Files

<a id="ncc_calc.HeResults.calculate_blank_all"></a>

#### calculate\_blank\_all

```python
def calculate_blank_all()
```

Calculate mean of all line blanks

<a id="ncc_calc.HeResults.set_blank"></a>

#### set\_blank

```python
def set_blank(blank_mean, blank_sterr)
```

Set blank values based on mean and stdev of selected

<a id="ncc_calc.HeResults.blankcorrect"></a>

#### blankcorrect

```python
def blankcorrect()
```

Correct values for background helium levels based on blanks

<a id="ncc_calc.HeResults.calculate_estimated_qbestfit"></a>

#### calculate\_estimated\_qbestfit

```python
def calculate_estimated_qbestfit(qshots, h3shots)
```

Calculate the estimated value for a Q-Shut based on depletion rates and Q number

<a id="ncc_calc.HeResults.calculate_ncc"></a>

#### calculate\_ncc

```python
def calculate_ncc()
```

Calculate the Ncc value

<a id="ncc_calc.HeResults.write_ncc_file"></a>

#### write\_ncc\_file

```python
def write_ncc_file()
```

Write ncc.csv file

<a id="ncc_calc.HeResults.filegenerator"></a>

#### filegenerator

```python
def filegenerator(filepath)
```

Generate a set of NCC values and write them to a file

<a id="ncc_calc.singlefilereader"></a>

#### singlefilereader

```python
def singlefilereader(filename)
```

Read an He file and calculate bestfit values for graphs

<a id="ncc_calc.linbestfit"></a>

#### linbestfit

```python
def linbestfit(sampletime, amu_1, amu_3, amu_4)
```

Calculate the best-fit value for t=0

<a id="ncc_calc.ncc"></a>

#### ncc

