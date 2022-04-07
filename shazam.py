from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, 
    QAction, QFileDialog, QApplication,QMessageBox)
from PyQt5.QtCore import Qt    
from numpy import loadtxt
import numpy as np
import pyqtgraph as pg
from gui import *
from pydub import AudioSegment
from scipy.io import wavfile
import sounddevice as sd
import librosa
from librosa import display
import matplotlib.pyplot as plt
from PIL import Image
import imagehash
from imagehash import hex_to_hash
from matplotlib import pylab




class Shazam(Ui_MainWindow):
    def __init__(self,mainwindow):
        super(Shazam,self).setupUi(mainwindow)
        self.__plots=[self.song1_plot,self.song2_plot]
        self.__spectograms=[0,0]
        self.__audios=[0,0,0]
        self.__audios_rates=[0,0]
        self.__labels=[self.song1_name,self.song2_name,self.result_name]
        self.__flags=[False,False,False]
        slider_ranges={"min":0,"max":100,"step":1,"value":50}
        self.slider.setMaximum(slider_ranges["max"])
        self.slider.setMinimum(slider_ranges["min"])
        self.slider.setValue(slider_ranges["value"])
        self.slider.setSingleStep(slider_ranges["step"])
        self.slider.valueChanged.connect(self.mix)
        self.song1_percent.setText('50%')
        self.song2_percent.setText('50%')
        self.open_song1.triggered.connect(lambda:self.open_song(0))
        self.open_song2.triggered.connect(lambda:self.open_song(1))
        self.play_song1.clicked.connect(lambda : self.play_song(0))
        self.play_song2.clicked.connect(lambda : self.play_song(1))
        self.play_result.clicked.connect(lambda : self.play_song(2))
        self.spectogram1.clicked.connect(lambda : self.spectrogram(0))
        self.spectogram2.clicked.connect(lambda : self.spectrogram(1))
        self.start_check.clicked.connect(self.hashing)

        self.table.setColumnWidth(1,300)

    def open_song(self,i):
        fname = QFileDialog.getOpenFileName(None, 'Open file', "D:\\DSP\\Dsp_task4","MP3 (*.MP3) mp3 (*.mp3) ")
        if fname[0]:
            if fname[0].endswith('.mp3'):
                songData= AudioSegment.from_mp3(fname[0])[0:60000]
                name=fname[0].split('/')[-1]
                name=name.split('.')[0]
                songData.export(name+'.wav',format='wav')
                self.__audios[i],self.__audios_rates[i] = librosa.load(name+'.wav',sr=None,mono=False,dtype=np.int16)
            else :
                self.errormsg = QMessageBox()
                self.errormsg.setWindowTitle("TYPE ERROR")
                self.errormsg.setText("Sorry,choose .MP3 song")
                self.errormsg.setStandardButtons(QMessageBox.Ok)
                self.errormsg.setIcon(QMessageBox.Critical)
                self.x = self.errormsg.exec_()    
            if type(self.__audios[i])==np.ndarray:
                self.__audios[i]=self.__audios[i][0,:]      
            self.__flags[i]=True
            x=fname[0].split('/')
            self.__labels[i].setText(x[-1])
            data=np.abs(np.fft.rfft(self.__audios[i]))/len(self.__audios[i])
            self.__plots[i].plotItem.plot(data)
            self.__spectograms[i]= librosa.amplitude_to_db(np.abs(librosa.stft(self.__audios[i].astype(np.float32))), ref=np.max)
        
    def spectrogram(self,i): 
        plt.close()
        librosa.display.specshow(self.__spectograms[i], y_axis='linear')
        plt.colorbar(format='%+2.0f dB')
        plt.title(self.__labels[i].text()+' spectrogram')
        plt.tight_layout()
        plt.show()

    def hashing(self):
     if self.__flags[0] and self.__flags[1]:  
        compare_list=[]
        text=str(self.comboBox_2.currentText())
        text2=str(self.comboBox.currentText())
        print(text2)
        self.mix() 
        pylab.axis('off') # no axis
        pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])
        
        if text == "spectrogram":
            spec=librosa.amplitude_to_db(np.abs(librosa.stft(self.__audios[2].astype(np.float32))), ref=np.max)
            librosa.display.specshow(spec, y_axis='linear')
            file=open("spectrogram.text",'r')
        elif text =="mfccs":
            y_harmonic, y_percussive = librosa.effects.hpss(self.__audios[2].astype(np.float32))
            spec = librosa.feature.mfcc(y=y_harmonic, sr=44100, n_mfcc=13)
            librosa.display.specshow(spec, x_axis='time')
            file=open("mfccs.text",'r')
        elif text =="rolloff":
            spec = librosa.feature.spectral_rolloff(y=self.__audios[2].astype(np.float32), sr=44100)
            plt.semilogy(spec.T)
            file=open("rolloff.text",'r')
        elif text=="centriod":
            spec = librosa.feature.spectral_centroid(y=self.__audios[2].astype(np.float32), sr=44100)
            plt.semilogy(spec.T)
            file=open("centriod.text",'r')
        elif text=="melspect":
            S = librosa.feature.melspectrogram(y=self.__audios[2].astype(np.float32), sr=44100, n_mels=128,fmax=8000)
            spec= librosa.power_to_db(S, ref=np.max)
            librosa.display.specshow(spec, x_axis='time',y_axis='mel', sr=44100,fmax=8000)
            file=open("melspect.text",'r')
        
        pylab.savefig('mix'+'.png', bbox_inches=None, pad_inches=0)
        phash1=imagehash.phash(Image.open('mix.png'))
        
        if text2 != "None":
            if text2 == "spectrogram":
                spec=librosa.amplitude_to_db(np.abs(librosa.stft(self.__audios[2].astype(np.float32))), ref=np.max)
                librosa.display.specshow(spec, y_axis='linear')
                file=open("spectrogram.text",'r')
            elif text2 =="mfccs":
                y_harmonic, y_percussive = librosa.effects.hpss(self.__audios[2].astype(np.float32))
                spec = librosa.feature.mfcc(y=y_harmonic, sr=44100, n_mfcc=13)
                librosa.display.specshow(spec, x_axis='time')
                file=open("mfccs.text",'r')
            elif text2 =="rolloff":
                spec = librosa.feature.spectral_rolloff(y=self.__audios[2].astype(np.float32), sr=44100)
                plt.semilogy(spec.T)
                file=open("rolloff.text",'r')
            elif text2=="centriod":
                spec = librosa.feature.spectral_centroid(y=self.__audios[2].astype(np.float32), sr=44100)
                plt.semilogy(spec.T)
                file=open("centriod.text",'r')
            elif text2=="melspect":
                S = librosa.feature.melspectrogram(y=self.__audios[2].astype(np.float32), sr=44100, n_mels=128,fmax=8000)
                spec= librosa.power_to_db(S, ref=np.max)
                librosa.display.specshow(spec, x_axis='time',y_axis='mel', sr=44100,fmax=8000)
                file=open("melspect.text",'r')
            
            pylab.savefig('mix1'+'.png', bbox_inches=None, pad_inches=0)
            pylab.close()
            phash2=imagehash.phash(Image.open('mix1.png'))
            hash_list=file.readlines()            
            for i in range(0,len(hash_list),2):
                name=hash_list[i]
                Hash=hex_to_hash(hash_list[i+1])
                compare_list.append([name,.5*(phash1-Hash)+.5*(phash2-Hash)])
        else:
            hash_list=file.readlines()            
            for i in range(0,len(hash_list),2):
                name=hash_list[i]
                Hash=hex_to_hash(hash_list[i+1])
                compare_list.append([name,phash1-Hash])


        compare_list.sort(key=lambda val : val[1])
        self.table.clearContents()
        for i in range(10):   
         self.table.insertRow(i)
         item1 = QtWidgets.QTableWidgetItem(str(compare_list[i][1]))
         item1.setFlags(Qt.ItemIsSelectable |  Qt.ItemIsEnabled )
         self.table.setItem(i,0,item1)
         item2 = QtWidgets.QTableWidgetItem(compare_list[i][0])
         item2.setFlags(Qt.ItemIsSelectable |  Qt.ItemIsEnabled ) 
         self.table.setItem(i,1,item2)
         
    def play_song(self,i):
       if self.__flags[i]: 
        sd.stop()
        sd.play(self.__audios[i])

    def mix(self):
     sd.stop()
     if self.__flags[0] and self.__flags[1]:   
        value=self.slider.value()
        self.song1_percent.setText(str(value)+'%')
        self.song2_percent.setText(str(100-value)+'%')
        self.__audios[2]=self.__audios[0]*(float(value)/100.0)+self.__audios[1]*(float(100-value)/100.0)
        self.__audios[2]=self.__audios[2].astype(type(self.__audios[0][0])) 
        self.__flags[2]=True
        self.result_name.setText("you can listen now")
        
if __name__=="__main__":
    import sys
    app=QtWidgets.QApplication(sys.argv)
    MainWindow=QtWidgets.QMainWindow()
    ui=Shazam(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


