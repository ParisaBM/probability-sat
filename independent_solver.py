import torch

def solve_sat(si):
    prob_vector = torch.tensor([0.5]*si.num_variables, requires_grad=True)
    for i in range(100000):
        clause_probabilities = torch.ones(len(si.clauses))
        for j, c in enumerate(si.clauses):
            for l in c:
                if l[0]:
                    clause_probabilities[j] *= 1 - prob_vector[l[1]]
                else:
                    clause_probabilities[j] *= prob_vector[l[1]]
        clause_probabilities = 1 - clause_probabilities
        #score = clause_probabilities.log().sum()
        score = clause_probabilities.min()
        print(score)
        print(prob_vector)
        score.backward()
        with torch.no_grad():
            prob_vector = (prob_vector + 0.001*prob_vector.grad).clamp(0.0001, 0.9999)
        prob_vector.requires_grad = True
