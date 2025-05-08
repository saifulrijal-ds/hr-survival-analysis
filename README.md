# hr-survival-analysis
## Basic Setup
### 1. Creating a Dagshub Repository from GitHub
First, you'll need to connect your existing GitHub repository to DagsHub:

1. Sign in to [DagsHub](https://dagshub.com/) using your account
2. Click the "**Create +**" button in the top navigation bar
3. Select "**Connect a repository**"
4. Choose "Github" and click "**connect**"
5. Authorize your Github user
6. Select your GitHub repository "hr-survival-analysis"
7. Click "**Connect Repository**"

### 2. Python packages installation
1. Install `pipenv`
    ```bash
    pip install pipenv
    # or
    conda install conda-forge::pipenv
    ```
2. Install packages from Pipfile
    ```bash
    pipenv install
    ```
### 3. Set up DVC with DagsHub as remote
1. Initialize DVC
    ```bash
    dvc init
    ```
2. Verify initialization was succesful
    ```bash
    ls -la .dvc
    ```
3. Configure DVC with DagsHub as remote storage, using S3 protocol:
    ```bash
    # Add DagsHub's S3-compatible storage as a default remote
    dvc remote add -d dagshub s3://dvc

    # Configure the endpoint URL
    dvc remote modify dagshub endpointurl https://dagshub.com/<username>/<repo_name>.s3

    # Configure authentication (locally so tokens aren't committed to Git)
    dvc remote modify origin --local access_key_id your_token
    dvc remote modify origin --local secret_access_key your_token
    ```
4. Commiting DVC initialization to Git
    ```bash
    # Add the DVC config files
    git add .dvc .gitignore

    # Commit the changes
    git commit -m "Initialize DVC configuration"

    ```

