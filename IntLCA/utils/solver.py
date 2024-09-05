from typing import List, Dict, Tuple
from scipy import sparse
from pypardiso import spsolve
import numpy as np
import pandas as pd
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '../../')))
from IntLCA import intLCA

def simple_calculation(act_to_run: int, A_inds_rev: Dict[int, str], CF_dict: Dict[str, np.ndarray], FU: int, A_: sparse.csr_matrix, B: sparse.csr_matrix) -> Tuple[pd.DataFrame, np.ndarray, np.ndarray]:
    """
    Run simple calculation by solving the linear system and computing the result.

    Args:
        act_to_run (int): Index representing the truck fleet.
        A_inds_rev (Dict[int, str]): Dictionary mapping indices to activity names.
        CF_dict (Dict[str, np.ndarray]): Dictionary of characterization factors.
        FU (int): Functional unit.
        A_ (csr_matrix): The modified technosphere matrix.
        B (csr_matrix): The matrix used for computing the result.

    Returns:
        Tuple[pd.DataFrame, np.ndarray, np.ndarray]: DataFrame of results, contribution, and scaling factor.
    """
    results = []
    for key, value in CF_dict.items():
        act = A_inds_rev[act_to_run]
        f = np.zeros(A_.shape[0], dtype=np.float64)
        f[act_to_run] = FU

        s = spsolve(A_, f)  # process contribution - scaling factor
        G = s * B

        total = (G * value).sum()  # For total impacts
        contribution = G * value
        results.append([act[0], act[2], act[3], act[4], act[5], total, key])

    df = pd.DataFrame(results, columns=["name", "unit", "location", "Pathway", "Year", "Score", "Method"])

    return df, contribution, s


def breakdown_calculation(act_to_run: int, A_inds_rev: Dict[int, str], methods, CF_dict: Dict[str, np.ndarray], FU: int, A_: sparse.csr_matrix, B: sparse.csr_matrix, results, act_tech) -> List[pd.DataFrame]:
    """
    Run simple calculation by solving the linear system and computing the result.

    Args:
        act_to_run (List[int]): List of indices representing the truck fleet.
        A_inds_rev (Dict[int, str]): Dictionary mapping indices to activity names.
        methods (List[str]): method to use for calculating the results.
        CF (List[int]): List of characterization factors.
        FU (int): Functional unit.
        A_ (np.ndarray): The modified technosphere matrix.
        B (np.ndarray): The matrix used for computing the result.
        results (List): List of results.

    Returns:
        List[pd.DataFrame]: List of results for each activity.
    """
    list_df = []
    for key, value in CF_dict.items():
        store = A_[:, act_to_run]
        store = store.toarray()
        indices = np.where(store != 0)[0] #getting the first level exchanges
        exchanges = {}
        for ind in indices:
            if store[ind][0] == 1:
                exchanges[ind] = abs(store[ind][0])
            else:
                exchanges[ind] = abs(store[ind][0])

        sum = 0
        for key, value in exchanges.items():
            # Perform calculations
            act_id = A_inds_rev[key]
            f = np.float64(np.zeros(A_.shape[0]))
            f[key] = value*FU

            s = spsolve(A_, f)
            G = s * B

            results.append([act_id[0], (G * value).sum()])

            if value != 1:
                sum = sum + (G * value).sum()
            else:
                total = (G * value).sum()

        results.append(['direct emissions', total - sum])
        df = pd.DataFrame(results, columns=["name", methods])
        df = df.transpose()
        names = df.iloc[0]
        df.columns = names
        df = df.drop(index='name')
        df['method'] = key
        df = df.reset_index(drop=True)
        df['Year'] = act_id[5]
        df['Database'] = act_id[4]
        df['Technology'] = act_tech[0]
        list_df =list_df + [df]

    return list_df


def multi_calculation(act_to_run: List[int], A_inds_rev, CF_dict: Dict[str, np.ndarray], FU, A_, B) -> pd.DataFrame:
    """
    Perform multiple calculations for Life Cycle Impact Assessment (LCIA).

    Args:
        act_to_run (List[int]): List of activity indices to run.
        A_inds_rev: Reversed indices for activities.
        CF_dict: Dictionary of characterization factors.
        FU: Functional unit.
        A_: Modified technosphere matrix.
        B: Biosphere matrix.

    Returns:
        pd.DataFrame: DataFrame containing the results.
    """
    results = []
    for key, value in CF_dict.items():
        for act in act_to_run:
            act_details = A_inds_rev[act]
            f = np.zeros(A_.shape[0], dtype=np.float64)
            f[act] = FU

            s = spsolve(A_, f)  # process contribution - scaling factor
            G = s * B

            total = (G * value).sum()  # For total impacts
            contribution = G * value
            results.append([act_details[0], act_details[2], act_details[3], act_details[4], act_details[5], total, key])

    df = pd.DataFrame(results, columns=["name", "unit", "location", "Pathway", "Year", "Score", "Method"])

    return df

def super_calculation(lca_instance, act_to_run, exc_to_remove, act_to_modify, act_to_add, A_inds_rev, CF_dict, FU, A, B) -> pd.DataFrame:
    """
    Scenario assessment -
    Modifying the matrix based on activities with same location and perform multiple calculations for
    several Life Cycle Impact Assessment (LCIA) methods. The matrix is modified as many times as we have scenarios.

    Args:
        lca_instance: Instance of the IntLCA class
        act_to_run (List[int]): List of activity indices to run.
        exc_to_remove: List of exchanges to remove.
        act_to_modify: List of activities to modify.
        act_to_add: List of activities to add.
        A_inds_rev: Reversed indices for activities.
        CF_dict: Dictionary of characterization factors.
        FU: Functional unit.
        A: Technosphere matrix.
        B: Biosphere matrix.

    Returns:
        pd.DataFrame: DataFrame containing the results.
    """

    A_ = lca_instance.copy_technosphere(A)
    A_ = lca_instance.modify_technosphere_remove(exc_to_remove, act_to_modify)

    results = []
    for key, value in CF_dict.items():
        for add in act_to_add:
            A_ = lca_instance.modify_technosphere_add_loc(exc_to_remove, add, act_to_modify)

            for run in act_to_run:
                act_details = A_inds_rev[run]
                f = np.zeros(A_.shape[0], dtype=np.float64)
                f[run] = FU

                s = spsolve(A_, f)  # process contribution - scaling factor
                G = s * B

                total = (G * value).sum()  # For total impacts
                contribution = G * value
                results.append([act_details[0], act_details[2], act_details[3], act_details[4], act_details[5], total, key])

            A_ = lca_instance.modify_technosphere_remove(add, act_to_modify)

    df = pd.DataFrame(results, columns=["name", "unit", "location", "Pathway", "Year", "Score", "Method"])

    return df