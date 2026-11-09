# Deployment Operations
## Pre-deployment verification
Run automated tests, validate the release configuration, and confirm that the database migration is backward compatible.
## Health verification
After deployment, check the service health endpoint, error rate, request latency, and database connectivity before increasing traffic.
## Deployment rollback procedure
If health checks fail or the error rate exceeds the release threshold, stop the rollout and restore the previous stable application version.
Verify that the restored version is healthy before reopening traffic. Record the failed release version and the reason for rollback.
## Follow-up
Preserve logs, compare configuration changes, identify the root cause, and add a regression test before attempting another deployment.
