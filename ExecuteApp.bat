REM ★パスはtestapp.pyが置かれているディレクトリに書き換えること
SCRIPT_HOME=C:\Hoge\Piyo\
cd %SCRIPT_HOME%\testapp
call .\venv\Scripts\activate.bat
python testapp.py
pause
