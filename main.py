name: Disable CI

on: [push, pull_request]

jobs:
  disabled:
    runs-on: ubuntu-latest
    steps:
      - name: ⚠️ CI is disabled
        run: echo "GitHub Actions has been disabled for this project."
