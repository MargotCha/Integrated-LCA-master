from IntLCA.utils import instantiate, modifier, solver, saver
from IntLCA.utils.fetcher import ActivityFilter
from typing import List, Dict
import pandas as pd
import webbrowser
from typing import Union, List, Optional


class IntLCA:
    def __init__(self, project: str, scenarios: str, years: Union[str, List[str]], base_path: str, directory: Optional[str] = None, methods: Optional[Union[str, List[str], dict]] = None):
        """
        Initializes the IntLCA with project, scenarios, years, method, and directory.

        Args:
            project (str): Name of the project.
            scenarios (str): REMIND IAM scenarios that we are interested to look into. It can only be one that already has been installed by premise.
            years (Union[str, List[str]]): Years that we are interested to look into.
            base_path (str): Directory for fetching the databases.
            directory (Optional[str]): Directory for saving results. Default is None.
            methods (Optional[Union[str, List[str], dict]]): Method(s) for optimization. Default is None.
        """
        self.project = project
        self.scenarios = scenarios
        self.years = years
        self.base_path = base_path
        self.directory = directory
        self.methods = methods

    def access_data(self):
        """
        Import the data from the directories and create matrices.

        Returns:
        Matrices A, B, and indices dictionaries.
        """

        self.paths = instantiate.db_paths(self.base_path, self.scenarios, self.years)

        return self.paths
    
    def create_matrices(self, path):
        """            
        Create the matrices and the indices dictionaries.
        Returns:
        Matrices A, B, and indices dictionaries.
        """
        self.A, self.B, self.A_inds, self.B_inds, self.A_inds_rev, self.B_inds_rev = instantiate.matrices(path)

        return self.A, self.B, self.A_inds, self.B_inds, self.A_inds_rev, self.B_inds_rev


    def filtering(self, keys_to_add: List[Dict], keys_to_modify: List[Dict], keys_to_replace: List[Dict], keys_to_run: List[Dict]):
        """
        Filter the activities based on the given criteria.

        Returns:
        Tuple[List[int], List[int], List[int], List[int]]: Indices to remove, modify, add, and run.
        """
        def apply_filters(activities, keys):
            for key in keys:
                for filter_type, value in key.items():
                    if filter_type == 'starts':
                        activities.starts(value)
                    elif filter_type == 'includes':
                        activities.includes(value)
                    elif filter_type == 'reference_product':
                        activities.reference_product(value)
                    elif filter_type == 'includes_all':
                        activities.includes_all(value)
                    elif filter_type == 'excludes':
                        activities.excludes(value)
                    elif filter_type == 'location':
                        activities.location(value)
                    elif filter_type == 'excluding_locations':
                        activities.excluding_locations(value)
            return activities.get_filtered_indices()

        activities = ActivityFilter(self.A_inds)
        act_to_add = []
        for key_group in keys_to_add:
            activities = ActivityFilter(self.A_inds)
            act_to_add.extend(apply_filters(activities, key_group))

        activities = ActivityFilter(self.A_inds)
        act_to_modify = []
        for key_group in keys_to_modify:
            activities = ActivityFilter(self.A_inds)
            act_to_modify.extend(apply_filters(activities, key_group))

        activities = ActivityFilter(self.A_inds)
        exc_to_remove = []
        for key_group in keys_to_replace:
            activities = ActivityFilter(self.A_inds)
            exc_to_remove.extend(apply_filters(activities, key_group))

        activities = ActivityFilter(self.A_inds)
        act_to_run = []
        for key_group in keys_to_run:
            activities = ActivityFilter(self.A_inds)
            act_to_run.extend(apply_filters(activities, key_group))

        return self.exc_to_remove, self.act_to_modify, self.act_to_add, self.act_to_run
    

    def copy_technosphere(self):
        """
        Copy the technosphere matrix to make changes.
        """
        self.A_ = modifier.copy_technosphere(self.A)

        return self.A_

    def modify_technosphere_remove(self, exc_to_remove: List[int], act_to_modify: List[int]):
        """
        Modify the technosphere matrix by removing specified elements.

        Args:
            exc_to_remove (List[int]): List of indices of elements to remove.
            act_to_modify (List[int]): List of indices of elements to modify.
            act_to_add (List[int]): List of indices of elements to add.
        """
        self.A_ = modifier.remove_technosphere(self.A, exc_to_remove, act_to_modify)

        return self.A_
    
    def modify_technosphere_add(self, exc_to_remove: List[int], act_to_modify: List[int], act_to_add: List[int]):
        """
        Modify the technosphere matrix by removing specified elements.

        Args:
            exc_to_remove (List[int]): List of indices of elements to remove.
            act_to_modify (List[int]): List of indices of elements to modify.
            act_to_add (List[int]): List of indices of elements to add.
        """
        self.A_ = modifier.add_technosphere(self.A_, exc_to_remove, act_to_modify, act_to_add)

        return self.A_

    def modify_technosphere_add_loc(self, exc_to_remove: List[int], act_to_modify: List[int], act_to_add: List[int]):
        """
        Modify the technosphere matrix by removing specified elements.

        Args:
            exc_to_remove (List[int]): List of indices of elements to remove.
            act_to_modify (List[int]): List of indices of elements to modify.
            act_to_add (List[int]): List of indices of elements to add.
        """
        self.A_ = modifier.add_technosphere_loc(self.A_, exc_to_remove, act_to_modify, act_to_add)

        return self.A_

    def LCIA(self):
        """
        Generate a list of characterization factor (CF) vectors for Life Cycle Impact Assessment (LCIA) based on the given methods.

        Returns:
        List of CF vectors.
        """
        cf_dict = {}
        for method in self.methods:
            CF = instantiate.CF_vector(self.project, self.B, self.B_inds, method)
            self.cf_dict[method] = CF

        return self.cf_dict

    def calculate(self, act_to_run: int, FU: int):
        """
        Calculate the results for one activity and several methods.

        Args:
            act_to_run (List[int]): List of indices representing the truck fleet.
            CF (List[int]): List of characterization factors.
            FU (int): Functional unit.
        """
        self.CF_dict = self.LCIA()
        self.results, self.contribution, self.s = solver.simple_calculation(act_to_run, self.A_inds_rev, self.CF_dict, FU, self.A_, self.B)

        return self.results, self.contribution, self.s

    def breakdown(self, act_to_run: int, FU: int, results, act_tech:tuple):
        """
        Calculate the breakdown results for one activity and several methods.

        Args:
            act_to_run (List[int]): List of indices representing the truck fleet.
            FU (int): Functional unit.
            act_tech (tuple): Tuple of activity that we are interested to look into.
            results (List): List of results.
        """
        self.CF_dict = self.LCIA()
        self.dfs = solver.breakdown_calculation(act_to_run, self.A_inds_rev, self.CF_dict, FU, self.A_, self.B, results, act_tech)
        return self.dfs

    def multi_calc(self, FU: int):
        """
        Calculate the results for multiple activities and methods.

        Args:
            act_to_run (List[int]): List of indices representing the truck fleet.
            FU (int): Functional unit.

        """
        self.CF_dict = self.LCIA()
        self.dfs = solver.multi_calculation(self.act_to_run, self.A_inds_rev, self.CF_dict, FU, self.A_, self.B)

        return self.dfs

    def overall_calc(self, lca_instance, FU: int) -> pd.DataFrame:
        self.CF_dict = self.LCIA()
        self.dfs = solver.super_calculation(
            lca_instance,
            self.act_to_run,
            self.exc_to_remove,
            self.act_to_modify,
            self.act_to_add,
            self.A_inds_rev,
            self.CF_dict,
            FU,
            self.A,
            self.B
        )
        return self.dfs


    def organize_results(self, results):
        """
        Organize the results in a DataFrame.

        Args:
            results (List[float]): The results of the calculations.
            classify_ds_names (Callable): The function to classify the activities.
        """
        self.results = saver.classify_ds_names(results)

        return self.results


    def save_results(self, name: str, df: pd.DataFrame, s: Optional[pd.DataFrame] = None, contribution: Optional[pd.DataFrame] = None):
        """
        Save the results to an Excel file.

        Args:
            name (str): The name of the Excel file.
            df (pd.DataFrame): The DataFrame to save.
            s (Optional[pd.DataFrame]): The scaling factor DataFrame. Default is None.
            contribution (Optional[pd.DataFrame]): The process contribution DataFrame. Default is None.
        """
        if s is None:
            s = self.s
        if contribution is None:
            contribution = self.contribution

        saver.save(name, self.directory, s, contribution, df)


def example_notebook():
    """
    Opens the diesel example notebook in the web browser.
    """
    github_url = 'https:/github.com/MargotCha/Integrated-LCA-master/tree/main/Notebooks/Examples/example_notebook.ipynb'
    nbviewer_url = 'https://nbviewer.jupyter.org/github/' + github_url.split('github.com/')[1]
    webbrowser.open(nbviewer_url)
