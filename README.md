# Transform Metrics Repo
See full install instructions on the [install page](https://app.transformdata.io/install).

## Your First Metrics
Transform uses Github Workflows to validate and commit new versions of your metrics configs to our service. In this template repo, we've already set up these workflows for you in the `/.github` directory.

By default, we will run validation checks on open PRs, and commit new metric configs to Transform whenever a new commit is merged to the `main` branch.

You'll need to save the Transform API key for your Service User within the Github Secrets for this repo under `TRANSFORM_API_KEY={TRANSFORM_API_KEY}` for the above actions to work properly.

Please only keep the folder for your data warehouse.

## CLI Quick Start Guide
Some users prefer to set up a Python virtual environment in this directory, though this is optional:
```
python3 -m venv venv && source venv/bin/activate
```

Install the Transform client CLI:
```
pip3 install transform
```

To authenticate to Transform using the CLI, have your Transform API key handy
```
mql setup
```

## MQL CLI Example
List all metrics available:
```
mql list-metrics
```

Run the `revenue_usd` metric by day:
```
mql query --metrics revenue_usd --dimensions ds
```

Change the output to be odered by decending day:
```
mql query --metrics revenue_usd --dimensions ds --order -ds
```

Add the `country` dimension from the separate `customer` data source. Notice the `__` to indicate the join identifier:
```
mql query --metrics revenue_usd --dimensions ds --dimensions customer__country --order -ds
```

Run a ratio metric:
```
mql query --metrics cancellation_rate --dimensions ds --order -ds
