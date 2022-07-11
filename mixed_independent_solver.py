from independent_solver import non_opposite
import torch

def solved_mixed(si):
    prob_matrix = torch.rand((2, si.num_variables), requires_grad=True)
    case_distribution = torch.rand((), requires_grad=True)
    for i in range(100000):
        upward_directions = []
        worst = torch.tensor(1.)
        for j, c in enumerate(si.clauses):
            clause_probability = torch.tensor(0.)
            for k in range(2):
                case_probability = torch.tensor(1.)
                for l in c:
                    if l[0]:
                        case_probability *= 1 - prob_matrix[k][l[1]]
                    else:
                        case_probability *= prob_matrix[k][l[1]]
                if k == 0:
                    clause_probability += (1 - case_probability) * case_distribution
                else:
                    clause_probability += (1 - case_probability) * (1 - case_distribution)
            worst = min(worst, clause_probability)
            clause_probability.backward()
            upward_directions.append(prob_matrix.grad.flatten().tolist() + [case_distribution.grad.tolist()])
            prob_matrix.grad.zero_()
            case_distribution.grad.zero_()
        print(worst)
        step_direction = non_opposite(upward_directions)
        with torch.no_grad():
            prob_matrix = (prob_matrix + 0.01*step_direction[:-1].reshape((2, si.num_variables))).clamp(0.0001, 0.9999)
            case_distribution = (case_distribution + 0.01*step_direction[-1]).clamp(0.0001, 0.9999)
        prob_matrix.requires_grad = True
        case_distribution.requires_grad = True