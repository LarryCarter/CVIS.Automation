# HyperExecute Reporting

## Source of truth

HyperExecute should parse NUnit XML:

```yaml
report: true
partialReports:
  type: nunit
  location: .\TestResults\NUnitXml
  frameworkName: nunit
```

## Authoritative HTML

The CVIS HTML report is generated after tests run:

```text
TestResults\CPN\cpn-report.html
```

It is built from:

```text
TestResults\TRX
TestResults\NUnitXml
```

## Lifecycle report

The lifecycle report is diagnostic only:

```text
TestResults\CPN\cpn-lifecycle-report.html
```

Do not use lifecycle report totals to decide whether HyperExecute passed.
