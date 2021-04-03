This repo is another in my series of MLops examples to show the basics, such as:
* Saving and loading a trained model
* Versioning models
* scikit-learn pipelines to bundle preprocessing and modeling
* Serving a model from a web service
* Hosting the web service
* Pull request / review concepts, like reviewing a model build, reviewing service changes, and basic testing for the service

This repo uses CDK for deployment to EC2/Fargate with Docker.

# Setup

I've only set this up once so take this with a grain of salt.

1. Install Terraform and run the code in `infrastructure`. This creates an S3 bucket for DVC and an IAM user for Github Actions. Be sure to find and save: the S3 bucket name, the IAM user ID, and the IAM user secret key. `terraform init` `terraform apply`
1. Edit `.dvc/config` and point it to your new S3 bucket.
1. Create a local pipenv to make it easier to code `make setup-development-pipenv`
   1. (For forgetful people like me) Realize that the latest OS update uninstalled xcode developer tools again and run `xcode-select --install` to get pipenv working again
1. Create the github repo 
1. Setup `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` in your Github Secrets for the repo so Github Actions can use them.
1. If you haven't run `cdk bootstrap` on your AWS account, do that.
1. Train a model - it's probably easiest to edit anything under `training` and make a PR to trigger github to build it
1. After it's done training and you merge it, it'll deploy to your AWS account.

# What's where?


# TO DO

* Switch to FastAPI. If I've setup this repo right, it should be possible to do a zero-downtime change

# Notes on this version

* The initial `cdk synth` creates a lot of resources. I'm slightly worried that I don't understand it, though that's probably no different than lambda or heroku
* `cdk` and PyCharm terminal don't play nice - better to run in a separate terminal window
* The initial `cdk deploy` got stuck. I'm not sure what I did wrong but it got stuck on ECS service creation for 30 minutes. I checked and the ECS nodes came up. A bit of searching online suggested that maybe I configured it in such a way that it could never become healthy.
  * Attempt 2: Found that there was insufficient memory for the task. I'm rounding it down from 2048 to 2000 and increasing the instance type. 
* I wasn't sure how to choose between the EC2 and Fargate templates. I picked the EC2 one because I could pick the instance type and feel good about keeping the cost low.