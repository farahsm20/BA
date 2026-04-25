# Errors: 
### Port 5432 Conflict

- `role "postbound" does not exist`

- Cause: Mac's local PostgreSQL (installed via Homebrew) was running on port 5432 and intercepting the connection before it reached the 
Docker container ( i installed it twice :)  )

- Permanent fix:


    `bashbrew services stop postgresql@16`


     `brew uninstall postgresql@16`
