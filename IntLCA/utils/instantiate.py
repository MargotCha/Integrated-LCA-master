from scipy import sparse
from pathlib import Path
from csv import reader
import brightway2 as bw
import numpy as np

def db_paths(base_path, scenarios, years):
    """
    Create a list of Path objects for given scenarios and years.

    Parameters:
    base_path (str): The base directory path.
    scenarios (list): List of scenario names.
    years (list): List of years.

    Returns:
    list: List of Path objects.
    """

    paths = []
    for scenario in scenarios:
        for year in years:
            path = Path(f"{base_path}/remind/{scenario}/{year}")
            paths.append(path)
    return paths


def matrices(path):
    """
    Creates sparse matrices `A` and `B` from CSV files and updates the indices dictionaries.

    Parameters
    ----------
    path : str or list of str
            The directory path(s) where the CSV files (`A_matrix_index.csv`, `B_matrix_index.csv`, `A_matrix.csv`, and `B_matrix.csv`) are located.
    A_inds : dict
        A dictionary to store the indices for the `A_matrix`. The function will populate this dictionary based on the content of the `A_matrix_index.csv` file.
    B_inds : dict
        A dictionary to store the indices for the `B_matrix`. The function will populate this dictionary based on the content of the `B_matrix_index.csv` file.

    Returns
    -------
    A : scipy.sparse.csr_matrix
        The sparse matrix representation of the `A_matrix.csv` file. The matrix is constructed using the I, J indices and the respective values.
    B : scipy.sparse.csr_matrix
        The sparse matrix representation of the `B_matrix.csv` file. The matrix is constructed using the I, J indices and the respective values, with all values negated.
    A_inds : dict
        The updated dictionary of indices corresponding to the `A_matrix`.
    B_inds : dict
        The updated dictionary of indices corresponding to the `B_matrix`.
    """

    A_inds = dict()
    with open(path / "A_matrix_index.csv", 'r') as read_obj:
        csv_reader = reader(read_obj, delimiter=";")
        for row in csv_reader:
            A_inds[(row[0], row[1], row[2], row[3], str(path).split('\\')[5], str(path).split('\\')[6])] = row[4]
    A_inds_rev = {int(v): k for k, v in A_inds.items()}

    B_inds = dict()
    with open(path / "B_matrix_index.csv", 'r') as read_obj:
        csv_reader = reader(read_obj, delimiter=";")
        for row in csv_reader:
            B_inds[(row[0], row[1], row[2], row[3], str(path).split('\\')[5], str(path).split('\\')[6])] = row[4]
    B_inds_rev = {int(v): k for k, v in B_inds.items()}

    A_coords = np.genfromtxt(path / "A_matrix.csv", delimiter=";", skip_header=1)
    I = A_coords[:, 0].astype(int)
    J = A_coords[:, 1].astype(int)
    A = sparse.csr_matrix((A_coords[:, 2], (J, I)))

    B_coords = np.genfromtxt(path / "B_matrix.csv", delimiter=";", skip_header=1)
    I = B_coords[:, 0].astype(int)
    J = B_coords[:, 1].astype(int)
    B = sparse.csr_matrix((B_coords[:, 2] * -1, (I, J)), shape=(A.shape[0], len(B_inds)))

    return A, B, A_inds, B_inds, A_inds_rev, B_inds_rev


def CF_vector(project, B, B_inds, methods):
    """
    Generates a list of characterization factor (CF) vectors for Life Cycle Impact Assessment (LCIA) based on the given methods.

    Parameters
    ----------
    B : scipy.sparse.csr_matrix
        The B matrix representing the inventory data, where each column corresponds to a specific flow.
    B_inds : dict
        A dictionary mapping each flow (represented as a tuple) to its corresponding index in the `B` matrix.
    methods : list of tuples, list of strings, or list of dictionaries
        A list of tuples, each representing an LCIA method to be used (e.g., `("IPCC 2013", "climate change", "GWP 100a")`).
        Alternatively, a list of strings where each string represents the first element of the tuple (e.g., `"IPCC 2021"`).
        Alternatively, a list of dictionaries where each dictionary can contain keys `method`, `category`, and `indicator`.

    Returns
    -------
    method_list : list of numpy.ndarray
        A list of 1D NumPy arrays where each array corresponds to the characterization factors for a specific method.
        Each element in an array corresponds to the characterization factor for a specific flow in the `B` matrix.
        If no characterization factor is found for a flow, the corresponding value in the array remains zero.
    """
    bw.projects.set_current(project)

    def fetch_method_tuple(method_dict):
        """
        Fetch the method tuple from Brightway2 using the method dictionary.

        Args:
            method_dict (dict): Dictionary containing 'method', 'category', and 'indicator' keys.

        Returns:
            tuple: The method tuple that matches the criteria.

        Raises:
            ValueError: If no matching method is found in the Brightway2 database.
        """
        available_methods = bw.methods
        method_tuple = (
            method_dict.get('method'),
            method_dict.get('category'),
            method_dict.get('indicator')
        )

        matching_methods = [
            method for method in available_methods
            if all(
                method[i] == method_tuple[i]
                for i in range(len(method_tuple))
                if method_tuple[i] is not None
            )
        ]

        if matching_methods:
            return matching_methods[0]
        else:
            raise ValueError(f"Method {method_dict} not found in Brightway2 database.")
        

    def convert_to_dict(method):
        """
        Convert method input to a dictionary format.

        Args:
            method (str, tuple, or dict): Method input.

        Returns:
            dict: Method input converted to dictionary format.
        """
        if isinstance(method, str):
            return {'method': method}
        elif isinstance(method, tuple):
            method_dict = {'method': method[0]}
            if len(method) > 1:
                method_dict['category'] = method[1]
            if len(method) > 2:
                method_dict['indicator'] = method[2]
            return method_dict
        elif isinstance(method, dict):
            return method
        else:
            raise ValueError(f"Unsupported method format: {method}")

    method_list = []

    for method in methods:
        method_dict = convert_to_dict(method)
        method_tuple = fetch_method_tuple(method_dict)

        e_flows = np.zeros(B.shape[1])
        m_cfs = {
            (bw.get_activity(k)["name"], bw.get_activity(k)["categories"]): v
            for k, v in bw.Method(method_tuple).load()
        }
        for flow, idx in B_inds.items():
            for keys in m_cfs:
                if flow[0] == keys[0] and flow[1] == keys[1][0]:
                    if flow[2] == 'unspecified':
                        key_test = flow[0], (flow[1],)
                        if key_test in m_cfs:
                            e_flows[int(idx)] = m_cfs[key_test]
                    else:
                        key_test = flow[0], (flow[1], flow[2])
                        if key_test in m_cfs:
                            e_flows[int(idx)] = m_cfs[key_test]
        method_list.append(e_flows)

    return np.array(method_list)