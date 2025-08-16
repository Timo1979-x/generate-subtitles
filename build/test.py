import torch, os

# num_of_gpus = torch.cuda.device_count()
# print(f"num_of_gpus: {num_of_gpus}")

# for i in range(num_of_gpus):
#    print(torch.cuda.get_device_properties(i))


def get_device():
  device = os.getenv("DEVICE", None)
  if device != None:
    return device
  if torch.cuda.device_count() == 0:
    return 'cpu'
  else:
    return 'cuda:0'
  
print(f"detected device is {get_device()}")
