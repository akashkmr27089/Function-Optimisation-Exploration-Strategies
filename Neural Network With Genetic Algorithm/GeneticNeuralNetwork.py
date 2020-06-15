########################################################
## Written By Aakash Kumar akashkmr27089@gmail.com
########################################################

import torch
from torch import nn
import numpy as np
from collections import OrderedDict

def network_to_array(model):
    final_para = []
    for x in model.parameters():
        x = list(x.cpu().detach().numpy().flatten())
        final_para += x
    return final_para  

def array_to_state_dict(data_list, model):
    #this is used to convert array into model 
    para_old = model.state_dict()
    para = {}
    position = 0
    for i in range(len(para_old)):
        if(i%2 == 0):
            #weights
            data = list(para_old['fc'+str(int(i/2)+1)+'.weight'].size())
            size_selection = data[0]*data[1]
            array_data = np.array(data_list[position:position+size_selection]).reshape(data[0],data[1])
            position += size_selection
            tensor_data = torch.from_numpy(np.array(array_data))
            para.update({'fc'+str(int(i/2)+1)+'.weight':tensor_data})
        else:
            data = list(para_old['fc'+str(int(i/2)+1)+'.bias'].size())
            size_selection = data[0]
            array_data = np.array(data_list[position:position+size_selection]).reshape(data[0],)
            position += size_selection
            tensor_data = torch.from_numpy(np.array(array_data))
            para.update({'fc'+str(int(i/2)+1)+'.bias':tensor_data})
    return OrderedDict(para)

def population_size(model): 
    return network_to_array(model).__len__()

class actor(nn.Module):
    def __init__(self):
        super(actor,self).__init__()
        self.fc1 = nn.Linear(3,6)
        self.fc2 = nn.Linear(6,3)
    def forward(self, data):
        x = self.fc1(data)
        x = nn.ReLU(x)
        return self.fc2(x)

def main():
    actor_obj = actor()
    critic_obj = actor()
    print(" Actor Object : \n ", actor_obj.state_dict())
    print(" Critic Objcet : \n ", critic_obj.state_dict())
    array_list = network_to_array(actor_obj)
    print()
    print(" Array Representaiton of Weights (Actor):", np.array(array_list))
    final_actor_dict = array_to_state_dict(array_list, actor_obj)
    critic_obj.load_state_dict(final_actor_dict)
    print()
    print(" Critic Object : \n ", critic_obj.state_dict())

if __name__ ==  "__main__":
    main()
