# every session
`docker ps`                                          # confirm container is running

`cd ~/BachelorArbeit && source venv/bin/activate`    # activate venv

# copy paste new implementation 
`mkdir -p ~/BachelorArbeit/explorations/<topic>`

`touch ~/BachelorArbeit/explorations/<topic>/<name>.py`

`code ~/BachelorArbeit/explorations/<topic>/<name>.py`# (doesn't work sometimes so just open it in vs code )

`git add <folder>/ && git commit -m "msg" && git push origin main`

# something seems broken
`python3 -c "import postbound; print('ok')"`  # tests that postbound is importable in your current venv (to verify the venv is working correctly)


