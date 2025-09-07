"""
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
"""
import os
import glob
import csv
from datetime import datetime
import numpy
from scipy import stats
from app_control import settings, writesettings


class HeResults:
    """
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
    """
    def __init__(self):
        self.q_dep_factor = settings['Ncc']['q_dep_factor']
        self.q_depletion_err = settings['Ncc']['q_depletion_err']
        self.s_dep_factor = settings['Ncc']['s_dep_factor']
        self.q_pipette_ncc = settings['Ncc']['q_pipette_ncc']
        self.q_pipette_err = settings['Ncc']['q_pipette_err']
        self.q_offset = settings['Ncc']['q_offset']
        self.s_pipette_ncc = settings['Ncc']['s_pipette_ncc']
        self.s_offset = settings['Ncc']['s_offset']
        self.blanks_he34ratios = []
        self.blanks_he34sterrs = []
        self.blanks_mean = 0
        self.blanks_names = []
        self.blanks_sterr = 0
        self.files_dates = []
        self.files_descriptions = []
        self.files_he34corrratios = []
        self.files_he34corrstderrs = []
        self.files_he34ratios = []
        self.files_he34stderrs = []
        self.files_he3_shots = []
        self.files_he4nccs = []
        self.files_he4nccstderrs = []
        self.files_names = []
        self.files_qnumbers = []
        self.nccfilepath = ''
        self.qs_he34corrratios = []
        self.qs_he34corrstderrs = []
        self.qs_he34ratios = []
        self.qs_he34sterrs = []
        self.qs_he3_shots = []
        self.qs_he4nccs = []
        self.qs_he4nccstderrs = []
        self.qs_qnumbers = []

    def reset(self):
        """
        Resets all internal state variables of the object to their default initial values.
        """
        self.blanks_he34ratios = []
        self.blanks_he34sterrs = []
        self.blanks_mean = 0
        self.blanks_names = []
        self.blanks_sterr = 0
        self.files_dates = []
        self.files_descriptions = []
        self.files_he34corrratios = []
        self.files_he34corrstderrs = []
        self.files_he34ratios = []
        self.files_he34stderrs = []
        self.files_he3_shots = []
        self.files_he4nccs = []
        self.files_he4nccstderrs = []
        self.files_names = []
        self.files_qnumbers = []
        self.nccfilepath = ''
        self.qs_he34corrratios = []
        self.qs_he34corrstderrs = []
        self.qs_he34ratios = []
        self.qs_he34sterrs = []
        self.qs_he3_shots = []
        self.qs_he4nccs = []
        self.qs_he4nccstderrs = []
        self.qs_qnumbers = []

    def readdirectory(self, filepath):
        """
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
        """
        self.nccfilepath = filepath
        filelist = glob.glob(filepath + "**\\HE*R")
        settings['Ncc']['ncc_filepath'] = filepath
        for filename in filelist:
            self.files_names.append(os.path.basename(filename))
            self.files_he3_shots.append(int(os.path.basename(filename)[2:7]))
            self.files_dates.append(datetime.strftime(datetime.fromtimestamp(os.path.getmtime(filename)),
                                                      "%Y-%m-%d %H:%M:%S"))
            stime = []
            h1 = []
            he3 = []
            he4 = []
            with open(filename, 'r', encoding='utf-8') as hefile:
                read_data = csv.reader(hefile, delimiter='\t')
                for row in read_data:
                    if len(stime) == 0:
                        firstfield = row[0].split('@')
                        filedesc = firstfield[0]
                        self.files_descriptions.append(filedesc)
                        stime.append(firstfield[1])
                    else:
                        stime.append(row[0])
                    h1.append(row[1])
                    he3.append(float(row[2]))
                    he4.append(row[3])
            hefile.close()
            if len(stime) == 0:
                self.files_descriptions.append('Empty File')
            bestfit = linbestfit(stime, h1, he3, he4)
            self.files_he34ratios.append(bestfit[1])
            self.files_he34stderrs.append(bestfit[4])
            self.files_qnumbers.append(0)
            self.files_he34corrratios.append(0)
            self.files_he34corrstderrs.append(0)
            self.files_he4nccs.append(0)
            self.files_he4nccstderrs.append(0)
            if filedesc[0] == 'Q':
                self.qs_he3_shots.append(self.files_he3_shots[-1])
                self.qs_qnumbers.append(int(filedesc[1:]))
                self.qs_he34ratios.append(bestfit[1])
                self.qs_he34sterrs.append(bestfit[0])
                self.qs_he4nccs.append(0)
                self.qs_he34corrratios.append(0)
            if filedesc.lower() == 'lb' or filedesc.lower() == 'line blank':
                self.blanks_names.append(self.files_names[-1])
                self.blanks_he34ratios.append(bestfit[1])
                self.blanks_he34sterrs.append(bestfit[0])
        writesettings()

    def calculate_blank_all(self):
        """
        Calculates the mean and standard error for line blank 3He/4He ratios.

        This method computes the mean and standard error values for the given blank
        ratios and their corresponding standard errors, storing the results in the
        appropriate attributes.
        """
        self.blanks_mean = numpy.mean(self.blanks_he34ratios)
        self.blanks_sterr = numpy.mean(self.blanks_he34sterrs)

    def set_blank(self, blank_mean, blank_sterr):
        """
        Sets the blank mean and standard error values.

        This method allows setting the mean and standard error of line blanks, which
        are typically used for analytical or calibration purposes. These values
        will be stored within the instance for further calculations or reference.
        """
        self.blanks_mean = blank_mean
        self.blanks_sterr = blank_sterr

    def blankcorrect(self):
        """
        Adjusts provided helium-3 to helium-4 ratios by subtracting the mean of blank
        measurements and recalculates their standard errors.

        Modifies the lists of ratios and standard errors for both files and Q-Standards
        by correcting them with respect to the mean of the blank measurements.
        """
        for i in range(len(self.files_names)):
            self.files_he34corrratios[i] = self.files_he34ratios[i] - self.blanks_mean
            self.files_he34corrstderrs[i] = pow((pow(self.blanks_sterr, 2) + pow(self.files_he34stderrs[i], 2)), 0.5)
        for i in range(len(self.qs_qnumbers)):
            self.qs_he34corrratios[i] = self.qs_he34ratios[i] - self.blanks_mean

    def calculate_estimated_qbestfit(self, qshots, h3shots):
        """
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
        """
        h3ncc = self.s_pipette_ncc * pow(self.s_dep_factor, (h3shots - self.s_offset))
        qncc = self.q_pipette_ncc * pow(self.q_dep_factor, (qshots - self.q_offset))
        return (qncc/h3ncc) * 1000

    def calculate_ncc(self):
        """
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
        """
        q_to_use = 0  # used to determin which q-standard withn the directory to use (there may be more than one in a run)
        for i in range(len(self.files_names)):
            if q_to_use < len(self.qs_qnumbers) - 1:
                if self.files_he3_shots[i] >= self.qs_he3_shots[q_to_use+1]:
                    q_to_use += 1
            self.files_qnumbers[i] = self.qs_qnumbers[q_to_use]
            self.files_he4nccs[i] = (self.q_pipette_ncc * pow(self.q_dep_factor, self.qs_qnumbers[q_to_use] - self.q_offset)
                                     * (self.files_he34corrratios[i] / self.qs_he34corrratios[q_to_use])
                                     (self.files_he34corrratios[i] / self.qs_he34corrratios[q_to_use]))
            self.files_he4nccstderrs[i] = (self.files_he4nccs[i] *
                                           pow((pow((self.q_pipette_err / self.q_pipette_ncc), 2)) +
                                               pow((self.files_qnumbers[i] * self.q_depletion_err) /
                                                   (pow(self.q_dep_factor, self.files_qnumbers[i])), 2), 0.5))

    def write_ncc_file(self):
        """
        Writes the NCC (noble gas concentration) data to a CSV file.

        This method generates a CSV file named 'PyMS_ncc.csv' in the specified path,
        containing helium-related measurement information. The file includes columns
        such as filename, date, description, q-standard, 3He/4He ratio, and relevant
        statistical data.
        """
        csv_top_row = ('"filename","date","description","q-standard","3He/4He_ratio","3He/4He_ratio_error",'
                     '"3He/4He_blank_corrected_ratio","3He/4He_blank_corrected_error","ncc","ncc_err"')
        with open(self.nccfilepath + '\\PyMS_ncc.csv', 'w', newline='', encoding='utf-8') as hefile:
            print(csv_top_row, file=hefile)
            nccfile = csv.writer(hefile, delimiter=',')
            for i in range(len(self.files_names)):
                nccfile.writerow([self.files_names[i], self.files_dates[i], self.files_descriptions[i],
                                  self.files_qnumbers[i], self.files_he34ratios[i], self.files_he34stderrs[i],
                                  self.files_he34corrratios[i], self.files_he34corrstderrs[i], self.files_he4nccs[i],
                                  self.files_he4nccstderrs[i]])
        hefile.close()

    def filegenerator(self, filepath):
        """
        Generates and processes files based on specified operations.

        This method is responsible for managing a sequence of operations on a
        set of files provided through the specified file path. It includes
        reading directories, performing blank corrections, calculating normalized
        cross correlation (NCC), writing results, and finally resetting the
        state for subsequent operations.

        Args:
            filepath (str): Path to the directory or file to be processed.
        """
        self.readdirectory(filepath)
        self.calculate_blank_all()
        self.blankcorrect()
        self.calculate_ncc()
        self.write_ncc_file()
        self.reset()


def singlefilereader(filename):
    """
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
    """
    rows = []
    with open(filename, 'r', encoding='utf-8') as hefile:
        read_data = csv.reader(hefile, delimiter='\t')
        for row in read_data:
            rows.append(row)
    hefile.close()
    if len(rows) == 0:
        return [0], [0], [0], [0]
    firstfield = rows[0][0].split('@')
    rows[0][0] = firstfield[1]
    nt = len(rows)
    m1graph = []
    m3graph = []
    m4graph = []
    ratiograph = []
    position = 0
    for i in range(nt):
        if float(rows[i][0]) >= settings['Ncc']['ncc_start_seconds']:
            m1graph.append([float(rows[i][0]), float(rows[i][1])])
            m3graph.append([float(rows[i][0]), float(rows[i][2]) - float(rows[i][1]) * settings['Ncc']['HD_H']])
            m4graph.append([float(rows[i][0]), float(rows[i][3])])
            ratiograph.append([float(rows[i][0]), (m4graph[position][1]/m3graph[position][1]) * 1000])
            position = position + 1
    return m1graph, m3graph, m4graph, ratiograph


def linbestfit(sampletime, amu_1, amu_3, amu_4):
    """
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
    """
    st = []
    hd = []
    he3 = []
    he4_he3 = []
    position = 0
    try:
        for i in range(len(sampletime)):
            if float(sampletime[i]) >= settings['Ncc']['ncc_start_seconds']:
                st.append(float(sampletime[i]))
                hd.append(float(amu_1[i]) * settings['Ncc']['HD_H'])
                he3.append(float(amu_3[i]) - hd[position])
                he4_he3.append((float(amu_4[i]) / he3[position]) * 1000)
                position = position + 1
        return stats.linregress(st, he4_he3)
    except ValueError:
        return 0, 0, 0, 0, 0

ncc = HeResults()

if __name__ == '__main__':
    TEST_FILE_PATH = 'C:\\Users\\garyt\\SynologyDrive\\GTFiles\\PhD\\Samples'
    ncc.filegenerator(TEST_FILE_PATH)
