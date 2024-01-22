#!/bin/bash

GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CLEAR='\033[0m'

echo -e "${YELLOW}[!]${CLEAR} Setting up kCTF"
gcloud auth configure-docker
source kctf/activate
kctf cluster load remote-cluster
python3 ./scripts/start_challenges.py
kubectl apply -f nginx.yaml >/dev/null
echo -e "${GREEN}[-]${CLEAR} Starting/stopping challenges"
jq 'map_values(select(.started == false))|keys[]' challenges.json -c -r | while read d; do 
  # Check if chal is started
  cd $d 
  if [[ ! $(kctf chal status 2>&1) =~ "NotFound" ]]; then
    echo -e "${YELLOW}[*]${CLEAR} Stopping ${BLUE}$d${CLEAR}"
    kctf chal stop
  else
    echo -e "${YELLOW}[*]${CLEAR} Skipping ${BLUE}$d${CLEAR} (not running)"
  fi
  cd ..
done
jq 'map_values(select(.started == true))|keys[]' challenges.json -c -r | while read d; do 
  cd $d 
  # Check if chal is started 
  if [[ $(kctf chal status 2>&1) =~ "NotFound" ]]; then
    echo -e "${YELLOW}[*]${CLEAR} Starting ${BLUE}$d${CLEAR} (not started)"
    kctf chal start >/dev/null
  else 
    # Were any files in this dir modified this commit?
    if [[ $(git diff --name-only HEAD HEAD~1 .) ]]; then
      echo -e "${YELLOW}[*]${CLEAR} Starting ${BLUE}$d${CLEAR} (updated)"
      kctf chal start >/dev/null
    else
      echo -e "${YELLOW}[*]${CLEAR} Skipping ${BLUE}$d${CLEAR} (already running)"
    fi
  fi 
  cd ..
done
echo -e "${GREEN}[-]${CLEAR} Packaging challenges"
jq 'map_values(select(.package == false | not)) | keys[]' challenges.json -c -r | while read d; do 
  echo -e "${YELLOW}[*]${CLEAR} Packaging ${BLUE}$d${CLEAR}"
  tar --sort=name --owner=root:0 --group=root:0 --mtime='UTC 2024-01-01' -c --transform "s/$d\/dist/$d/" $d/dist | gzip -n | aws s3 cp - s3://irisctf-2024/$d.tar.gz --endpoint-url https://4a2c7fdf91730aebea0c116274da041f.r2.cloudflarestorage.com/ --region us-east-1
done
echo -e "${GREEN}[-]${CLEAR} Done!"
exit 0
