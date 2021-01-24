import numpy as np
import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import dateutil, datetime


class Enedis_analyse():

    def __init__(self, filename):
        self.filename = filename 
        self.read_csv()
        self.get_time_cons()
        self.plots()


    def read_csv(self):
        ''' read and make self.data = list of ['data_time', 'cons'] '''
        data = [] 
        f = open(self.filename, 'r')
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            data.append(row)
        f.close()
        # rm header:
        self.data = data[16:]


    def get_time_cons(self):
        time_posix = []
        time_midnight = []
        time_parser = []
        time_str = [data[0] for data in self.data]
        for t in time_str:
            tparse = dateutil.parser.parse(t)
            time_parser = np.append(time_parser, tparse)
            time_posix.append(tparse.timestamp())
            print(time_posix[-1], t)
            # get midnights:
            if tparse.hour == 0 and tparse.minute == 0:
                time_midnight.append(tparse.timestamp())
                print(f'* {time_posix[-1]}')
        self.time_parser = time_parser
        self.time_posix = time_posix
        self.time_midnight = time_midnight
        self.time_str = time_str
        # consumation:
        self.cons = [int(data[1]) if data[1]!='' else None for data in self.data]

    
    def make_day_dic(self, c0=0, c1=-1):
        ''' make day_dic = d['h.m']=cons  '''
        # init day_dic:
        day_dic = {}
        for h in range(24):
            for m in [0,30]:
                day_dic[f'{h}.{m}'] = []
        # fill day_dic:
        for dat in self.data[c0:c1]: 
            hour = dateutil.parser.parse(dat[0]).hour
            minute = dateutil.parser.parse(dat[0]).minute
            day_dic[f'{hour}.{minute}'].append(int(dat[1]) if dat[1] else np.nan)
        self.day_dic = day_dic 
        # make day_avg from day_dic:
        day_avg = {}
        day_med = {}
        for k in day_dic:
            day_avg[k] = np.nanmean(day_dic[k])
            day_med[k] = np.nanmedian(day_dic[k])
        self.day_avg = day_avg
        self.day_med = day_med
        # plots:
        self.plots(c0=c0, c1=c1)


    def plots(self, c0=0, c1=-1):
        # make xticklabels as date strings:
        formatter = FuncFormatter(lambda x_val, tick_pos: str(datetime.datetime.fromtimestamp(x_val).date()).replace('20','',1))
        fig1 = plt.figure('Enedis_analyse 1', clear=True)
        ax1 = fig1.add_subplot(311)
        ax1.plot(self.time_posix, self.cons, 'o', ms=1)
        ax1.plot(self.time_posix[c0:c1], self.cons[c0:c1], '.', ms=2, color='tab:orange')
        for time_midnight in self.time_midnight:
            ax1.axvline(time_midnight, alpha=0.2)
        ax1.xaxis.set_major_formatter(formatter)
        ax1.set_ylabel('Cons. (W)')
        ax1.grid(False)

        ax2 = fig1.add_subplot(312)
        ax2.plot(self.time_posix[c0:c1], self.cons[c0:c1], '-', ms=2, color='tab:orange')
        for time_midnight in self.time_midnight:
            ax2.axvline(time_midnight, alpha=0.1)
        ax2.set_xlim([self.time_posix[c0]-10000, self.time_posix[c1]])
        ax2.xaxis.set_major_formatter(formatter)
        ax2.set_ylabel('Cons. (W)')
        ax2.grid(False)

        ax3 = fig1.add_subplot(313)
        for k in self.day_dic:
            ax3.plot( np.repeat(float(k.replace('30', '50')), len(self.day_dic[k])), self.day_dic[k], '.', alpha=0.2, color='0.5')
        for k in self.day_avg:
            ax3.plot(float(k.replace('30', '50')), self.day_avg[k], 'o', color='tab:orange')
            ax3.plot(float(k.replace('30', '50')), self.day_med[k], '.', color='tab:red', alpha=0.8)
        ax3.set_xlabel('Hour')
        ax3.set_ylabel(r'$\langle$Cons.$\rangle$ (W)')
        fig1.tight_layout()



