#!/bin/bash

##
# This script takes care of bundling the apworld.
#
# Arguments:
# * $1: Can be "clean" to clean the build environment.
#
# Environment:
# * TAG:
#     A string used to tag the bundle name
#     eg: "v1.1.1" will name the bundle "metroidprime_apworld-v1.1.1"
#     (defaut: current date and time)
##

set -eo pipefail
shopt -s globstar

CWD="$(dirname $(realpath $0))"
REQS=("zip" "rsync" "pip")
OLD_LINUX_FOR_DME="manylinux2014_x86_64"
SUPPORTED_PLATFORMS=("win_amd64" "manylinux_2_28_x86_64")

##
# Make sure all the required utilities are installed.
##
function pre_flight() {
    local bad="0"
    for r in ${reqs[@]}; do
        if ! command -v $r > /dev/null; then
            echo "!=> Unable to locate the '${r}' utility in \$PATH. Make sure it is installed."
            bad="1"
        fi
    done

    [ "${bad}" = "1" ] && exit 1 ||:
}

##
# Generate the `lib` folder within the target directory.
# Uses the `requirements.txt` file of the project to get every dependencies and copy them over.
# Uses `requirements.ignore` to specify which files not to copy over from within each of the requirements.
##
function get_deps() {
    local platform="$1" requirements_file="$2" to="$3"
    echo "=> Bundle requirements for ${platform}"

    # DME doesn't publish to the same version as randomprime, this installs the most recent supported linux platform and uses a
    #  requirements.txt that excludes it
    if [ "${platform}" = "manylinux_2_28_x86_64" ]; then
        echo "  -> Installing dolphin-memory-engine override for ${platform}"
        pip install dolphin-memory-engine==1.2.0 \
            --target ${to}/${platform} \
            --platform ${OLD_LINUX_FOR_DME} \
            --only-binary=:all: \
            --no-user
    fi

    # Fetch the libraries binary files for the specified platform.
    echo "  -> Fetch requirements"
    pip install \
        --target ${to}/${platform} \
        --platform ${platform} \
        --only-binary=:all: \
        --requirement ${requirements_file} \
        --no-user

    # If platform is manylinux_2_28_x86_64 then also install dolphin memory engine 1.2.0

    # This is for the `.dist-info` folder, which contains the metadata of the mod.
    # We just copy over the license file into the main library folder
    echo "  -> Processing metadata"
    for folder in ${to}/${platform}/*.dist-info; do
        local dir="$(basename ${folder} | cut -d '-' -f 1)"
        cp --verbose "${folder}/LICENSE" "${folder}/../${dir}/" ||:
        rm --force --recursive ${folder}
    done

    # Go though each of the downloaded libraries and copy the relevant parts.
    echo "  -> Transfer requirements to bundle"
    for folder in ${to}/${platform}/*; do
        echo "    - Processing: ${folder}"

        # The actual code of the library.
        local dir="$(basename ${folder})"
        mkdir -p ${to}/${dir}
        rsync \
            --progress \
            --recursive \
            --prune-empty-dirs \
            --exclude-from="${CWD}/requirements.ignore" \
            "${folder}/" "${to}/${dir}"
    done

    echo "  -> Cleaning"
    rm --force --recursive ${to}/${platform}
}

##
# Create the `apworld` file used by Archipelago.
#
# Arguments:
# * $1: project root
# * $2: destination directory
##
function mk_apworld() {
    local root="$1" destdir="$2"
    echo "=> Bundling apworld"
    echo "From: ${root}"
    echo "To: ${destdir}"
    mkdir --parents "${destdir}/metroidprime"
    rsync --progress \
        --recursive \
        --prune-empty-dirs \
        --exclude-from="${CWD}/apworld.ignore" \
        "${root}/" "${destdir}/metroidprime"

    echo "${tag}" > "${destdir}/metroidprime/version.txt"

    # If this already exists then ovewrite it
    rm -rf "${destdir}/metroidprime/lib"
    mv "${destdir}/lib" "${destdir}/metroidprime/lib"
    pushd "${destdir}"
    zip -9r "metroidprime.apworld" "metroidprime"
    popd

    rm --force --recursive "${destdir}/metroidprime"
}

##
# Copy static data into the destination directory.
##
function cp_data() {
    local root="$1" destdir="$2"
    echo "=> Copying over the extra data"
    cp --verbose ${root}/LICENSE.md ${destdir}
    cp --verbose ${root}/README.md ${destdir}
    cp --verbose "${root}/Metroid Prime.yaml" ${destdir}
}

##
# Create the final bundled archive.
#
# Arguments:
# * $1: The location from where the archive is created.
# * $2: The path of the output archive.
##
function bundle() {
    local from="$1" out="$2"
    echo "=> Finalize bundle"
    [ -f "${out}" ] && rm ${out} ||:
    pushd "${from}"
    zip -9r "${out}" "."
    popd
}

##
# Main entry point.
##
function main() {
    pre_flight

    local target_path="${CWD}/target"
    local bundle_base="metroidprime_apworld"
    mkdir --parents ${target_path}

    case "$1" in
    # Clean the build environment.
    clean)
        find "${target_path}" \
            -depth \
            -type d \
            -name "${bundle_base}-*" \
            -exec rm --force --recursive --verbose {} \;
        ;;

    # Create the release bundle.
    *)
        local tag="${TAG:-$(date '+%Y-%m-%d_%H%M')}"
        local project="$(realpath ${CWD}/..)"
        local bundle="${bundle_base}-${tag}"
        local destdir="${target_path}/${bundle}"
        local local_install=false

        # Loop through all the arguments
        for arg in "$@"; do
          if [ "$arg" == "--local" ]; then
            local_install=true
            break
          fi
        done

      if [ "$local_install" == true ]; then
        # Copy project/lib to destdir
        mkdir -p "${destdir}"
        cp -r "${project}/lib" "${destdir}"
        echo "=> Local install, copying ${project}/lib to ${destdir}"
      else
          for platform in "${SUPPORTED_PLATFORMS[@]}"; do
              local requirements_file="${project}/requirements.txt"
              if [ "${platform}" = "manylinux_2_28_x86_64" ]; then
                  requirements_file="${project}/requirements-linux.txt"
              fi
              get_deps "${platform}" ${requirements_file} "${destdir}/lib"
              # copy deps to project folder as well for local dev
              cp -r "${destdir}/lib" "${project}"
          done
      fi

        mk_apworld "${project}" "${destdir}"
        cp_data "${project}" "${destdir}"
        bundle "${destdir}" "${target_path}/${bundle}.zip"
        echo "! Bundle finalized as ${target_path}/${bundle}.zip"
        ;;
    esac
}
main "$@"
