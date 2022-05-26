#!/bin/sh
#SBATCH --partition=CPUQ
#SBATCH --account=ie-idi
#SBATCH --time=00:60:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=12000
#SBATCH --job-name="dt8123"
#SBATCH --output=dt8123_dtwearable_result.out
#SBATCH --mail-user=hamza.mohammed@ntnu.no
#SBATCH --mail-type=ALL



WORKDIR=${SLURM_SUBMIT_DIR}
cd ${WORKDIR}
echo "we are running from this directory: $SLURM_SUBMIT_DIR"
echo " the name of the job is: $SLURM_JOB_NAME"
echo "Th job ID is $SLURM_JOB_ID"
echo "The job was run on these nodes: $SLURM_JOB_NODELIST"
echo "Number of nodes: $SLURM_JOB_NUM_NODES"
echo "We are using $SLURM_CPUS_ON_NODE cores"
echo "We are using $SLURM_CPUS_ON_NODE cores per node"
echo "Total of $SLURM_NTASKS cores"

module purge
module load Anaconda/2020.07


# Step 1: Setup environment.
echo
echo Setting up virtual environment...
echo

set -e

pip3 install virtualenv # Assumes pip3 is installed!
python3 -m virtualenv $OUTPUT_FOLDER/venv
source $OUTPUT_FOLDER/venv/bin/activate
pip3 install -r requirements.txt



python3 app.py #/path/to/file.py

uname -a


