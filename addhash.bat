@echo off
echo Before:
type filedb
echo .
echo|set /p=%*,>> filedb
echo Added.
echo Now:
type filedb