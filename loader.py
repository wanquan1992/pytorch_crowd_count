import torch
import h5py
import glob
import os
import numpy as np
import torch.utils.data as data
class UCF_CC_50(data.Dataset):
	def __init__(self, h5_datapath):
		super(UCF_CC_50, self).__init__()
		self.h5_datapath = h5_datapath
		hdf5_list = [x for x in glob.glob(os.path.join(self.h5_datapath, '*.h5'))]
		print(hdf5_list)
		self.images = []
		self.gts = []
		self.total_patches = 0
		self.limits = []
		for f in hdf5_list:
			with h5py.File(f, 'r') as h5_file:
				images = h5_file.get('data')
				gts = h5_file.get('label')
				self.images.append(np.array(images))
				self.gts.append(np.array(gts))
				self.limits.append(images.shape[0])
				self.total_patches += images.shape[0]
		print(self.limits)
	
	def __getitem__(self, index):
		dataset_index = -1
		for i in range(len(self.limits)-1, -1, -1):
			if index>=self.limits[i]:
				dataset_index = i
				break
			in_dataset_index = index -self.limits[dataset_index]
			return self.images[dataset_index][in_dataset_index], self.gts[dataset_index][in_dataset_index] 
	def __len__(self):
		return self.total_patches
if __name__ == '__main__':
	dataset = UCF_CC_50('dataset/processed_hdf5')
	print dataset.__getitem__(20)