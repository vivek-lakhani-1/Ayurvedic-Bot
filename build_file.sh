echo "Build Start"
python3 -m pip install -r req.txt
python3 manage.py collectstatic --noinput --clear
echo "Build End"
