import pandas as pd
import os


def classify_ds_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Classify the activities you run calculations for based on the names.

    Returns:
    DataFrame: The DataFrame with classified activities.
    """
    df.loc[df["Technology"].str.contains("from atmosphere"), "CO2"] = "DAC"
    df.loc[df["Technology"].str.contains("DAC"), "CO2"] = "DAC"
    df.loc[df["Technology"].str.contains("direct air capture"), "CO2"] = "DAC"
    df.loc[df["Technology"].str.contains("post-combustion"), "CO2"] = "post-combustion"
    df.loc[df["Technology"].str.contains("pre-combustion"), "CO2"] = "pre-combustion"
    df.loc[df["Technology"].str.contains("electrolysis"), "hydrogen"] = "electrolysis"
    df.loc[(df["Technology"].str.contains("steam methane")) & (
        df["Technology"].str.contains("biomethane")), "hydrogen"] = "SMR - biomethane"
    df.loc[(df["Technology"].str.contains("steam methane")) & (
        df["Technology"].str.contains("natural gas")), "hydrogen"] = "SMR - natural gas"
    df.loc[(df["Technology"].str.contains("auto-thermal")) & (
        df["Technology"].str.contains("natural gas")), "hydrogen"] = "ATR - natural gas"
    df.loc[(df["Technology"].str.contains("auto-thermal")) & (
        df["Technology"].str.contains("biomethane")), "hydrogen"] = "ATR - biomethane"
    df.loc[(df["Technology"].str.contains("gasification of woody biomass")), "hydrogen"] = "gasification - biomass"
    df.loc[(df["Technology"].str.contains("hard coal gasification")), "hydrogen"] = "gasification - hard coal"
    df.loc[df["Technology"].str.contains("mix"), "electricity"] = "grid"
    df.loc[df["Technology"].str.contains("onshore"), "electricity"] = "wind - onshore"
    df.loc[df["Technology"].str.contains("offshore"), "electricity"] = "wind - offshore"
    df.loc[df["Technology"].str.contains("nuclear"), "electricity"] = "nuclear"
    df.loc[df["Technology"].str.contains("hydro, pumped"), "electricity"] = "hydro, pumped storage"
    df.loc[df["Technology"].str.contains("hydro, reservoir, alpine"), "electricity"] = "hydro, reservoir, alpine"
    df.loc[df["Technology"].str.contains("hydro, reservoir, non-alpine"), "electricity"] = "hydro, reservoir, non-alpine"
    df.loc[df["Technology"].str.contains("hydro, run-of-river"), "electricity"] = "hydro, run-of-river"
    df.loc[df["Technology"].str.contains("solar"), "electricity"] = "solar"
    df.loc[df["Technology"].str.contains("BECCS"), "electricity"] = "BECCS"
    df.loc[df["Technology"].str.contains("Alkaline"), "electrolyzer"] = "Alkaline"
    df.loc[df["Technology"].str.contains("PEM"), "electrolyzer"] = "PEM"
    df.loc[df["Technology"].str.contains("waste heat"), "heat"] = "waste"
    df.loc[df["Technology"].str.contains("industrial steam heat"), "heat"] = "industrial steam heat"
    df.loc[df["Technology"].str.contains("heat pump heat"), "heat"] = "heat pump heat"
    df.loc[df["Technology"].str.contains("CCS"), "CCS"] = True

    return df

def save(name: str, directory: str, s: pd.DataFrame, contribution: pd.DataFrame, results: pd.DataFrame) -> None:
    """
    Save the DataFrame to an Excel file.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        name (str): The name of the Excel file.
        directory (str): The directory where the results folder will be created.
        s (pd.DataFrame): The scaling factor DataFrame.
        contribution (pd.DataFrame): The process contribution DataFrame.
        results (pd.DataFrame): The results DataFrame.
    """

    # Ask the user whether to create an Excel file with one sheet or three sheets
    choice = input("Do you want to create an Excel file with one sheet (results only) or three sheets (results, scaling factor, process contribution)? Enter 'one' or 'three': ").strip().lower()

    # Create the results folder
    results_folder = os.path.join(directory, 'results')
    os.makedirs(results_folder, exist_ok=True)

    # Create an Excel file based on the user's choice
    excel_path = os.path.join(results_folder, f'{name}.xlsx')
    with pd.ExcelWriter(excel_path) as writer:
        if choice == 'one':
            results.to_excel(writer, sheet_name='Results', index=False)
        elif choice == 'three':
            results.to_excel(writer, sheet_name='Results', index=False)
            s.to_excel(writer, sheet_name='Scaling factor', index=False)
            contribution.to_excel(writer, sheet_name='Process contribution', index=False)
        else:
            print("Invalid choice. Please enter 'one' or 'three'.")
