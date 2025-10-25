# Coastal-Mapper: A Proof-of-Concept for Low-Cost Deep Learning-Based Coastal Delineation

## 1. Research Context and Problem Statement

Coastal zones are among the most dynamic and critical environments on Earth, facing increasing pressure from climate change, erosion, and anthropogenic activity. Accurate and timely monitoring of the coastline (the Land/Sea interface) is fundamental for risk assessment, resource management, and environmental modeling.

While high-resolution methods like LiDAR and manual GPS surveys provide high-accuracy "ground-truth," they are expensive, time-consuming, and operationally difficult to scale. Conversely, traditional remote sensing methods (e.g., spectral indices like NDWI) are scalable but often fail in complex areas (e.g., tidal flats, high-sediment waters, shadows).

Deep Learning, specifically semantic segmentation, has shown state-of-the-art (SOTA) performance. However, SOTA models often rely on large, manually annotated datasets, which re-introduces a significant bottleneck.

## 2. Project Objectives and Core Hypothesis

This project serves as a foundational **Proof-of-Concept (POC)** to investigate a scalable, low-cost alternative.

**Primary Objective:** To develop and evaluate an automated pipeline for binary (Land/Sea) coastal segmentation by training a U-Net architecture.

**Core Hypothesis:** This project hypothesizes that an effective segmentation model can be trained using **freely available, large-scale, but inherently noisy 'ground-truth' data** sourced from OpenStreetMap (OSM), in conjunction with open-access Sentinel-2 imagery from Google Earth Engine (GEE).

The key contribution is the exploration of a *fully automated, low-cost pipeline* that minimizes human intervention and assesses the viability of "crowd-sourced" data (OSM) as a substitute for expert-labeled masks.

## 3. Long-Term Research Vision

This POC is the *first exploratory step* toward a more ambitious, long-term research goal: **developing novel Deep Learning architectures for 4D coastal monitoring (3D space + time)**.

The insights gained from this project (e.g., model performance vs. label noise, temporal data handling) will directly inform future work on:
* **Super-Resolution:** Enhancing 10m satellite data.
* **Multi-Modal Data Fusion:** Architectures capable of integrating heterogeneous data sources (e.g., Sentinel-1 SAR, Satellite imagery, low-altitude Drone data, and sparse LiDAR).
* **Temporal Dynamics:** Moving from static composites to time-series analysis for monitoring erosion, accretion, and tidal impacts.

This project is intended to build the fundamental skills and baseline metrics required for M1/M2-level research (e.g., TER, internship) in this domain.

## 4. Current Project Status (End of Step 4)

* [x] **Step 1:** Conda environment defined and validated.
* [x] **Step 2:** Ground-Truth (Vector): OSM vector coastline data has been downloaded (`data/osm_coastline.gpkg`).
* [x] **Step 3:** Input Data (Raster X): A Sentinel-2 median composite image has been generated via GEE (`data/S2_Composite_AOI.tif`).
* [x] **Step 4:** Ground-Truth (Raster Y): A perfectly aligned binary "sea" mask has been generated (`data/mask_sea.tif`).
* [ ] **Step 5:** Tiling (Patch Generation): Splitting the large rasters into training patches (e.g., 256x256).
* [ ] **Step 6:** Model Implementation: Implementing the PyTorch `Dataset`, `DataLoader`, and U-Net training loop.
* [ ] **Step 7:** Model Evaluation: Training the model and analyzing its performance (IoU).

## 5. Project Structure

```
coastal-mapper/
│
├── data/                       # Input data (raster and vector)
│   ├── S2_Composite_AOI.tif    # Sentinel-2 composite
│   ├── osm_coastline.gpkg      # OSM coastline vector data
│   └── mask_sea.tif            # Generated binary sea mask
│
├── notebooks/                  # Jupyter notebooks for each step
│   ├── 01_data_acquisition.ipynb
│   ├── 02_mask_generation.ipynb
│   └── 03_tiling_and_preprocessing.ipynb
│
├── .gitignore                  # Git ignore file
├── environment.yml             # Conda environment definition
├── requirements.txt            # Python dependencies
├── README.md                   # Project overview and instructions
├── LICENSE                     # License information
├── aoi.geojson                 # Area of Interest definition
└── check_environment.py        # Script to verify environment setup
```

## 6. Methodology (Data Pipeline Steps 1-4)

The methodology focuses on creating a spatially-aligned (X, Y) pair from heterogeneous data sources.

1.  **Input Data (X):** A cloud-filtered, median composite of Sentinel-2 (L2A, 10m bands: B2, B3, B4, B8) is generated via the GEE API for a user-defined `aoi.geojson`. The composite is exported in a local UTM CRS (auto-detected) to ensure metric pixel spacing (10m x 10m).
2.  **Ground-Truth (Raw Y):** Vector lines tagged `natural=coastline` are extracted from OpenStreetMap using the `osmnx` library.
3.  **Preprocessing (Target Y):** This is the core data engineering task. The OSM vector lines (in EPSG:4326) are reprojected to the S2 image's UTM CRS. A vector-to-raster conversion is then performed by:
    a.  Splitting the raster's bounding box polygon using the reprojected coastline vector.
    b.  Applying a heuristic (largest resulting area) to identify the 'Sea' polygon.
    c.  **Rasterizing** this 'Sea' polygon (value=1) onto a 'Land' (value=0) array, using the S2 image's exact georeferencing (transform and shape) via `rasterio`.

This process results in `mask_sea.tif`, a binary mask that is **perfectly aligned at the pixel level** with `S2_Composite_AOI.tif`.

---

## 7. Installation and Replication

This project uses **Conda** to manage the complex geospatial and deep learning libraries.

1.  **Create and activate the Conda environment:**
    ```bash
    conda create -n coastal-mapper python=3.12 -y
    conda activate coastal-mapper
    ```
    
2.  **Install dependencies:**
    ```bash
    conda install --file requirements.txt -y
    ```
    Or use the provided `environment.yml`:
    ```bash
    conda env create -f environment.yml
    conda activate coastal-mapper
    ```
    
3.  **Authenticate with Google Earth Engine:**
    (One-time setup)
    ```bash
    earthengine authenticate
    ```
    
4.  **Validate the Environment:**
    ```bash
    python check_environment.py
    ```
    

## 8. Next Steps (Experimental Phase)

The project is poised to enter the deep learning phase.

* **Step 5: Tiling (Patch Generation):** The large rasters (X and Y) will be tiled into smaller, uniform patches (e.g., 256x256) to create the training, validation, and test datasets. A **spatial split** (non-overlapping geographic zones) will be used, rather than a random shuffle, to ensure the model's generalization capabilities are properly tested.
* **Step 6: Model Implementation:** A U-Net model will be implemented in PyTorch, leveraging the `segmentation-models-pytorch` library (with a pre-trained ResNet backbone).
* **Step 7: Experimental Protocol:** A robust training and validation loop will be developed, using appropriate loss functions (e.g., BCE + Dice Loss) and metrics (Intersection over Union - IoU) to formally evaluate the hypothesis.

## 9. License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 10. Acknowledgments

This project builds upon open-source libraries and datasets, including Google Earth Engine, OpenStreetMap, Rasterio, Geopandas, and PyTorch. Special thanks to the open-source community for their invaluable contributions.

## 11. Contact

For questions or collaboration inquiries, please contact [ME](mailto:anthony.mudet@etu.univ-nantes.fr).