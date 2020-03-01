# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 23:57:15 2020

@author: kinga
"""

import sys

import numpy as np
import matplotlib.pyplot as plt
import librosa
from librosa import display

def show_wav(wav_file):
    '''
    Visualize an STFT power spectrum
    '''
    
    y, sr = librosa.load(wav_file)
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    
    plt.figure(figsize=(12,8))
    plt.subplot(4, 2, 1)
    display.specshow(D, y_axis='linear')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Linear-frequency power spectrogram')
    
    # Or on a logarithmic scale
    plt.subplot(4, 2, 2)
    display.specshow(D, y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Log-frequency power spectrogram')    

    # Or use a CQT scale
    CQT = librosa.amplitude_to_db(np.abs(librosa.cqt(y, sr=sr)), ref=np.max)
    plt.subplot(4, 2, 3)
    display.specshow(CQT, y_axis='cqt_note')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Constant-Q power spectrogram (note)')

    plt.subplot(4, 2, 4)
    display.specshow(CQT, y_axis='cqt_hz')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Constant-Q power spectrogram (Hz)')
    
    # Draw a chromagram with pitch classes
    C = librosa.feature.chroma_cqt(y=y, sr=sr)
    plt.subplot(4, 2, 5)
    display.specshow(C, y_axis='chroma')
    plt.colorbar()
    plt.title('Chromagram')

    # Force a grayscale colormap (white -> black)
    plt.subplot(4, 2, 6)
    display.specshow(D, cmap='gray_r', y_axis='linear')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Linear power spectrogram (grayscale)')

    # Draw time markers automatically
    plt.subplot(4, 2, 7)
    display.specshow(D, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Log power spectrogram')

    # Draw a tempogram with BPM markers
    plt.subplot(4, 2, 8)
    Tgram = librosa.feature.tempogram(y=y, sr=sr)
    display.specshow(Tgram, x_axis='time', y_axis='tempo')
    plt.colorbar()
    plt.title('Tempogram')
    plt.tight_layout()
    plt.show()
    
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError(' You need to give wave file to be display')
    
    show_wav(sys.argv[1])
   
    
    