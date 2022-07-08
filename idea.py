import torch
from torch import tensor
from independent_solver import non_opposite

vec = tensor([0.6, 0.1, 0.1, 0.11, 0.11], requires_grad=True)
directions = []

p = vec[0]*vec[1]*vec[2] + (1-vec[0])*vec[3]*vec[4]
p.backward()
directions.append(vec.grad.tolist())
vec.grad.zero_()

p = vec[0]*(1-vec[1])*vec[2] + (1-vec[0])*(1-vec[3])*vec[4]
(-p).backward()
directions.append(vec.grad.tolist())
vec.grad.zero_()

p = vec[0]*vec[1]*(1-vec[2]) + (1-vec[0])*vec[3]*(1-vec[4])
(-p).backward()
directions.append(vec.grad.tolist())
vec.grad.zero_()

p = vec[0]*(1-vec[1])*(1-vec[2]) + (1-vec[0])*(1-vec[3])*(1-vec[4])
(-p).backward()
directions.append(vec.grad.tolist())

print(directions)
print(non_opposite(directions))