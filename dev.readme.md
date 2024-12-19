# Dev readme

## How build

```pwsh
  uv build
```

## How Deploy

```bash
 twine upload dist/* -u $CI_DEPLOY_USER -p $CI_DEPLOY_PASSWORD --repository-url https://gitlab.com/api/v4/projects/52290531/packages/pypi
```

How Test

```bash
  uv pytest --junit-xml=reports.xml .
```
