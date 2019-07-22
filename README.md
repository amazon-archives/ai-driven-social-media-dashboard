# AI-Driven Social Media Dashboard
Voice of customer analytics through social media: Build a social media dashboard using artificial intelligence and business intelligence services.

Organizations want to understand how customers perceive them and who those customers are. For example, what factors are driving the most positive and negative experiences for their offerings? Social media interactions between organizations and customers are a great way to evaluate this and deepen brand awareness. Understanding these conversations are a low-cost way to acquire leads, improve website traffic, develop customer relationships, and improve customer service. Since these conversations are all in unstructured text format, it is difficult to scale the analysis and get the full picture.

## OS/Python Environment Setup
```bash
sudo apt-get update
sudo apt-get install zip sed wget -y
```

## Building Lambda Package
```bash
cd deployment
./build-s3-dist.sh source-bucket-base-name version
```
source-bucket-base-name should be the base name for the S3 bucket location where the template will source the Lambda code from.
The template will append '-[region_name]' to this value.
version should be a version S3 key prefix
For example: ./build-s3-dist.sh solutions v1.0
The template will then expect the source code to be located in the solutions-[region_name]/ai-driven-social-media-dashboard/v1.0/

## CF template and Lambda function
Located in deployment/dist


***

Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.

Licensed under the Amazon Software License (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at

    http://aws.amazon.com/asl/

or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific language governing permissions and limitations under the License.
