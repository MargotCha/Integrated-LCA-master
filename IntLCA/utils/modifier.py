from typing import List
import copy
from scipy import sparse

def  copy_technosphere(A: sparse.csr_matrix) -> sparse.csr_matrix:
    """
    Copy the technosphere matrix to make changes.

    Args:
        A (sparse.csr_matrix): The original technosphere matrix.

    Returns:
        A_ (sparse.csr_matrix): The copy of the original technosphere matrix.
    """

    A_ = copy.deepcopy(A)

    return A_


def remove_technosphere(A_: sparse.csr_matrix, exc_to_remove: List[int], act_to_modify: List[int]) -> sparse.csr_matrix:
    """
    Prepare the technosphere matrix for new activities by removing specified elements.

    Args:
        A_ (spare.csr_matrix): A copy of the original technosphere matrix. -> Can be obtained from the function copy_technosphere
        exc_to_remove (List[int]): List of indices of elements to remove.
        act_to_modify (List[int]): List of indices of elements to modify.

    Returns:
        A_ (sparse.csr_matrix): The modified technosphere matrix with specified elements removed.
    """

    A_[exc_to_remove, act_to_modify] = 0

    return A_


def add_technosphere(A_: sparse.csr_matrix, exc_to_remove: List[int], act_to_modify: List[int], act_to_add: List[int]) -> sparse.csr_matrix:
    """
    Add to the technosphere matrix new connections between existing and new activities.

    Args:
        A_ (spare.csr_matrix): A copy of the original technosphere matrix. -> Can be obtained from the function copy_technosphere
        exc_to_remove (List[int]): List of indices of elements to remove.
        act_to_modify (List[int]): List of indices of elements to modify.
        act_to_add (List[int]): List of indices of elements to add.

    Returns:
        A_ (sparse.csr_matrix): The modified technosphere matrix with specified elements added with amounts fetched from the things that were removed.
    """
        
    amount = A_[exc_to_remove, act_to_modify]
    A_[act_to_add, act_to_modify] = amount

    return A_


def add_technosphere_loc(A_: sparse.csr_matrix, exc_to_remove: List[int], act_to_modify: List[int],
                     act_to_add: List[int], A_inds_rev:  dict) -> sparse.csr_matrix:
    """
    Add to the technosphere matrix new connections between existing and new activities with the same location.

    Args:
        A_ (spare.csr_matrix): A copy of the original technosphere matrix. -> Can be obtained from the function copy_technosphere
        exc_to_remove (List[int]): List of indices of elements to remove.
        act_to_modify (List[int]): List of indices of elements to modify.
        act_to_add (List[int]): List of indices of elements to add.
        A_inds_rev (dict): Reversed indices for activities.


    Returns:
        A_ (sparse.csr_matrix): The modified technosphere matrix with specified elements added with amounts fetched from the things that were removed.
    """
    for add in act_to_add:
        for modify in act_to_modify:
            if A_inds_rev[add][3] == A_inds_rev[add][3]:
                amount = A_[exc_to_remove[0], modify]
                A_[add, modify] = amount

    return A_
