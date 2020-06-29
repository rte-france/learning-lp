"""
Interface for linear optimisation problems as needed in problem_generator and
problem_selector. The default implementation of the interface is Cplex_problem.
"""


class Problem:

    def read(self, filename):
        """Loads problem from file."""
        pass

    def get_RHS(self, cons_to_vary):
        """
        Returns the RHS of the linear optimisation problem.

        Arguments
        ---------
        cons_to_vary : int list
            indices of RHS to be returned

        Returns
        -------
        rhs : float list (IMPORTANT)
        """
        pass

    def set_RHS(self, rhs):
        """
        Changes the RHS of the linear optimisation problem to the input.

        Arguments
        ---------
        rhs : (int, float) list
            the format required by cplex (IMPORTANT)
        """
        pass

    def get_constraint_names(self):
        """
        Returns list of names of constraints of the linear optimisation problem.

        Returns
        -------
        name list : string list
        """
        pass

    def get_variable_names(self):
        """
        Returns list of names of variables of the linear optimisation problem.

        Returns
        -------
        name list : string list
        """
        pass

    def solve(self):
        """Solves the linear optimisation problem."""
        pass

    def get_objective_value(self):
        """Returns the solution of the linear optimisation problem (objective value)."""
        pass

    def mute_solver(self):
        """Disables all messages generated by the solver while solving the optimisation problem."""
        pass

    def var_get_bounds(self, ind):
        """Returns the bounds of the variable with index ind."""
        pass

    def var_set_bounds(self, ind, lw_bnd, up_bnd):
        """Sets the bounds of the variable with index ind to lw_bnd and up_bnd."""
        pass

    def get_status(self):
        """Returns the status of the solution"""
        pass

    def is_feasible(self):
        """True if problem is feasible."""
        pass


class Problem_factory:

    def get_problem_instance(self) -> Problem:
        pass

    def read_problem_from_file(self, filename: str) -> Problem:
        pass
