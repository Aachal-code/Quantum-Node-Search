# GitHub Actions CI/CD Setup Guide

Due to GitHub's directory naming conventions, the CI/CD workflow file needs to be placed in a specific location within your GitHub repository:

## File Location

```
.github/workflows/tests.yml
```

## Setup Instructions

1. In your GitHub repository, create the `.github/workflows/` directory structure
2. Copy the content from `workflows-tests.yml` to `.github/workflows/tests.yml`
3. Push to your repository

## Alternatively, Use This Command

```bash
mkdir -p .github/workflows
cp workflows-tests.yml .github/workflows/tests.yml
git add .github/
git commit -m "Add GitHub Actions CI/CD pipeline"
git push
```

## What the CI/CD Pipeline Does

### 1. **Tests Job**
- Runs on Python 3.9, 3.10, 3.11, 3.12
- Executes all unit tests
- Generates coverage reports
- Uploads to Codecov

### 2. **Lint Job**
- Checks code quality with Flake8
- Ensures consistent formatting

### 3. **Benchmark Job**
- Runs quick benchmarks (N = 8, 16, 32, 64)
- Uploads results as artifacts
- Can comment on PRs with results

### 4. **Notify Job**
- Reports overall pipeline status
- Fails if any job fails

## Triggers

The pipeline runs on:
- Every push to `main` or `develop` branches
- Every pull request to `main`
- Weekly schedule (Sunday at 00:00 UTC)

## Required GitHub Secrets

For Docker builds (optional), set in Settings → Secrets:
- `DOCKER_USERNAME`: Your Docker Hub username
- `DOCKER_PASSWORD`: Your Docker Hub access token

## View Results

After pushing:
1. Go to Actions tab in your GitHub repository
2. Select the workflow run
3. Check individual job logs

## Customize

Edit `workflows-tests.yml` (or `.github/workflows/tests.yml` after moving) to:
- Add more test environments
- Change triggers
- Add notifications
- Integrate with external services

## Example: Running Benchmarks on Every PR

```yaml
- name: Comment PR with benchmark results
  if: github.event_name == 'pull_request'
  uses: actions/github-script@v6
  with:
    script: |
      const fs = require('fs');
      const results = fs.readFileSync('data/results.csv', 'utf8');
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: '## Benchmark Results\n\n```\n' + results + '\n```'
      });
```

## Troubleshooting

### Tests Fail on Certain Python Versions
- Check for version-specific compatibility in `requirements.txt`
- Update dependency versions as needed

### Codecov Integration Not Working
- Ensure `CODECOV_TOKEN` is set (optional for public repos)
- Check Codecov integration status

### Docker Build Fails
- Verify Docker secrets are set correctly
- Check Dockerfile for syntax errors
- Ensure sufficient GitHub Actions minutes

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Pytest with GitHub Actions](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python)
- [Docker with GitHub Actions](https://docs.github.com/en/actions/publishing-packages/publishing-docker-images)
