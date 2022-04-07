from matplotlib import pylab
from pylab import *
import glob
import numpy as np
from pydub import AudioSegment
from scipy.io import wavfile
import matplotlib.pyplot as plt
from scipy import signal
import librosa
from librosa import display
from hashlib import md5
from PIL import Image
import imagehash
from imagehash import hex_to_hash
from difflib import SequenceMatcher 


mypath='D:\DSP\Dsp_task4\\'
songs=glob.glob("*.MP3")


file1=open("spectrogram.text",'a+')
file2=open("mfccs.text",'a+')
file3=open("centriod.text",'a+')
file4=open("rolloff.text",'a+')
file5=open("melspect.text",'a+')
# for i in range(len(songs)):
#  name=songs[i].split('.')
#  name=name[0]
#  print("spectrogram",name)
#  songData= AudioSegment.from_mp3(mypath+songs[i])[0:60000]
#  songData.export(mypath+'wav files\\'+name+'.wav',format='wav')
#  y, sr = librosa.load(mypath+'wav files\\'+name+'.wav',
#                         sr=None,mono=False,dtype=np.int16)
#  y=y[0,:]                        
#  pylab.axis('off') # no axis
#  pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])
#  D = librosa.amplitude_to_db(np.abs(librosa.stft(y.astype(np.float32))), ref=np.max)
#  librosa.display.specshow(D, y_axis='linear')
#  pylab.savefig(mypath+'spectrograms\\'+name+'.png', bbox_inches=None, pad_inches=0)
#  pylab.close()
 
#  x=imagehash.phash(Image.open(mypath+'spectrograms\\'+name+'.png'))   
#  file1.writelines([name+"\n"+x.__str__()+"\n"])
 
# for i in range(len(songs)):
#  name=songs[i].split('.')
#  name=name[0]
#  print("mfccs",name)
#  y, sr = librosa.load(mypath+'wav files\\'+name+'.wav',
#                         sr=None,mono=False,dtype=np.int16)
#  y=y[0,:] 
#  pylab.axis('off') # no axis
#  pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[]) 
#  y_harmonic, y_percussive = librosa.effects.hpss(y.astype(np.float32))
#  mfccs = librosa.feature.mfcc(y=y_harmonic, sr=sr, n_mfcc=13)
#  librosa.display.specshow(mfccs, x_axis='time')
#  pylab.savefig(mypath+'spectrograms\\'+name+'_mfccs'+'.png', bbox_inches=None, pad_inches=0)
#  pylab.close()
 
#  x=imagehash.phash(Image.open(mypath+'spectrograms\\'+name+'_mfccs'+'.png'))   
#  file2.writelines([name+'_mfccs'+"\n"+x.__str__()+"\n"])   

for i in range(len(songs)):
 name=songs[i].split('.')
 name=name[0]
 print("centriod",name)
 y, sr = librosa.load(mypath+'wav files\\'+name+'.wav',
                        sr=None,mono=False,dtype=np.int16)
 y=y[0,:] 
 pylab.axis('off') # no axis
 pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[]) 
 cent = librosa.feature.spectral_centroid(y=y.astype(np.float32), sr=sr)
 plt.semilogy(cent.T)
 pylab.savefig(mypath+'spectrograms\\'+name+'_centriod'+'.png', bbox_inches=None, pad_inches=0)
 pylab.close()
 plt.close()
 x=imagehash.phash(Image.open(mypath+'spectrograms\\'+name+'_centriod'+'.png'))   
 file3.writelines([name+'_centriod'+"\n"+x.__str__()+"\n"])
    
for i in range(len(songs)):
 name=songs[i].split('.')
 name=name[0]
 print("melspect",name)
 
 y, sr = librosa.load(mypath+'wav files\\'+name+'.wav',
                        sr=None,mono=False,dtype=np.int16)
 y=y[0,:] 
 
 pylab.axis('off') # no axis
 pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])  
 
 S = librosa.feature.melspectrogram(y=y.astype(np.float32), sr=sr, n_mels=128,fmax=8000)
 S_dB = librosa.power_to_db(S, ref=np.max)
 librosa.display.specshow(S_dB, x_axis='time',y_axis='mel', sr=sr,fmax=8000)
 
 pylab.savefig(mypath+'spectrograms\\'+name+'_melspect'+'.png', bbox_inches=None, pad_inches=0)
 pylab.close()
 
 x=imagehash.phash(Image.open(mypath+'spectrograms\\'+name+'_melspect'+'.png'))   
 file5.writelines([name+'_melspect'+"\n"+x.__str__()+"\n"]) 

for i in range(len(songs)):
 name=songs[i].split('.')
 name=name[0]
 print("rolloff",name)
 y, sr = librosa.load(mypath+'wav files\\'+name+'.wav',
                        sr=None,mono=False,dtype=np.int16)
 y=y[0,:] 
 pylab.axis('off') # no axis
 pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])
 cent = librosa.feature.spectral_rolloff(y=y.astype(np.float32), sr=sr)
 plt.semilogy(cent.T)
 pylab.savefig(mypath+'spectrograms\\'+name+'_rolloff'+'.png', bbox_inches=None, pad_inches=0)
 pylab.close()
 plt.close()
 x=imagehash.phash(Image.open(mypath+'spectrograms\\'+name+'_rolloff'+'.png'))   
 file4.writelines([name+'_rolloff'+"\n"+x.__str__()+"\n"])

file1.close()
file2.close()
file3.close()
file4.close()
file5.close()

