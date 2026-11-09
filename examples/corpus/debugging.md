# Service Debugging
## Symptom
After deployment, the API returned HTTP 500 responses because the application could not initialize its database connection.
## Root cause
The deployment had a missing environment variable named DATABASE_URL. Without this required configuration, the service could not construct the database connection string.
## Resolution
Add DATABASE_URL to the deployment environment, restart the service, and verify the health endpoint and database connectivity.
## Prevention
Validate required environment variables during startup and fail with a clear configuration error before accepting traffic.
