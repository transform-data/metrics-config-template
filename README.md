# Transform Metrics Repo
Welcome to your new Transform Project! See full install instructions on the [install page](https://app.transformdata.io/install) to get started using Transform.

## Resources
* Learn more about Transform [in the docs](https://www.notion.so/transformdata/Transform-Documentation-4eb96a3207634834ab1ae8b5b23923ff)
* Reach out to our team at [support@transformdata.io](mailto:support@transformdata.io) for support or to setup a shared slack channel

## Configure Github Workflows
Transform uses Github Workflows to validate and commit new versions of your metrics configs to our service. In this template repo, we've already set up these workflows for you in the `/.github` directory.

By default, we will run validation checks on open PRs, and commit new metric configs to Transform whenever a new commit is merged to the `main` branch.

You'll need to save the Transform API key for your Service User within the [Github Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository) for this repo under `TRANSFORM_API_KEY={TRANSFORM_API_KEY}` for the above actions to work properly.

<img width="1782" alt="Screen Shot 2022-08-22 at 3 05 27 PM" src="https://user-images.githubusercontent.com/48079901/186027082-7eb6010a-dc97-4af4-ad90-701ced95c8d3.png">

## Configure BitBucket Pipelines
Transform also uses BitBucket Pipelines to validate and commit new versions of your metrics configs to our service. In this template repo, we've already set up these workflows for you in the `bitbucket-pipelines.yml` file.

By default, we will run validation checks on open PRs, and commit new metric configs to Transform whenever a new commit is merged to the `main` or `master` branch.

You'll need to save the Transform API key for your Service User within the [BitBucket Variables](https://support.atlassian.com/bitbucket-cloud/docs/variables-and-secrets/#User-defined-variables) for this repo under `TRANSFORM_API_KEY={TRANSFORM_API_KEY}` for the above actions to work properly.

<img width="1792" alt="Screen Shot 2022-08-11 at 4 40 12 PM" src="https://user-images.githubusercontent.com/48079901/184261300-5c7cb5c6-347c-4228-ac13-af41afe53524.png">

## Configure GitLab Pipelines
Transform also uses GitLab Pipelines to validate and commit new versions of your metrics configs to our service. In this template repo, we've already set up these workflows for you in the `.gitlab-ci.yml` file.

By default, we will run validation checks on open PRs, and commit new metric configs to Transform whenever a new commit is merged to your default branch.

You'll need to save the Transform API key for your Service User within the [GitLab Variables](https://docs.gitlab.com/ee/ci/variables/) for this repo under `TRANSFORM_API_KEY={TRANSFORM_API_KEY}` for the above actions to work properly.

<img width="1782" alt="Screen Shot 2022-08-25 at 10 56 52 AM" src="https://user-images.githubusercontent.com/48079901/186736411-a3dde080-5aae-4dcb-b609-8cb5b697bdd4.png">

## Optional: Integrating Into An Existing Repository

Rather than storing your configs in a new repo, you can store them in specific directory within an existing repo. In addition to configuring the Github/Gitlab/Bitbucket Workflows & Pipelines above, you'll need to save the path to the directory of configs (relative to the repo-root, unquoted), within the Github Secrets/Gitlab Variables/Bitbucket Variables for this existing repo under `TRANSFORM_CONFIG_DIR={TRANSFORM_CONFIG_DIR}` for the above actions to work properly.

## CLI Quick Start Guide

Some users prefer to set up a Python virtual environment in this directory, though this is optional:
```
python3 -m venv venv && source venv/bin/activate
```

1. Install the Transform client CLI:
```
pip install transform_mql
```

2. To authenticate to Transform MQL server using the CLI, navigate to this directory and run
```
mql setup
```
You will be asked to provide the API you created during setup, so have it handy.
## MQL CLI Example
Below is a list of common MQL commands.

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
