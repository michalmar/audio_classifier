# Audio Classifier

This repo is based on paper **ICASSP 2018** https://arxiv.org/pdf/1711.01369.pdf 
"Knowledge Transfer From Weakly Labeled Audio Using Convolutional Neural Network For Sound Events And Scenes" Anurag Kumar, Maksim Khadkevich, Christian Fügen 
 -> forked from: https://github.com/anuragkr90/weak_feature_extractor

## Installation

install ffmpeg: https://pythonbasics.org/convert-mp3-to-wav/
install requirements

### RUN
1. convert MP3 to WAV 
`python convert_mp3_to_wav.py "../COVID-19-train-audio/not-covid19-coughs/PMID-16436200" cough`
`python convert_mp3_to_wav.py "../COVID-19-train-audio/not-covid19-coughs/PMID-32095775" cough`


1. [OPTIONAL] prepare sample data (other class) 

`wget https://mmadlbs.blob.core.windows.net/share/ambient.mp3`
`python convert_wav_to_slices_by_time.py ./tmp 2`

1. extract features `python feature_extract.py "./data" "./features/out.csv"` 


1. run classification ... so far manually