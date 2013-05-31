xcopy art ..\pgs4a-0.9.4\1gam_01\art /E /Y
xcopy core ..\pgs4a-0.9.4\1gam_01\core /E /Y
xcopy dat ..\pgs4a-0.9.4\1gam_01\dat /E /Y
xcopy fonts ..\pgs4a-0.9.4\1gam_01\fonts /E /Y
xcopy music ..\pgs4a-0.9.4\1gam_01\music /E /Y
xcopy sounds ..\pgs4a-0.9.4\1gam_01\sounds /E /Y
copy main.py ..\pgs4a-0.9.4\1gam_01\main.py /Y
copy doc.txt ..\pgs4a-0.9.4\1gam_01\doc.txt /Y
cd ..\pgs4a-0.9.4\
c:\python27\python android.py build 1gam_01 release install
c:\python27\python android.py logcat