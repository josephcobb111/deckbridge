conda create -n conda_build python=3.9 boa conda-build -y
conda activate conda_build
rm -R -f conda-pkg
mkdir conda-pkg
conda build conda_recipe/ --output-folder conda-pkg
conda install -c file://${HOME}/deckbridge/conda-pkg/ deckbridge -y
conda install pytest pytest-cov flake8 -y
pytest

# To upload to cloud
# anaconda login
# anaconda upload <PATH-TO-PACKAGE>.tar.bz2
# e.g.,
# anaconda login
# anaconda upload conda-pkg/noarch/deckbridge-0.1.0-py_0.tar.bz2 
