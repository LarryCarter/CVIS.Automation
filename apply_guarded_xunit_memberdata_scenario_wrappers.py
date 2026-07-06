from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path.cwd()
EXPECTED_SOLUTION = ROOT / "CVIS.Automation.sln"
EXPECTED_PROJECT = ROOT / "Automation.ConsoleApp.Tests" / "Automation.ConsoleApp.Tests.csproj"

SKIP = {".git", ".vs", ".contollo", "bin", "obj", "__pycache__", "TestResults"}

METHOD_RE = re.compile(
    r"(?P<attrs>(?:^[ \t]*\[[^\r\n]*\][ \t]*(?:\r?\n))+)"
    r"(?P<sig>^[ \t]*(?:public|private|protected|internal)\s+(?:static\s+)?(?:async\s+)?"
    r"(?P<ret>void|Task|Task<[^>]+>|ValueTask|ValueTask<[^>]+>)\s+"
    r"(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*\((?P<params>[^)]*)\)\s*(?:\r?\n)?[ \t]*\{)",
    re.MULTILINE,
)
THEORY_RE = re.compile(r'^[ \t]*\[Theory(?:\([^\)]*\))?\][ \t]*(?:\r?\n)?', re.MULTILINE)
TRAIT_RE = re.compile(r'^[ \t]*\[Trait\(\s*"([^"]+)"\s*,\s*"([^"]+)"\s*\)\][ \t]*(?:\r?\n)?', re.MULTILINE)
MEMBER_RE = re.compile(r'^[ \t]*\[MemberData\(\s*nameof\((?P<name>[A-Za-z_][A-Za-z0-9_]*)\)[^\)]*\)\][ \t]*(?:\r?\n)?', re.MULTILINE)

@dataclass
class Method:
    start:int
    end:int
    attrs:str
    name:str
    ret:str

@dataclass
class Result:
    file:Path
    source:str
    provider:str
    wrappers:list[str]

def assert_correct_repository() -> None:
    if not EXPECTED_SOLUTION.exists():
        raise SystemExit(
            "Wrong target root. This RDEL must be run from the CVIS.Automation solution root. "
            f"Expected file not found: {EXPECTED_SOLUTION}"
        )

    if not EXPECTED_PROJECT.exists():
        raise SystemExit(
            "Wrong target root or missing project. This RDEL requires Automation.ConsoleApp.Tests. "
            f"Expected file not found: {EXPECTED_PROJECT}"
        )

def skip(path: Path) -> bool:
    return any(part in SKIP for part in path.parts)

def brace_end(text, open_i):
    depth = 0
    s = c = v = sl = ml = False
    i = open_i
    while i < len(text):
        ch = text[i]
        nx = text[i+1] if i+1 < len(text) else ""
        if sl:
            if ch == "\n":
                sl = False
            i += 1
            continue
        if ml:
            if ch == "*" and nx == "/":
                ml = False
                i += 2
                continue
            i += 1
            continue
        if s:
            if v and ch == '"' and nx == '"':
                i += 2
                continue
            if not v and ch == "\\":
                i += 2
                continue
            if ch == '"':
                s = False
                v = False
            i += 1
            continue
        if c:
            if ch == "\\":
                i += 2
                continue
            if ch == "'":
                c = False
            i += 1
            continue
        if ch == "/" and nx == "/":
            sl = True
            i += 2
            continue
        if ch == "/" and nx == "*":
            ml = True
            i += 2
            continue
        if ch == "@" and nx == '"':
            s = True
            v = True
            i += 2
            continue
        if ch == '"':
            s = True
            i += 1
            continue
        if ch == "'":
            c = True
            i += 1
            continue
        if ch == "{":
            depth += 1
        if ch == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    raise ValueError("brace")

def top_args(text):
    out=[]; cur=[]; par=bra=brk=0; s=c=v=False; i=0
    while i < len(text):
        ch=text[i]; nx=text[i+1] if i+1 < len(text) else ""
        if s:
            cur.append(ch)
            if v and ch == '"' and nx == '"':
                cur.append(nx); i+=2; continue
            if not v and ch == "\\":
                if nx: cur.append(nx)
                i+=2; continue
            if ch == '"':
                s=False; v=False
            i+=1; continue
        if c:
            cur.append(ch)
            if ch == "\\" and nx:
                cur.append(nx); i+=2; continue
            if ch == "'":
                c=False
            i+=1; continue
        if ch == "@" and nx == '"':
            cur += [ch,nx]; s=True; v=True; i+=2; continue
        if ch == '"':
            cur.append(ch); s=True; i+=1; continue
        if ch == "'":
            cur.append(ch); c=True; i+=1; continue
        if ch=="(": par+=1
        elif ch==")": par-=1
        elif ch=="{": bra+=1
        elif ch=="}": bra-=1
        elif ch=="[": brk+=1
        elif ch=="]": brk-=1
        if ch=="," and par==0 and bra==0 and brk==0:
            out.append("".join(cur).strip()); cur=[]; i+=1; continue
        cur.append(ch); i+=1
    tail="".join(cur).strip()
    if tail:
        out.append(tail)
    return out

def token(value):
    value=value.strip().strip('"')
    parts=re.split(r"[^A-Za-z0-9]+", value)
    return "".join(p[:1].upper()+p[1:] for p in parts if p) or "Scenario"

def row_token(args, idx):
    for arg in top_args(args):
        a=arg.strip()
        if len(a)>2 and a.startswith('"') and a.endswith('"'):
            return token(a)
    return f"Row{idx:03d}"

def find_provider(text, name):
    pat = re.compile(rf"\b{name}\b\s*(?:=>\s*(?P<expr>.*?);|\{{(?P<body>.*?)\n[ \t]*\}})", re.DOTALL)
    for m in pat.finditer(text):
        prefix=text[max(0,m.start()-300):m.start()]
        if re.search(r"(IEnumerable|TheoryData|object\[\]|public|private|internal|protected|static)", prefix):
            return m.group("expr") or m.group("body")
    return None

def rows_from(body):
    rows=[]; seen=set()
    patterns=[
        re.compile(r"yield\s+return\s+new\s+object\[\]\s*\{(?P<a>.*?)\}\s*;", re.DOTALL),
        re.compile(r"new\s+object\[\]\s*\{(?P<a>.*?)\}", re.DOTALL),
        re.compile(r"\.Add\((?P<a>.*?)\)\s*;", re.DOTALL),
    ]
    for pat in patterns:
        for m in pat.finditer(body):
            a=m.group("a").strip()
            if not a or a in seen:
                continue
            seen.add(a)
            rows.append((a,row_token(a,len(rows)+1)))
    return rows

def method_infos(text):
    out=[]
    for m in METHOD_RE.finditer(text):
        op=text.find("{", m.start("sig"))
        if op < 0:
            continue
        try:
            end=brace_end(text, op)
        except Exception:
            continue
        out.append(Method(m.start(), end+1, m.group("attrs"), m.group("name"), m.group("ret")))
    return out

def traits(attrs):
    return "".join(f'[Trait("{k}", "{v}")]\n' for k,v in TRAIT_RE.findall(attrs))

def indent_attrs(s):
    return "".join("    "+line+"\n" for line in s.splitlines()) if s else ""

def call_line(ret, name, args):
    call=f"{name}({args})"
    if ret == "Task" or ret.startswith("Task<") or ret == "ValueTask" or ret.startswith("ValueTask<"):
        return f"        return {call};"
    return f"        {call};"

def unique(base, used):
    if base not in used:
        used.add(base)
        return base
    i=2
    while f"{base}_{i}" in used:
        i+=1
    name=f"{base}_{i}"
    used.add(name)
    return name

def process(path):
    text=path.read_text(encoding="utf-8-sig")
    used=set(re.findall(r"\b(?:public|private|protected|internal)\s+(?:static\s+)?(?:async\s+)?(?:void|Task|Task<[^>]+>|ValueTask|ValueTask<[^>]+>)\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", text))
    inserts=[]; results=[]
    for meth in method_infos(text):
        if not THEORY_RE.search(meth.attrs):
            continue
        providers=[m.group("name") for m in MEMBER_RE.finditer(meth.attrs)]
        if not providers:
            continue
        wrappers=[]; names=[]
        for prov in providers:
            body=find_provider(text, prov)
            if not body:
                continue
            for args, rtok in rows_from(body):
                wname=unique(f"{meth.name}_{token(prov)}_{rtok}", used)
                wrapper = (
                    "\n    [Fact]\n"
                    + indent_attrs(traits(meth.attrs))
                    + f"    public {meth.ret} {wname}()\n"
                    + "    {\n"
                    + call_line(meth.ret, meth.name, args) + "\n"
                    + "    }"
                )
                wrappers.append(wrapper.rstrip())
                names.append(wname)
        if wrappers:
            inserts.append((meth.end, "\n\n" + "\n\n".join(wrappers)))
            results.append(Result(path,meth.name,", ".join(providers),names))
    if not inserts:
        return []
    updated=text
    for pos, ins in sorted(inserts, reverse=True):
        updated=updated[:pos]+ins+updated[pos:]
    path.write_text(updated, encoding="utf-8")
    return results

def append(path, title, body):
    path.parent.mkdir(parents=True, exist_ok=True)
    old=path.read_text(encoding="utf-8") if path.exists() else ""
    if title in old:
        return
    path.write_text((old.rstrip()+"\n\n" if old.strip() else "") + title + "\n\n" + body.strip() + "\n", encoding="utf-8")

def docs():
    append(ROOT/"docs/DECISIONS.md", "## 2026-07-06 — Guarded xUnit MemberData Scenario Wrappers",
           "Decision: RDEL package 012 must fail fast unless it is run from the CVIS.Automation solution root.\n\nIt generates explicit `[Fact]` wrapper methods for parseable xUnit `[MemberData]` rows when an external counting tool cannot see individual scenarios.")
    append(ROOT/"docs/AI_INSTRUCTIONS.md", "## xUnit MemberData Counting Rule",
           "If a `[MemberData]` theory must be visible to the external counter per scenario, generate explicit wrapper facts or use simple `[InlineData]`. Packages must validate the target repository before transforming files.")
    append(ROOT/"docs/memory.md", "## xUnit MemberData scenario wrappers",
           "RDEL sequence 012 replaces the failed wrong-root sequence 011 application with a guarded package that requires CVIS.Automation.sln.")
    append(ROOT/"docs/context.md", "## xUnit MemberData scenario count compatibility",
           "The external counter may not count individual MemberData rows. Generated `[Fact]` wrappers expose parseable rows as physical tests. Sequence 012 is guarded against wrong-repo application.")

def report(results):
    p=ROOT/"docs/xunit-memberdata-scenario-wrapper-report.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    lines=["# xUnit MemberData Scenario Wrapper Report","","Generated by RDEL package 012.",""]
    if not results:
        lines.append("No parseable xUnit MemberData scenarios were found.")
    else:
        for r in results:
            lines += [f"## `{r.file.relative_to(ROOT)}`","",f"- Source theory: `{r.source}`",f"- Provider(s): `{r.provider}`","- Wrapper methods:"]
            lines += [f"  - `{n}`" for n in r.wrappers]
            lines.append("")
    p.write_text("\n".join(lines).rstrip()+"\n", encoding="utf-8")

def build_project() -> int:
    result = subprocess.run(
        ["dotnet", "build", str(EXPECTED_PROJECT)],
        cwd=ROOT,
        text=True,
    )
    return result.returncode

def main():
    assert_correct_repository()

    results=[]
    test_root = ROOT / "Automation.ConsoleApp.Tests"
    for path in test_root.rglob("*.cs"):
        if not skip(path):
            results.extend(process(path))

    report(results)
    docs()

    print(f"xUnit MemberData wrapper generation complete. Source methods changed: {len(results)}")
    print("Report: docs/xunit-memberdata-scenario-wrapper-report.md")

    exit_code = build_project()
    if exit_code != 0:
        raise SystemExit(exit_code)

if __name__ == "__main__":
    main()
