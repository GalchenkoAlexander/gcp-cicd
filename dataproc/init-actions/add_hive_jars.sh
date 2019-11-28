#!/bin/bash


function copyAndConfigureHiveAuxLibs() {

  readonly HIVE_AUX_LIBS_GCS_PATH=$(/usr/share/google/get_metadata_value attributes/hive-aux-libs)

  # TODO: set via dataproc properties
    bdconfig set_property \
    --configuration_file "/etc/hive/conf/hive-site.xml" \
    --name 'hive.reloadable.aux.jars.path' --value 'file:///usr/lib/hive/auxlib/*' \
    --clobber

  # Ensure that instance metadata was passed with path to Hive aux libs
  if [ -z "$HIVE_AUX_LIBS_GCS_PATH" ]
  then
      echo "$HIVE_AUX_LIBS_GCS_PATH is empty"
      exit 1
  fi

  # If the Hive aux lib directory does not exist, create it.
  if [ ! -d "${HIVE_AUX_LIBS_GCS_PATH}" ]
  then
    echo "Creating directory ${HIVE_AUX_LIBS_GCS_PATH}."
    mkdir -p "{$HIVE_AUX_LIBS_GCS_PATH}" 
  fi

  # gsutil parallel copy of Hive aux libs to local filesystem
  gsutil -m cp -r "${HIVE_AUX_LIBS_GCS_PATH}" /usr/lib/hive/auxlib/
}

function configureAndBounceHiveServer2() {
  
  # Update hive to add auxlib dir
  bdconfig set_property \
    --configuration_file "/etc/default/hive-server2" \
    --name 'AUX_CLASSPATH' --value 'file:///usr/lib/hive/auxlib/*' \
    --clobber

  # Restart & check hive-server2 status
  if ( systemctl is-enabled --quiet hive-server2 ); then
    # Restart hive server2 if it is enabled
    systemctl restart hive-server2
    systemctl status hive-server2  # Ensure it started successfully
  else
    echo "Service hive-server2 is not enabled"
  fi

}

function main() {

  # Copy Hive aux libs to all nodes on the cluster
  copyAndConfigureHiveAuxLibs

  # Only configure HiveServer2 on Dataproc master
  readonly ROLE=$(/usr/share/google/get_metadata_value attributes/dataproc-role)
  if [[ "${ROLE}" == 'Master' ]]; then
    configureAndBounceHiveServer2
  fi
  
}

main
