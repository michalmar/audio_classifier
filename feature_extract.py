import sys
import os
from collections import OrderedDict

import numpy as np
import pandas as pd
import librosa as lib

import torch.nn.functional as Fx
import torch
from torch.autograd import Variable

import weak_network as wnet
import extractor as exm


usegpu = False


n_fft = 1024
hop_length = 512
n_mels = 128
trainType = 'weak_mxh64_1024'
pre_model_path = 'mx-h64-1024_0d3-1.17.pkl'
featType = 'layer18' # or layer 19 -  layer19 might not work well
globalpoolfn = Fx.avg_pool2d # can use max also
netwrkgpl = Fx.avg_pool2d # keep it fixed



def load_model(netx,modpath):
    #load through cpu -- safest
    state_dict = torch.load(modpath, map_location=lambda storage, loc: storage)
    new_state_dict = OrderedDict()
    for k, v in state_dict.items():
        if 'module.' in k:
            name = k[7:]
        else:
            name = k
        new_state_dict[name] = v
    netx.load_state_dict(new_state_dict)


def get_feature(extractor,inpt):
    # return pytorch tensor 
    extractor.eval()
    indata = Variable(torch.Tensor(inpt), volatile=True)
    if usegpu:
        indata = indata.cuda()

    pred = extractor(indata)
    # print( pred.size())

    if len(pred.size()) > 2:
        gpred = globalpoolfn(pred,kernel_size=pred.size()[2:])
        gpred = gpred.view(gpred.size(0),-1)

    return gpred


#keep sample rate 44100, no need 
def main(foldername, srate=44100):

    # init the model
    netType = getattr(wnet, trainType)
    netx = netType(527,netwrkgpl)
    load_model(netx,pre_model_path)
    
    if usegpu:
        netx.cuda()
    
    feat_extractor = exm.featExtractor(netx,featType)


    features = {}
    files = os.listdir(foldername)
    for filename in files:

        print(filename)
        fileparts = filename.split('.')
        assert fileparts[1] == 'wav'

        filepath = os.path.join(foldername, filename)
        
        try:
            y, sr = lib.load(filepath,sr=None)
        except:
            raise IOError('Give me an audio  file which I can read!!')
        
        if len(y.shape) > 1:
            print( 'Mono Conversion',  )
            y = lib.to_mono(y)

        if sr != srate:
            print( 'Resampling to {}'.format(srate), )
            y = lib.resample(y,sr,srate)

            
        mel_feat = lib.feature.melspectrogram(y=y,sr=srate,n_fft=n_fft,hop_length=hop_length,n_mels=128)
        inpt = lib.power_to_db(mel_feat).T
        
        #quick hack for now
        if inpt.shape[0] < 128:
            inpt = np.concatenate((inpt,np.zeros((128-inpt.shape[0],n_mels))),axis=0)
        

        # input needs to be 4D, batch_size X 1 X inpt_size[0] X inpt_size[1]
        inpt = np.reshape(inpt,(1,1,inpt.shape[0],inpt.shape[1]))
        # print(inpt.shape) 

        pred = get_feature(feat_extractor,inpt)

        #numpy arrays
        feature = pred.data.cpu().numpy()
        print(feature) 

        features[fileparts[0]] = np.squeeze(feature)

    # prediction for each segment in each column
    return features


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError(' You need to give folder as first argument..Duhhh!!')
    
    features = main(sys.argv[1])
    print(features)
    
    if len(sys.argv) > 2:
        df = pd.DataFrame(features).T
        df.to_csv(sys.argv[2])
