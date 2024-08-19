param (
    [string]
    $Package
)

pip install $Package
pip freeze > requirements.txt