#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import importlib

# List of libraries to check
LIBRARIES = [
    "numpy",
    "matplotlib",
    "torch",
    "torchvision",
    "segmentation_models_pytorch",
    "ee",
    "rasterio",
    "geopandas",
    "osmnx",
    "jupyterlab"
]


def check_imports():
    """
    Checks if all required libraries can be imported.
    :return: True if all libraries are importable, False otherwise.
    """
    print("--- Starting import verification ---")
    all_ok = True
    missing = []

    for lib in LIBRARIES:
        try:
            importlib.import_module(lib)
            print(f"[OK] Library '{lib}' imported successfully.")
        except ImportError:
            print(f"[ERROR] Library '{lib}' NOT FOUND.")
            all_ok = False
            missing.append(lib)

    if not all_ok:
        print("\nERROR: Some libraries are missing.")
        print("Please install them in your 'coastal-mapper' environment.")
        print(f"Missing: {missing}")
        return False

    print("--- All libraries are installed. ---\n")
    return True


def check_gee_authentication():
    """Checks Google Earth Engine initialization."""
    print("--- Starting GEE verification ---")
    try:
        # Import ee library (already checked, but needed here)
        import ee

        # Try to initialize the API
        # If 'earthengine authenticate' succeeded, this works.
        ee.Initialize()

        print("[OK] Google Earth Engine authentication successful.")
        print("The API is ready.\n")

        # Final test: try to get some data
        collection = ee.ImageCollection("COPERNICUS/S2").limit(1)
        info = collection.getInfo()
        print("[OK] GEE data access test successful.")
        return True

    except ee.ee_exception.EEException as e:
        print(f"[ERROR] Earth Engine initialization failed: {e}")
        print("\n>>> Make sure you have run the following command")
        print(">>> in your terminal (with the env activated):")
        print(">>> earthengine authenticate")
        return False
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred with GEE: {e}")
        return False


# --- Script entry point ---
if __name__ == "__main__":
    print(f"Python environment verification: {sys.executable}")

    if "coastal-mapper" not in sys.executable:
        print("\nWarning: You are NOT running this script")
        print("from the 'coastal-mapper' Conda environment.")
        print("Results might be incorrect.")
        print("Make sure you have run 'conda activate coastal-mapper' first.\n")

    imports_ok = check_imports()

    if imports_ok:
        gee_ok = check_gee_authentication()

        if gee_ok:
            print("\n=================================================")
            print("[SUCCESS] Your Python environment is correctly set up!")
            print("=================================================")
        else:
            print("\n[FAILED] Problem with GEE authentication.")
    else:
        print("\n[FAILED] Problem with library installation.")
