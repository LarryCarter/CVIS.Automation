# Add HyperExecute CPN Reporting

This is a Contollo RDEL plugin-compatible package.

## Adds

```text
hyperexecute-cpn-reporting.yaml
hyperexecute-cvis-automation-reporting.yaml
README_HYPEREXECUTE_CPN_REPORTING.md
```

## Report output format

```text
TestResults\NUnitXml\*.xml
TestResults\NUnit\*.trx
TestResults\CPN\cpn-report.html
TestResults\CPN\cpn-report.json
TestResults\CPN\Tests\*.json
```

## HyperExecute parsing

```yaml
report: true
partialReports:
  type: nunit
  location: .\TestResults\NUnitXml
  frameworkName: nunit
```

## CPN artifacts

```yaml
uploadArtefacts:
  - name: cpn-test-output
    path:
      - .\TestResults\NUnitXml
      - .\TestResults\NUnit
      - .\TestResults\CPN
```
