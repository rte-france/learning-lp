"""
The objective of the class dataset is to stock sets of RHS of linear optimisation problems
and their associated solutions (objective values) in order to make them exploitable
by a neural network.

All classes of this module primarily stock data.
"""
import os
import pickle
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import variation
from sklearn.preprocessing import StandardScaler


class RHS:
    """
    RHS is a class stocking a list of RHS fitting a given linear optimisation problem.

    In general the class will be used to stock the RHS newly generated by the
    module problem_generator.py. Since no details about the initial optimisation
    problem are kept, the only purpose of those RHS is to serve as training data for
    a neural network. For each RHS, the associated solution of the linear optimisation
    problem will be stocked in a list of solutions in an instance of the class solutions
    (see class solutions).

    Attributes
    ----------
    content : float list list or numpy array
        a list of truncated RHS fitting some linear optimisation problem
    """
    def __init__(self, data):
        """data can be an np.array or a list."""
        if isinstance(data, np.ndarray):
            self.content = data
        elif isinstance(data, list):
            self.content = np.array(data)
        else:
            raise Exception("Could not initialise the RHS instance. The data must be list or array.")

    def get_RHS(self):
        return self.content

    def set_RHS(self, new_RHS_list):
        self.__init__(new_RHS_list)

    def size(self):
        """
        Returns the number of RHS stocked in content.

        Returns
        -------
        size : int
        """
        return len(self.content)

    def save_csv(self, name, path=None):
        """
        Saves content in a file with format csv.

        Arguments
        ---------
        name : str
            name of the new file
        path : str
            path to file
        """
        import csv
        full_name = name + ".csv"
        csv_path = os.path.join("." if path is None else path, full_name)
        with open(csv_path, 'w', newline='') as file_RHS:
            writer = csv.writer(file_RHS, delimiter=';')
            writer.writerows(self.content)


class solutions:
    """
    solutions is a class stocking a list of solutions of linear optimisation problems
    that differ only by their RHS.

    In general the class will be used to stock the solutions of the the problems
    that have been newly generated by the module problem_generator.py. Since no other
    details then the truncated RHS are kept about those optimisation problems, the only
    purpose of those solutions is to serve as training data for a neural network.
    For each solution, the associated RHS of the linear optimisation problem will be
    stocked in a list of RHS in an instance of the class RHS (see class RHS).

    Attributes
    ----------
    content : float list or numpy array
       a list of solutions of some linear optimisation problems that differ only by their
       RHS
    """
    def __init__(self, data):
        """data can be a list or an instance of np.array with the solutions"""
        if isinstance(data, np.ndarray):
            self.content = data
        elif isinstance(data, list):
            self.content = np.array(data)
        else:
            raise Exception("could not initialize the solution instance. The data must be list or array")

    def get_solutions(self):
        """return an array with the solutions"""
        return self.content

    def set_solutions(self, new_solutions):
        self.__init__(new_solutions)

    def size(self):
        """
        Returns the number of solutions stocked in content.

        Returns
        -------
        size : int
        """
        return len(self.content)

    def save_csv(self, name, path=None):
        """
        Saves content in a file with format csv.

        Arguments
        ---------
        name : str
            name of the new file
        path : str
            path to file
        """
        import csv
        full_name = name + ".csv"
        csv_path = os.path.join("." if path is None else path, full_name)
        with open(csv_path, 'w', newline='') as file_sol:
            writer = csv.writer(file_sol, delimiter=';')
            sol_list = self.content.reshape(-1, 1)
            writer.writerows(sol_list)


class dataset:
    """
    dataset is a class stocking a list of RHS fitting a given linear optimisation problem
    and the list of solutions of that optimisation problem for each RHS respectively.

    In general the class will be used to stock the RHS and solutions of the the problems
    that have been newly generated by the module problem_generator.py. The main
    purpose of a dataset instance is to serve as training data for a neural network
    (see class NeuralNetwork). dataset is not used to stock the predictions of
    a neural network instance (see class OutputData).


    (For more information see class RHS and class solutions)

    Attributes
    ----------
    RHS : float list list or numpy array
        (see class RHS)
    solutions : float list or numpy array
        (see class solutions)
    """
    def __init__(self, RHS_list, solutions_list):
        self.RHS = RHS(RHS_list)
        self.solutions = solutions(solutions_list)
        s1, s2 = self.solutions.size(), self.RHS.size()
        if s1 != s2:
            print("{} != {}".format(s1, s2))
        assert s1 == s2, "RHS and solutions do not have the same size"

    def get_solutions(self):
        """Returns the solutions as an array."""
        return self.solutions.get_solutions()

    def get_RHS(self):
        """Returns the RHS as an array"""
        return self.RHS.get_RHS()

    def set_RHS(self, new_RHS):
        assert len(new_RHS) == self.size()
        self.RHS.set_RHS(new_RHS)

    def set_solutions(self, new_solutions):
        assert len(new_solutions) == self.size()
        self.solutions.set_solutions(new_solutions)

    def size(self):
        """
        Returns number of samples in dataset instance.

        Returns
        -------
        size : int
            number of samples
        """
        return self.RHS.size()

    def dump_in_file(self, file_name, path=None):
        """
        Dumps self.RHS and self.solutions in a pickle file.

        The file is created at path/file_name. The full path should always be specified.
        self.RHS and self.solutions are stocked under the form of a pair
        (self.RHS, self.solutions).

        Arguments
        ---------
        path : str
            path to new file
        file_name : str
            name of the new file
        """
        import pickle
        pickle_path = os.path.join("." if path is None else path, file_name)
        set = (self.RHS.get_RHS(), self.solutions.get_solutions())
        pickle.dump(set, open(pickle_path, "wb"))

    def to_csv(self, name, path=None, single_file=False):
        """
        Saves content in a single or two distinct files with format csv.

        If single_file is True, the content is saved in a single file.
        Else the content is saved in two separate files. More precisely,
        the first file contains self.RHS, the second one self.solutions.
        Both files are saved in the same directory and have names that start
        with the string given as an argument.

        Arguments
        ---------
        name : str
            name of the new file
        path : str
            path to file
        single_file : bool
            states whether self.RHS and self.solutions are saved in a single file
            or two separate files
        """
        import csv
        if single_file:
            reshaped_sol = np.reshape(self.get_solutions(), (self.size(), 1))
            content = np.concatenate((self.get_RHS(), reshaped_sol), axis=1)
            full_name = name + ".csv"
            csv_path = os.path.join("." if path is None else path, full_name)
            with open(csv_path, 'w', newline='') as file_cont:
                writer = csv.writer(file_cont, delimiter=';')
                writer.writerows(content)
        else:
            self.RHS.save_csv(name + "_RHS", path)
            self.solutions.save_csv(name + "_sol", path)

    def cut(self, proportion_to_cut):
        """
        Cuts a certain proportion of constraints out of self to create a new dataset.

        The proportion of data to be cut out is given by proportion_to_cut. The indices
        of the data to be cut out are chosen randomly. The cut data is deleted from the first dataset.

        Arguments
        ---------
        proportion_to_cut : float
            proportion of data to be cut out of self

        Returns
        -------
        dataset : dataset instance
            instance containing the cut out data
        """
        size = self.size()
        number_to_cut = int(proportion_to_cut * size)
        index_to_cut = np.random.choice(size, number_to_cut, replace=False)  # We randomly generate the indexes to cut
        list_to_cut_bool = size * [False]
        for index in index_to_cut:
            list_to_cut_bool[index] = True  # list_to_cut_bool[i] is True if line i must be cut
        RHS_to_keep, solutions_to_keep = [], []
        RHS_to_cut, solutions_to_cut = [], []
        initial_RHS_array = self.get_RHS()
        initial_solutions_array = self.get_solutions()
        for i in range(size):
            if list_to_cut_bool[i]:  # if we cut the line i
                RHS_to_cut.append(initial_RHS_array[i])
                solutions_to_cut.append(initial_solutions_array[i])
            else:
                RHS_to_keep.append(initial_RHS_array[i])
                solutions_to_keep.append(initial_solutions_array[i])
        self.__init__(RHS_to_keep, solutions_to_keep)
        return dataset(RHS_to_cut, solutions_to_cut)

    def merge(self, other_dataset):
        """
        Merges the given dataset into self.

        More precisely the content of self and the given dataset are concatenated.
        The dataset given as an argument is not modified.

        Arguments
        ---------
        other_dataset : dataset instance
            dataset to be merged with self
        """
        assert isinstance(other_dataset, dataset), "Argument has to be a dataset instance."
        assert len(other_dataset.get_RHS()[0]) == len(self.get_RHS()[0]), "Bound vectors do not have the same size."

        new_RHS_array = np.concatenate((self.get_RHS(), other_dataset.get_RHS()), axis=0)
        new_solutions_array = np.concatenate((self.get_solutions(), other_dataset.get_solutions()), axis=0)
        
        self.__init__(new_RHS_array, new_solutions_array)

    def copy(self):
        """Copies the dataset."""
        return dataset(np.copy(self.get_RHS()), np.copy(self.get_solutions()))

    def cut_the_first_one(self):
        assert self.size() > 0
        proportion_to_cut = 1 / self.size()
        return self.cut(proportion_to_cut)


def load_pickle(file_name, path=None):
    """
    Unpickels a file into a dataset instance.

    Should only be used on a file that has previously been pickled
    by the method dataset.dump_in_file (see dump_in_file).

    Arguments
    ---------
    path : str
        path to file
    file_name : str
        name of file
    """
    pickle_path = os.path.join("." if path is None else path, file_name)
    set = pickle.load(open(pickle_path, "rb"))
    data = dataset(set[0], set[1])
    assert data.solutions.size() == data.RHS.size(), "RHS and solutions do not have the same size"
    return data


def load_csv(file_RHS, file_sol, path=None):
    """
    Loads the content of two csv files into a dataset instance.

    Takes two file names a arguments. The first one should contain a list of
    RHS, the second one a list of solutions. Both files should be saved in the
    same directory.

    Arguments
    ---------
    path : str
        path to file
    file_RHS : str
        name of file containing a RHS list
    file_sol : str
        name of file containing a list of solutions
    """
    import csv
    RHS_list = []
    solutions = []
    csv_path = os.path.join("." if path is None else path, file_RHS)
    with open(csv_path, "r") as csv_RHS:
        reader = csv.reader(csv_RHS)
        for row in reader:
            RHS_list.append([float(e) for e in row])
    sol_path = os.path.join("." if path is None else path, file_sol)
    with open(sol_path, "r") as csv_sol:
        reader = csv.reader(csv_sol)
        for row in reader:
            solutions.append(float(row[0]))
    return dataset(RHS_list, solutions)


def load_csv_single_file(file, path=None):
    """
    Loads the content of a csv file into a dataset instance.

    The file should contain a float table. The last column of that table
    should contain the solution vector.

    Arguments
    ---------
    path : str
        path to file
    file : str
        name of file
    """
    import csv
    content = []
    csv_path = os.path.join("." if path is None else path, file)
    with open(csv_path, "r") as csv_RHS:
        reader = csv.reader(csv_RHS)
        for row in reader:
            content.append([float(e) for e in row])
    RHS_list = content[:-1]
    solutions = content[-1]
    return dataset(RHS_list, solutions)
