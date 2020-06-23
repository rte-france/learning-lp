"""
Implementation for FICO Xpress of the Problem interface in problem_interface.py.
"""

from problem_interface import Problem, Problem_factory
import xpress as xp


class Xpress_problem(Problem):

    def __init__(self):
        self.content = xp.problem()
        self.mute_solver()

    def read(self, filename):
        """Loads problem from file."""
        self.content.read(filename)

    def get_RHS(self, cons_to_vary):
        """
        Returns the RHS of the linear optimisation problem.

        Arguments
        ---------
        cons_to_vary : int list
            indices of RHS to be returned

        Returns
        -------
        rhs : float list
        """
        rhs = []
        if cons_to_vary is None:
            return rhs
        else:
            for elem in cons_to_vary:
                aux = []
                self.content.getrhs(aux, elem, elem)
                rhs.append(aux[0])
            return rhs

    def set_RHS(self, rhs):
        """
        Changes the RHS of the linear optimisation problem to the input.

        Arguments
        ---------
        rhs : (int, float) list
            the format required by cplex
        """
        self.content.chgrhs(mindex=[i[0] for i in rhs], rhs=[i[1] for i in rhs])

    def get_constraint_names(self):
        """
        Returns list of names of constraints of the linear optimisation problem.

        Returns
        -------
        name list : string list
        """
        constraints = self.content.getConstraint()
        nb_cons = len(constraints)
        name_list = nb_cons * [None]
        for i in range(nb_cons):
            name_list[i] = constraints[i].name.strip()
        return name_list

    def get_variable_names(self):
        """
        Returns list of names of variables of the linear optimisation problem.

        Returns
        -------
        name list : string list
        """
        variables = self.content.getVariable()
        nb_vars = len(variables)
        name_list = nb_vars * [None]
        for i in range(nb_vars):
            name_list[i] = variables[i].name.strip()
        return name_list

    def solve(self):
        """Solves the linear optimisation problem."""
        self.content.solve()

    def get_objective_value(self):
        """Returns the solution of the linear optimisation problem (objective value)."""
        return self.content.getObjVal()

    def mute_solver(self):
        """Disables all messages generated by the solver while solving the optimisation problem."""
        self.content.setControl("outputlog", 0)

    def var_get_bounds(self, ind):
        """Returns the bounds of the variable with index ind."""
        var = self.content.getVariable(ind)
        return var.lb, var.ub

    def var_set_bounds(self, ind, lw_bnd, up_bnd):
        """Sets the bounds of the variable with index ind to lw_bnd and up_bnd."""
        self.content.chgbounds([ind, ind], ["L", "U"], [lw_bnd, up_bnd])

    def get_status(self):
        """Returns the status of the solution"""
        return self.content.getProbStatusString()

    def is_feasible(self):
        """True if problem is feasible."""
        if self.get_status() == "lp_infeas":
            return False
        else:
            return True


class Xpress_Problem_Factory(Problem_factory):

    def get_problem_instance(self) -> Xpress_problem:
        return Xpress_problem()

    def read_problem_from_file(self, filename: str) -> Xpress_problem:
        p = Xpress_problem()
        p.read(filename)
        return p


# if __name__ == '__main__':
#
#     petit_probleme = Xpress_Problem_Factory().read_problem_from_file("petit_probleme.lp")
#     petit_probleme.set_RHS([(25, -12)])
#     petit_probleme.solve()
#     print(petit_probleme.get_objective_value())
#     print(petit_probleme.get_status())
