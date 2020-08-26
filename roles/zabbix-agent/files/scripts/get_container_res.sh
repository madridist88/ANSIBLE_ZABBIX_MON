#!/bin/bash
CONT_NAME=$1
CONT_RES=$2
docker stats $CONT_NAME --format "$CONT_RES" --no-stream | sed s/%//

