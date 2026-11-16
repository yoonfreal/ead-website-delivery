# EAD delivery demo

Class 3: Git, GitHub and artifact delivery. Class 4: Docker image delivery.

## Local use
Requires Python 3.11 or newer and Git. No pip install is needed.

Run from the repository root (use python3 on Mac/Linux or py on Windows):

```text
python3 -m unittest discover -s tests -v
python3 tools/check_site.py src
python3 tools/build.py
python3 -m http.server 8000 --directory dist/site --bind 127.0.0.1
```

Open http://localhost:8000 and stop with Ctrl+C.
The local preview is not a production service.

## Workflow contract
- Push ci-demo: tests, validation, build, then artifact upload.
- Push main or feature/*: no push-triggered workflow run.
- Pull request targeting main or ci-demo: tests and build, no artifact upload.
- A failed step blocks later build/upload steps.
- Artifacts contain site.zip and build-info.json, retained for 7 days subject to repository policy.
- This is CI plus artifact delivery, not a deployed running application.
