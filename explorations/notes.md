# every session
`docker ps`                                          # confirm container is running

`cd ~/BachelorArbeit && source venv/bin/activate`    # activate venv

# copy paste new implementation 
`mkdir -p ~/BachelorArbeit/explorations/<topic>`

`touch ~/BachelorArbeit/explorations/<topic>/<name>.py`

`code ~/BachelorArbeit/explorations/<topic>/<name>.py`# (doesn't work sometimes so just open it in vs code )

`git add <folder>/ && git commit -m "msg" && git push origin main`

# setup errors and fixes

### venv verification

`python3 -c "import postbound; print('ok')"`  # tests that postbound is importable in your current venv (to verify the venv is working correctly)

### Port 5432 Conflict

- `role "postbound" does not exist`

- Cause: Mac's local PostgreSQL (installed via Homebrew) was running on port 5432 and intercepting the connection before it reached the 
Docker container ( i installed it twice :)  )

- Permanent fix:


    `bashbrew services stop postgresql@16`


     `brew uninstall postgresql@16`

### TU Dresden Download Failed
The PostBOUND setup script tries to download the JOB dataset from TU Dresden's server, but i assume the link requires university credentials so it returned an HTML login page instead of actual data causing the load to fail 

Fixed by downloading the dataset directly from the public CWI source, copying it into the Docker container, and loading each table manually (idk why it took too long so i downloaded each table individually)
