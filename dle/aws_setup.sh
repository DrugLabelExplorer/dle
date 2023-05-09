#!/bin/bash
#
#

DB_ENDPOINT=`aws ssm get-parameters --names rds_endpoint --region us-east-1 | jq -r '.Parameters[0].Value'`
ECS_LB=`aws ssm get-parameters --names ecs_lb --region us-east-1 | jq -r '.Parameters[0].Value'`
EC2_IP=`aws ssm get-parameters --names ec2_ip --region us-east-1 | jq -r '.Parameters[0].Value'`
RDS_PW=`aws ssm get-parameters --names rds_pw --region us-east-1 | jq -r '.Parameters[0].Value'`
ELASTIC_PW=`aws ssm get-parameters --names elastic_pw --region us-east-1 | jq -r '.Parameters[0].Value'`
KIBANA_PW=`aws ssm get-parameters --names kibana_pw --region us-east-1 | jq -r '.Parameters[0].Value'`





mv .env.example .env

sed '/DATABASE.*/d' -i .env
sed '/PROVISION_ES.*/d' -i .env
sed '/ELASTICSEARCH_URL.*/d' -i .env
sed '/ELASTIC_PASSWORD.*/d' -i .env
sed '/KIBANA_PASSWORD.*/d' -i .env


sed '/.*ca_certs.*/d' -i dle/settings.py
sed '/.*ssl.TLSVersion.TLSv1_2.*/d' -i dle/settings.py




echo "DATABASE_URL=\"postgres://postgres:$RDS_PW@$DB_ENDPOINT:5432/postgres\"" >> .env
echo "API_ENDPOINT=\"$EC2_IP\"" >> .env
echo "ALLOWED_HOSTS=\"$EC2_IP, $ECS_LB\"">> .env
echo "PROVISION_ES=False" >> .env
echo "ELASTICSEARCH_URL=http://$EC2_IP:9200" >> .env
echo "ELASTIC_PASSWORD=$ELASTIC_PW" >> .env
echo "KIBANA_PASSWORD=$KIBANA_PW" >> .env