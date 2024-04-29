import torch
import argparse
import numpy as np
if __name__ == '__main__':
    from MSnet.MelodyExtraction import MeExt
else:
    from .MSnet.MelodyExtraction import MeExt
import os
def main(filepath, model_type, output_dir = "./output/", gpu_index = None, evaluate = None, mode = 'std'):
    # since it will be called directly also, we need to asign default values here as well

    songname = filepath.split('/')[-1].split('.')[0]
    pretrained_models = "/nfs/guille/eecs_research/soundbendor/models/Melody-extraction-with-melodic-segnet/MSnet/pretrain_model/"
    model_path = pretrained_models+'MSnet_'+str(model_type)

    if gpu_index is not None:
        with torch.cuda.device(gpu_index):
            print("using GPU")
            est_arr = MeExt(filepath, model_type=model_type, model_path=model_path, GPU=True, mode=mode, gid=gpu_index)
    else:
        print("using CPU")
        est_arr = MeExt(filepath, model_type=model_type, model_path=model_path, GPU=False, mode=mode)

    override_output_dir = '/'.join(filepath.split('/')[:-2])+'/melody/'
    output_dir = override_output_dir
    # print(output_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    print('Save the result in '+output_dir+songname+'.txt')
    np.savetxt(output_dir+'/'+songname+'.txt', est_arr)
    if evaluate is not None:
        raise NotImplementedError("Evaluation is not implemented yet")
        import pandas as pd
        from MSnet.utils import melody_eval
        if 'csv' in evaluate:
            ycsv = pd.read_csv(evaluate, names = ["time", "freq"])
            gtt = ycsv['time'].values
            gtf = ycsv['freq'].values
            ref_arr = np.concatenate((gtt[:,None], gtf[:,None]), axis=1)
        elif 'txt' in evaluate:
            ref_arr = np.loadtxt(evaluate)
        else:
            print("Error: Wrong type of ground truth. The file must be '.txt' or '.csv' ")
            return None
        eval_arr = melody_eval(ref_arr, est_arr)
        print(songname, ' | VR: {:.2f}% VFA: {:.2f}% RPA: {:.2f}% RCA: {:.2f}% OA: {:.2f}%'.format(
        eval_arr[0], eval_arr[1], eval_arr[2], eval_arr[3], eval_arr[4]))
    
    return est_arr
def parser():

    p = argparse.ArgumentParser()

    p.add_argument('-fp', '--filepath',
                    help='Path to input audio (default: %(default)s',
                    type=str, default='train01.wav')
    p.add_argument('-t', '--model_type',
                    help='Model type: vocal or melody (default: %(default)s',
                    type=str, default='vocal')
    p.add_argument('-gpu', '--gpu_index',
                    help='Assign a gpu index for processing. It will run with cpu if None.  (default: %(default)s',
                    type=int, default=None)
    p.add_argument('-o', '--output_dir',
                    help='Path to output folder (default: %(default)s',
                    type=str, default='./output/')
    p.add_argument('-e', '--evaluate', 
                    help='Path of ground truth (default: %(default)s',
                    type=str, default=None)
    p.add_argument('-m', '--mode', 
                    help='The mode of CFP: std and fast (default: %(default)s',
                    type=str, default='std')
    return p.parse_args()
if __name__ == '__main__':
    args = parser()
    main(args.filepath, args.model_type, args.output_dir, args.gpu_index, args.evaluate, args.mode)

