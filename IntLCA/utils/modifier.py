from typing import List
import copy
from scipy import sparse

def  copy_technosphere(A: sparse.csr_matrix):
    """
    Copy the technosphere matrix to make changes.
    """

    A_ = copy.deepcopy(A)

    return A_


def remove_technosphere(A_: sparse.csr_matrix, exc_to_remove: List[int], act_to_modify: List[int]):
    """
    Prepare the technosphere matrix for new activities by removing specified elements.

    Args:
        A (List[List[float]]): The original technosphere matrix.
        exc_to_remove (List[int]): List of indices of elements to remove.
        act_to_modify (List[int]): List of indices of elements to modify.

    Returns:
        List[List[float]]: The modified technosphere matrix with specified elements removed.
    """

    A_[exc_to_remove, act_to_modify] = 0

    return A_


def add_technosphere(A_: sparse.csr_matrix, exc_to_remove: List[int], act_to_modify: List[int], act_to_add: List[int]):
    """
    Add to the technosphere matrix new connections between existing and new activities.

    Args:
        A (List[List[float]]): The original technosphere matrix.
        exc_to_remove (List[int]): List of indices of elements to remove.
        act_to_modify (List[int]): List of indices of elements to modify.

    Returns:
        List[List[float]]: The modified technosphere matrix with specified elements removed.
    """
        
    amount = A_[exc_to_remove, act_to_modify]
    A_[act_to_add, act_to_modify] = amount

    return A_


def add_technosphere_loc(A_: sparse.csr_matrix, exc_to_remove: List[int], act_to_modify: List[int],
                     act_to_add: List[int], A_inds_rev):
    """
    Add to the technosphere matrix new connections between existing and new activities.

    Args:
        A (List[List[float]]): The original technosphere matrix.
        exc_to_remove (List[int]): List of indices of elements to remove.
        act_to_modify (List[int]): List of indices of elements to modify.

    Returns:
        List[List[float]]: The modified technosphere matrix with specified elements removed.
    """
    for add in act_to_add:
        for modify in act_to_modify:
            if A_inds_rev[add][3] == A_inds_rev[add][3]:
                amount = A_[exc_to_remove[0], act_to_modify]
                A_[add, modify] = amount

    return A_
