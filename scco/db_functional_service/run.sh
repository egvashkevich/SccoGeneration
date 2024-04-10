#!/bin/bash

# -e --- editable install (debug)
# -r --- reinstall
# -f --- path to .py file to run (relative to package directory)

################################################################################

# User data (EDIT MANUALLY FOR EACH PROJECT).

#set -x # debug
#set -eu

read -r -d '' ENV_FILES<<'EOF' || echo "ok" > /dev/null
    .env
    .env.secret.postgres
EOF

PACKAGE_NAME="db_functional_service"
REINSTALL="" # can be set by -r flag
EDITABLE_INSTALL="" # can be set by -e flag

################################################################################

# Script.

ENV_FILES=$(echo "${ENV_FILES}" | awk '{ print $1 }')
PIP_INSTALL_ARGS="."
MAIN_FILE=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    -e|--editable)
      PIP_INSTALL_ARGS="--editable ${PIP_INSTALL_ARGS}"
      shift 1 ;;
    -r|--reinstall)
      REINSTALL="1"
      shift 1 ;;
    -f|--file)
      MAIN_FILE="$2"
      shift 2;;
    *)
      echo "Unexpected argument: '$1'"
      exit 1
  esac
done

if [ -z "${MAIN_FILE}" ]; then
  echo "-f option is omitted, but required to specify file"
  exit 1
fi

if [ -n "${REINSTALL}" ]; then
  echo "Uninstalling package."
  pip3 uninstall -y "${PACKAGE_NAME}"
  echo "Installing package."
  pip3 install ${PIP_INSTALL_ARGS}
else
  PACKAGE_IS_INSTALLED="$(pip3 freeze | grep "${PACKAGE_NAME}")"
  echo -e "PACKAGE_IS_INSTALLED: ${PACKAGE_IS_INSTALLED}"
  if [ -n "${PACKAGE_IS_INSTALLED}" ]; then
    echo "Package is already installed, skip installation."
  else
    echo "Installing package."
    pip3 install ${PIP_INSTALL_ARGS}
  fi
fi

#for ENV_FILE in ${ENV_FILES}; do
#  ENV_VARS="$(grep -Ev '^\s*#|^\s*$' "${ENV_FILE}" | xargs -d '\n')"
#  for ENV_VAR in ${ENV_VARS}; do
#    export "${ENV_VAR?}"
#  done
#done

set -o allexport
for ENV_FILE in ${ENV_FILES}; do
  source "${ENV_FILE}" set
done
set +o allexport

################################################################################

# Run.

echo -e "Run package main.\n-----------------------------------------------"

python -u "src/${PACKAGE_NAME}/${MAIN_FILE}"
