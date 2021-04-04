This repo is another in my series of MLops examples to show the basics, such as:
* Saving and loading a trained model
* Versioning models
* scikit-learn pipelines to bundle preprocessing and modeling
* Serving a model from a web service
* Hosting the web service
* Pull request / review concepts, like reviewing a model build, reviewing service changes, and basic testing for the service

This repo uses CDK to deploy machine learning models to an ECS cluster on EC2 with Docker.

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

* Get Github Actions deployment working - right now I'm just working with manual deployment.
    * First step - use the deployment user locally
* Test that the health endpoint is helpful if I break Docker
    * It sorta worked, though it took an hour to give up on unhealthy instances. And I had to do some weird memory configuration
    * Setup a timeout on the stack update, which would prevent a deploy from hanging when memory is misconfigured.
    * It worked correctly on a subsequent run
* Add something to CDK to prevent memory misconfiguration.
* https: To do this, I need to figure out how to make a certificate
* domain name: It looks like it'd work if I had a domain on Route53

# Notes on this version

* The initial `cdk synth` creates a lot of resources. I'm slightly worried that I don't understand it, though reading online it sounds like that's normal for ECS.
* `cdk` and PyCharm terminal don't play nice - better to run in a separate terminal window
* I've learned the hard way when the ECS task is defined with a memory requirement higher than what's available in the cluster, the deployment hangs, waiting for just the right node to show up in the cluster (which doesn't happen). If you CTRL-C the deployment, the service will still be stuck mid-deployment which prevents a new deploy. 
    * I've solved it by destroying and recreating the stack which makes a new URL.
    * I've also tried manually canceling the stack deploy after an hour, which causes an update rollback. The rollback has been stuck in progress for about 13 minutes. I couldn't cancel the rollback. Eventually I gave up and deleted the ECS Service that was stuck trying to update and after a few minutes CloudFormation updated the status of the Stack. Then I began `cdk destroy` again
* I also had problems binding gunicorn to port 80 so I changed ports.
* The first few requests to a newly deployed API can be significantly slower - why is that?

## Good things about ECS

* ECS doesn't swap to new code until it's proven healthy
* I'm confident that it could be configured to meet various company security requirements

## Bad things about ECS

* The CDK interface for ECS is error prone because it's designed to support clusters with multiple instance types.
* You have to do a bunch of work to setup https
* Deployments are slow

## EC2 vs Fargate

* I read that Fargate manages more for you but can cost more. From the options in CDK it doesn't look like it configures all that much more.
* Fargate could only be configured down to 1gb ram but EC2 could go lower.