This repo is another in my series of MLops examples to show the basics, such as:
* Saving and loading a trained model
* Versioning models
* scikit-learn pipelines to bundle preprocessing and modeling
* Serving a model from a web service
* Hosting the web service
* Pull request / review concepts, like reviewing a model build, reviewing service changes, and basic testing for the service

This repo uses CDK to deploy machine learning models to an ECS cluster on EC2 with Docker.

# Setup


1. Install Terraform and run the code in `infrastructure`. This creates an S3 bucket for DVC and an IAM user for Github Actions. Be sure to find and save: the S3 bucket name, the IAM user ID, and the IAM user secret key. `terraform init` `terraform apply`
1. Edit `.dvc/config` and point it to your new S3 bucket.
1. Create a local pipenv to make it easier to code - run `make setup-development-pipenv`
   1. (For forgetful people like me) Realize that the latest OS update uninstalled xcode developer tools again and run `xcode-select --install` to get pipenv working again
1. Create the github repo 
1. Setup `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` in your Github Secrets for the repo so Github Actions can use them.
1. If you haven't run `cdk bootstrap` on your AWS account, do that.
1. Train a model - it's probably easiest to edit anything under `training` and make a PR to trigger github to build it. You could also do it locally.
1. After it's done training and you merge it, it'll deploy to your AWS account.

# What's where?

* `.dvc`: Configuration for DVC, which is how we version models and link the model versions to git
* `.github`: Configuration for the CI/CD pipeline in Github Actions
* `infrastructure`: This sets up AWS resources for the repo and makes a user to run the deployments
* `serving/app`: The actual web service code
* `serving/app/data`: The model is stored here
* `serving/deployment`: CDK code to create resources needed for hosting the model and deploy the code/data
* `serving/tests`: Minimal tests to make sure the code can load the model and that the health check is working
* `training`: Code to build the model

# TO DO

* Check that the deployment user has permissions to create/update the ECS cluster
* Add a check to prevent memory misconfiguration in CDK
* https

# Notes on this version

* The initial `cdk synth` creates a lot of resources. I'm slightly worried that I don't understand it, though reading online it sounds like that's normal for ECS.
* `cdk` and PyCharm terminal don't play nice - better to run in a separate terminal window
* When the ECS task is defined with a memory requirement higher than what's available in the cluster, the deployment hangs, waiting for just the right node to show up in the cluster (which doesn't happen). If you CTRL-C the deployment, the service will still be stuck mid-deployment which also prevents any new deployments. 
    * One time I solved it by destroying and recreating the stack, but that's not ideal.
    * Another time I tried manually canceling the stack deploy, which triggers an update rollback. But then it got stuck in updating. I had to manually delete the ECS Service at that point to even run `cdk destroy`.
* I had problems binding gunicorn to port 80 so I changed to 8000
* The first few requests to a newly deployed API can be significantly slower - why is that? Is that the service? Or Postman?
* Notes on health checking with circuit breaker
    * One time it got stuck waiting for new instances to appear and auto scaling didn't seem to be running, so I had to manually increase to 2 instances and then it deployed and cycled through failed health checks a few times before finally the status was updated to a failed state. 
    * The health check logic worked correctly on a subsequent run


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