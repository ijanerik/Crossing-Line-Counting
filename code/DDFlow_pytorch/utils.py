import cv2
import numpy as np
from matplotlib import pyplot as plt
import datetime
import torch


def save_gt(pair, flow_fw, flow_bw, occ_fw, occ_bw, prefix):
    np.save(pair.get_frames(0).get_info_dir('{}flow_bw.npy'.format(prefix)), flow_fw.numpy())
    np.save(pair.get_frames(0).get_info_dir('{}flow_fw.npy'.format(prefix)), flow_bw.numpy())
    np.save(pair.get_frames(0).get_info_dir('{}occ_fw.npy'.format(prefix)), occ_fw.numpy())
    np.save(pair.get_frames(0).get_info_dir('{}occ_bw.npy'.format(prefix)), occ_bw.numpy())

def load_gt(pair, prefix):
    flow_fw = torch.from_numpy(np.load(pair.get_frames(0).get_info_dir('{}flow_bw.npy'.format(prefix))))
    flow_bw = torch.from_numpy(np.load(pair.get_frames(0).get_info_dir('{}flow_fw.npy'.format(prefix))))
    occ_fw = torch.from_numpy(np.load(pair.get_frames(0).get_info_dir('{}occ_fw.npy'.format(prefix))))
    occ_bw = torch.from_numpy(np.load(pair.get_frames(0).get_info_dir('{}occ_bw.npy'.format(prefix))))

    return flow_fw, flow_bw, occ_fw, occ_bw

# Return a RGB image based on a optical flow map
def flo_to_color(flo):
    hsv = np.zeros((flo.shape[0], flo.shape[1], 3), dtype=np.uint8)
    n = 8
    max_flow = flo.max()
    mag, ang = cv2.cartToPolar(flo[:, :, 0], flo[:, :, 1])
    hsv[:, :, 0] = ang * 180 / np.pi / 2
    hsv[:, :, 1] = np.clip(mag*n/max_flow*255, 0, 255)/3
    hsv[:, :, 2] = 255
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    RGB_im = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    return RGB_im

class sTimer():
    def __init__(self, name):
        self.start = datetime.datetime.now()
        self.name = name

    def show(self, printer=True):
        ms = int((datetime.datetime.now() - self.start).total_seconds() * 1000)
        if printer:
            print("{}: {}ms".format(self.name, ms))
            
        return ms

# FROM CSRNET
class AverageMeter(object):
    """Computes and stores the average and current value"""
    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count