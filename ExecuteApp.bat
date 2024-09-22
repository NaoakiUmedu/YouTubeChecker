REM パスはtestapp.pyが置かれているディレクトリに書き換える
SCRIPT_HOME=C:\Hoge\Piyo
cd %SCRIPT_HOME%
call .\venv\Scripts\activate.bat
python testapp.py
pause
