MailShooter
-----------

### Requirement
python3

### Prerequisites
```bash
# maybe you need a virtualenv?
virtualenv .venv
source .venv/bin/activate

# install this
pip install ${PATH_TO_MAILSHOOTER}

# copy and modify some files
cp -t ./ ${PATH_TO_MAILSHOOTER}/examples/*
# modify it.

# run
mailshooter template.yaml data.csv
```