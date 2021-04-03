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

1. Install Terraform and run the code in `infrastructure`. This creates an S3 bucket for DVC and an IAM user for Github Actions. Be sure to find and save: the S3 bucket name, the IAM user ID, and the IAM user secret key.
1. Edit `.dvc/config` and point it to your new S3 bucket.
1. Setup `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` in your Github Secrets for the repo so Github Actions can use them.
1. If you haven't run `cdk bootstrap` on your AWS account, do that.
1. Train a model - it's probably easiest to edit anything under `training` and make a PR to trigger github to build it
1. After it's done training and you merge it, it'll deploy to your AWS account.

# What's where?


# TO DO

# Notes on this version

