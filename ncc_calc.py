"""
Ncc Calculator
Author: Gary Twinn
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
    """
    def __init__(self):
        self.q_dep_factor = settings['Ncc']['q_dep_factor']
        self.q_depletion_err = settings['Ncc']['q_depletion_err']
        self.s_dep_factor = settings['Ncc']['s_dep_factor']
        self.q_pipette_ncc = settings['Ncc']['q_pipette_ncc']
        self.q_pipette_err = settings['Ncc']['q_pipette_err']
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
        """Reset class"""
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
        """Read Directory for Helium Files"""
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
        """Calculate mean of all line blanks"""
        self.blanks_mean = numpy.mean(self.blanks_he34ratios)
        self.blanks_sterr = numpy.mean(self.blanks_he34sterrs)

    def set_blank(self, blank_mean, blank_sterr):
        """Set blank values based on mean and stdev of selected"""
        self.blanks_mean = blank_mean
        self.blanks_sterr = blank_sterr

    def blankcorrect(self):
        """Correct values for background helium levels based on blanks"""
        for i in range(len(self.files_names)):
            self.files_he34corrratios[i] = self.files_he34ratios[i] - self.blanks_mean
            self.files_he34corrstderrs[i] = pow((pow(self.blanks_sterr, 2) + pow(self.files_he34stderrs[i], 2)), 0.5)
        for i in range(len(self.qs_qnumbers)):
            self.qs_he34corrratios[i] = self.qs_he34ratios[i] - self.blanks_mean

    def calculate_estimated_qbestfit(self, qshots, h3shots):
        """Calculate the estimated value for a Q-Shut based on depletion rates and Q number"""
        h3ncc = self.s_pipette_ncc * pow(self.s_dep_factor, (h3shots - self.s_offset))
        qncc = self.q_pipette_ncc * pow(self.q_dep_factor, qshots)
        return (qncc/h3ncc) * 1000

    def calculate_ncc(self):
        """Calculate the Ncc value"""
        qoffset = 0
        for i in range(len(self.files_names)):
            if qoffset < len(self.qs_qnumbers)-1:
                if self.files_he3_shots[i] >= self.qs_he3_shots[qoffset+1]:
                    qoffset += 1
            self.files_qnumbers[i] = self.qs_qnumbers[qoffset]
            self.files_he4nccs[i] = (self.q_pipette_ncc * pow(self.q_dep_factor, self.qs_qnumbers[qoffset]) *
                                     (self.files_he34corrratios[i] / self.qs_he34corrratios[qoffset]))
            self.files_he4nccstderrs[i] = (self.files_he4nccs[i] *
                                           pow((pow((self.q_pipette_err / self.q_pipette_ncc), 2)) +
                                               pow((self.files_qnumbers[i] * self.q_depletion_err) /
                                                   (pow(self.q_dep_factor, self.files_qnumbers[i])), 2), 0.5))

    def write_ncc_file(self):
        """Write ncc.csv file"""
        firstline = ('"filename","date","description","q-standard","3He/4He_ratio","3He/4He_ratio_error",'
                     '"3He/4He_blank_corrected_ratio","3He/4He_blank_corrected_error","ncc","ncc_err"')
        with open(self.nccfilepath + '\\PyMS_ncc.csv', 'w', newline='', encoding='utf-8') as hefile:
            print(firstline, file=hefile)
            nccfile = csv.writer(hefile, delimiter=',')
            for i in range(len(self.files_names)):
                nccfile.writerow([self.files_names[i], self.files_dates[i], self.files_descriptions[i],
                                  self.files_qnumbers[i], self.files_he34ratios[i], self.files_he34stderrs[i],
                                  self.files_he34corrratios[i], self.files_he34corrstderrs[i], self.files_he4nccs[i],
                                  self.files_he4nccstderrs[i]])
        hefile.close()

    def filegenerator(self, filepath):
        """Generate a set of NCC values and write them to a file"""
        self.readdirectory(filepath)
        self.calculate_blank_all()
        self.blankcorrect()
        self.calculate_ncc()
        self.write_ncc_file()
        self.reset()


def singlefilereader(filename):
    """Read an He file and calculate bestfit values for graphs"""
    rows = []
    with open(filename, 'r', encoding='utf-8') as hefile:
        read_data = csv.reader(hefile, delimiter='\t')
        for row in read_data:
            rows.append(row)
    hefile.close()
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
    """Calculate the best-fit value for t=0"""
    st = []
    hd = []
    he3 = []
    he4_he3 = []
    position = 0
    for i in range(len(sampletime)):
        if float(sampletime[i]) >= settings['Ncc']['ncc_start_seconds']:
            st.append(float(sampletime[i]))
            hd.append(float(amu_1[i]) * settings['Ncc']['HD_H'])
            he3.append(float(amu_3[i]) - hd[position])
            he4_he3.append((float(amu_4[i]) / he3[position]) * 1000)
            position = position + 1
    return stats.linregress(st, he4_he3)


ncc = HeResults()

if __name__ == '__main__':
    TEST_FILE_PATH = 'C:\\Users\\garyt\\OneDrive - TS Technologies Ltd\\GTFiles\\PhD\\Samples'
    ncc.filegenerator(TEST_FILE_PATH)
