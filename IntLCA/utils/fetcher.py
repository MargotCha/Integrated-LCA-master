from typing import List, Dict, Union


class ActivityFilter:
    def __init__(self, A_inds: Dict):
        self.A_inds = A_inds
        self.filtered_indices = set(A_inds.values())

    def starts(self, prefixes: Union[str, List[str]]) -> 'ActivityFilter':
        if isinstance(prefixes, str):
            prefixes = [prefixes]
        self.filtered_indices &= {
            int(j) for i, j in self.A_inds.items()
            if any(i[0].startswith(prefix) for prefix in prefixes)
        }
        return self

    def reference_product(self, substrings: Union[str, List[str]]) -> 'ActivityFilter':
        if isinstance(substrings, str):
            substrings = [substrings]
        self.filtered_indices &= {
            int(j) for i, j in self.A_inds.items()
            if any(substring in i[1] for substring in substrings)
        }
        return self

    def includes(self, substrings: Union[str, List[str]]) -> 'ActivityFilter':
        if isinstance(substrings, str):
            substrings = [substrings]
        self.filtered_indices &= {
            int(j) for i, j in self.A_inds.items()
            if any(substring in i[0] for substring in substrings)
        }
        return self

    def includes_all(self, substrings: Union[str, List[str]]) -> 'ActivityFilter':
        if isinstance(substrings, str):
            substrings = [substrings]
        self.filtered_indices &= {
            int(j) for i, j in self.A_inds.items()
            if all(substring in i[0] for substring in substrings)
        }
        return self

    def excludes(self, substrings: Union[str, List[str]]) -> 'ActivityFilter':
        if isinstance(substrings, str):
            substrings = [substrings]
        self.filtered_indices -= {
            int(j) for i, j in self.A_inds.items()
            if any(substring in i[0] for substring in substrings)
        }
        return self

    def location(self, substrings: Union[str, List[str]]) -> 'ActivityFilter':
        if isinstance(substrings, str):
            substrings = [substrings]
        self.filtered_indices &= {
            int(j) for i, j in self.A_inds.items()
            if any(substring in i[3] for substring in substrings)
        }
        return self

    def excluding_locations(self, substrings: Union[str, List[str]]) -> 'ActivityFilter':
        if isinstance(substrings, str):
            substrings = [substrings]
        self.filtered_indices -= {
            int(j) for i, j in self.A_inds.items()
            if any(substring in i[3] for substring in substrings)
        }
        return self

    def get_filtered_indices(self) -> List[int]:
        return list(self.filtered_indices)


