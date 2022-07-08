import torch
from scipy.optimize import linprog

def non_opposite(vectors):
    # takes as input a list of vectors
    # returns a non-zero vector whose dot product with any input vector is non-negative
    # returns null if it can't find one
    objective = [0]*len(vectors[0])+[-1]
    zero_ub = [0]*len(vectors)
    box = [(-1, 1)]*len(vectors[0])+[(0, None)]
    negative_vectors = [[-x for x in v]+[1] for v in vectors]
    result = linprog(c = objective, A_ub = negative_vectors, b_ub = zero_ub, bounds = box)
    print(result)
    result = result.x[:-1]
    result = torch.tensor(result)
    return result

def solve_sat(si):
    # prob_vector = torch.tensor([0.5]*si.num_variables, requires_grad=True)
    prob_vector = torch.rand(si.num_variables, requires_grad=True)
    for i in range(100000):
        upward_directions = []
        worst = torch.tensor(1)
        for j, c in enumerate(si.clauses):
            clause_probability = torch.tensor(1.)
            for l in c:
                if l[0]:
                    clause_probability *= 1 - prob_vector[l[1]]
                else:
                    clause_probability *= prob_vector[l[1]]
            clause_probability = 1 - clause_probability
            worst = min(worst, clause_probability)
            clause_probability.backward()
            upward_directions.append(prob_vector.grad.tolist())
            prob_vector.grad.zero_()
        #print(upward_directions)
        print(worst)
        step_direction = non_opposite(upward_directions)
        with torch.no_grad():
            prob_vector = (prob_vector + step_direction).clamp(0.0001, 0.9999)
            print(prob_vector)
        prob_vector.requires_grad = True
