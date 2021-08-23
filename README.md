# Dashboard Config

This repository is an example of a GitHub Actions workflow and group of sites configuration files that
generates and stores metadata configuation files file for use in the dashboard-api-maap.

## Configuration

### Datasets

The `datasets` directory contains a directory for the available datasets. Each dataset is a `json` file (see example: [datasets/MOD13A1.006.json](./datasets/MOD13A1.006.json))

All the datasets inside the directory are read a input dataset to the dashboard.

#### Helper to add datasets to the dashboard

The `helpers` directory contains:

- `dataset_json_generator.py`: An interactive script that generates the json for the dataset
- `requirements.txt`: Requirements to run `dataset_json_generator.py`
- `test_raster_dataset.ipynd`: An interactive notebook to test visualization of raster dataset

### Sites

The `sites` directory contains a directory for each site. Within each site directory, there are two files:

1. site.json - a description of the site
2. summary.html - an HTML fragment that's used as the summary description for this site in the dashboard

Each site directory must be included in the `SITES` array in config.yml. 

The `global` site is used for the default global dashboard configuration.

## Datasets Usage

### Manual Execution

This will create the datasets metadata file and copy it to the S3 location indicated in `BUCKET` and print the final JSON description.

1. Update config.yml with the appropriate BUCKET and DATASETS configuration
2. Export a shell variable for `STAGE`, e.g., `export STAGE=local`
3. Run the dataset metadata generator.

```bash
export STAGE=local
python dataset_metadata_generator/src/main.py | jq .
```


## Sites Usage 

### Manual Execution

This will copy the file to the S3 location indicated in `BUCKET` and print the final JSON description.

1. Update config.yml with the appropriate BUCKET and SITES configuration
2. Export a shell variable for `STAGE`, e.g., `export STAGE=local`
3. Run the sites generator.

```bash
export STAGE=local
python sites_generator/main.py | jq .
```

### Execution via GitHub Actions

1. In the GitHub repository, add secrets (Settings -> Secrets) for accessing AWS (AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY)
2. Update config.yml with the appropriate BUCKET and SITES configuration.
3. Push config.yaml to GitHub and verify it runs correctly. Note only branches configured in `.github/workflows.yml` will run the workflow (e.g. generate the sites metadata files).
