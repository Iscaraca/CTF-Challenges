# Setup

All AWS services used are on the `ap-southeast-1` region. To change this, edit `tisc_chall/src/.aws/config` accordingly.

## Configuring the Lambda Function

Create an AWS account. Navigate to the console and create a lambda function `craft_query` with the `Node.js 18.x` runtime and the `x86_64` architecture. The handler should be at `index.handler`. Do not expose this function via a publically accessible API. Any other configuration details (e.g. memory) can be left up to the deployer.

Upload the code for the function by clicking on `Upload from -> .zip file`. The lambda function code is available at `tisc_chall/solution/craft_query.zip`.

## Configuring the IAM User

Create a new IAM policy, `craft_query_policy`. Edit the JSON to define these permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "lambda:ListFunctions",
                "lambda:GetFunction",
                "lambda:InvokeFunction"
            ],
            "Resource": "*"
        }
    ]
}
```

Create a new IAM user, `website`. Ensure console access is disabled, and no other form of credentials are generated except for access keys for the AWS CLI. Copy the access key and the secret access key and save them to `tisc_chall/src/.aws/credentials`. Attach `craft_query_policy` to the user.

## Deploying the app

The app is located in `tisc_chall/src`. Run

```bash
docker compose down -v && docker compose up --build
```

and access the app at `localhost:3000`. `server.js` and `db-init.sql` are available as downloadable files.