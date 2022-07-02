from independent_solver import solve_sat

class SatInstance:
    # a sat instance variable stores a sat problem in cnf
    # it's represented as a list of clauses
    # each clause is represented as a list of literals
    # a literal is a tuple containing a boolean to say whether its postive or negative, and an integer identifier
    # the identifiers are from 0 to num_variables-1 inclusively
    # this is offset by 1 compared to the dimacs format which uses 1 as its base identifier
    # self.num_variables is simply the number of variables in the problem
    def __init__(self, filename):
        # the parameters of the problem are taken from a dimacs file
        # the name of that file is given as the parameter of the initializer
        # the format is specified here: http://beyondnp.org/static/media/uploads/docs/satformat.pdf
        # although dimacs supports cnf and sat, our parser assumes cnf
        with open(filename) as file:
            self.clauses = [[]]
            reached_problem_line = False
            for line in file:
                line = line.strip()
                if line.startswith('c'):
                    continue
                tokens = line.split()
                if not reached_problem_line:
                    # the problem line is the first non-comment line of the file
                    # it should look like "p cnf n m"
                    # we care about n the number of variables, 
                    # but not m the number of clauses which we can determine implicitly as we construct the clauses
                    if len(tokens) < 4:
                        print("too few token in problem on line:\n\t" + line)
                        break
                    if tokens[0] != "p":
                        print("problem line must start with p on line:\n\t" + line)
                        break
                    if tokens[1] != "cnf":
                        print("must be cnf format on line:\n\t" + line)
                    try:
                        self.num_variables = int(tokens[2])
                    except:
                        print("invalid number of variables on line:\n\t" + line)
                        break
                    reached_problem_line = True
                else:
                    # clauses are represented as integers
                    # a negative integer represents a negated literal
                    # a 0 delimits the end of each clause
                    # sometimes the last clause doesn't have a 0
                    for literal in tokens:
                        try:
                            literal_as_int = int(literal)
                            if literal_as_int == 0:
                                self.clauses.append([])
                            else:
                                self.clauses[-1].append((literal_as_int > 0, abs(literal_as_int)-1))                     
                        except:
                            print("bad literal or seperator:" + literal)
                            break
        # if the last clause does have a 0 at the end we clean up its empty clause
        if not self.clauses[-1]:
            self.clauses.pop()
    def subscript_number(n):
        # takes an integer and represents it with subscripted symbols
        # for example 21 would become the string "₂₁"
        # the unicode code-point difference between regular integer symbols, such as "3", 
        # and their subscripted counterparts, such as "₃" is 8272, so we add this amount to each character
        return "".join([chr(ord(x)+8272) for x in str(n)])
    def display(self):
        # a function to print a problem one clause per line
        for clause in self.clauses:
            literals = [("" if x[0] else "¬") + "x" + SatInstance.subscript_number(x[1]) for x in clause]
            print(" ∨ ".join(literals))

if __name__ == "__main__":
    si = SatInstance('15.cnf')
    si.display()
    solve_sat(si)