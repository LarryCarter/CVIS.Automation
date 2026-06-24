from pathlib import Path
import shutil

ROOT = Path.cwd()
PACKAGE_ROOT = Path(__file__).resolve().parent
PAYLOAD = PACKAGE_ROOT / "payload"

def copy_file(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)

def main():
    options = ROOT / "CVIS.Playwright.NUnitCompat" / "Reporting" / "CPNReportOptions.cs"
    if options.exists():
        text = options.read_text(encoding="utf-8")
        text = text.replace('public string JsonFileName { get; init; } = "cpn-report.json";',
                            'public string JsonFileName { get; init; } = "cpn-lifecycle-report.json";')
        text = text.replace('public string HtmlFileName { get; init; } = "cpn-report.html";',
                            'public string HtmlFileName { get; init; } = "cpn-lifecycle-report.html";')
        options.write_text(text, encoding="utf-8")
        print("Renamed lifecycle report outputs to cpn-lifecycle-report.*")

    for src in PAYLOAD.rglob("*"):
        if src.is_file():
            rel = src.relative_to(PAYLOAD)
            copy_file(src, ROOT / rel)
            print(f"Copied {rel}")

    print("Hard authoritative reporting fix added.")
    print("Run .\\scripts\\run-authoritative-test-report-local.ps1")
    print("Open TestResults\\CPN\\cpn-report.html")

if __name__ == "__main__":
    main()
