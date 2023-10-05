echo "Build Start"
python3.11 -m pip install -r req.txt
python3.11 manage.py collectstatic --noinput --clear
echo "Build End"