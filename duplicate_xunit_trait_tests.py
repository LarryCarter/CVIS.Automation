from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import re
from typing import Iterable
ROOT = Path.cwd()
EXCLUDED_DIRS = {'.git', '.vs', '.contollo', 'bin', 'obj', '__pycache__', 'TestResults'}
METHOD_PATTERN = re.compile(r'(?P<attrs>(?:^[ \t]*\[[^\r\n]*\][ \t]*(?:\r?\n))+)'
                            r'(?P<sig>^[ \t]*(?:public|private|protected|internal)\s+'
                            r'(?:static\s+)?(?:async\s+)?'
                            r'(?:void|Task|Task<[^>]+>|ValueTask|ValueTask<[^>]+>)\s+'
                            r'(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*\([^)]*\)\s*(?:\r?\n)?[ \t]*\{)', re.MULTILINE)
TRAIT_PATTERN = re.compile(r'^[ \t]*\[Trait\(\s*"(?P<key>[^"]+)"\s*,\s*"(?P<value>[^"]+)"\s*\)\][ \t]*(?:\r?\n)?', re.MULTILINE)
FACT_PATTERN = re.compile(r'^[ \t]*\[Fact(?:\([^\)]*\))?\][ \t]*(?:\r?\n)?', re.MULTILINE)
@dataclass(frozen=True)
class Trait:
    key: str
    value: str
@dataclass(frozen=True)
class Change:
    path: Path
    method_name: str
    trait_keys: list[str]
    generated_methods: list[str]
def should_skip(path: Path) -> bool:
    return any(part in EXCLUDED_DIRS for part in path.parts)
def iter_csharp_files() -> Iterable[Path]:
    for path in ROOT.rglob('*.cs'):
        if not should_skip(path): yield path
def find_matching_brace(text: str, open_brace_index: int) -> int:
    depth=0; in_string=in_char=in_verbatim_string=False; in_sl=in_ml=False; i=open_brace_index
    while i < len(text):
        c=text[i]; n=text[i+1] if i+1 < len(text) else ''
        if in_sl:
            if c=='\n': in_sl=False
            i+=1; continue
        if in_ml:
            if c=='*' and n=='/': in_ml=False; i+=2; continue
            i+=1; continue
        if in_string:
            if in_verbatim_string:
                if c=='"' and n=='"': i+=2; continue
                if c=='"': in_string=in_verbatim_string=False
                i+=1; continue
            if c=='\\': i+=2; continue
            if c=='"': in_string=False
            i+=1; continue
        if in_char:
            if c=='\\': i+=2; continue
            if c=="'": in_char=False
            i+=1; continue
        if c=='/' and n=='/': in_sl=True; i+=2; continue
        if c=='/' and n=='*': in_ml=True; i+=2; continue
        if c=='@' and n=='"': in_string=in_verbatim_string=True; i+=2; continue
        if c=='"': in_string=True; i+=1; continue
        if c=="'": in_char=True; i+=1; continue
        if c=='{': depth+=1
        if c=='}':
            depth-=1
            if depth==0: return i
        i+=1
    raise ValueError('Could not find matching brace')
def sanitize_trait_key(key: str) -> str:
    parts=re.split(r'[^A-Za-z0-9]+', key)
    return ''.join(p[:1].upper()+p[1:] for p in parts if p) or 'Trait'
def trait_method_name(original_name: str, trait_key: str) -> str:
    suffix=sanitize_trait_key(trait_key)
    if f'_{suffix}_' in original_name or original_name.endswith(f'_{suffix}'): return original_name
    for token in ('_Should','_When','_Returns','_Can','_Has','_Is'):
        if token in original_name: return original_name.replace(token, f'_{suffix}{token}', 1)
    return f'{original_name}_{suffix}'
def build_attribute_block(attrs: str, trait: Trait) -> str:
    return TRAIT_PATTERN.sub('', attrs) + f'[Trait("{trait.key}", "{trait.value}")]\n'
def process_file(path: Path) -> Change | None:
    original=path.read_text(encoding='utf-8-sig'); replacements=[]
    for match in METHOD_PATTERN.finditer(original):
        attrs=match.group('attrs'); method_name=match.group('name')
        if not FACT_PATTERN.search(attrs): continue
        traits=[Trait(m.group('key'), m.group('value')) for m in TRAIT_PATTERN.finditer(attrs)]
        if len(traits)<=1: continue
        open_brace_index=original.find('{', match.start('sig'))
        if open_brace_index<0: continue
        try: close_brace_index=find_matching_brace(original, open_brace_index)
        except ValueError: continue
        method_core=original[match.start('sig'):close_brace_index+1]
        generated_blocks=[]; generated_names=[]
        for trait in traits:
            new_name=trait_method_name(method_name, trait.key)
            if re.search(rf'\b{re.escape(new_name)}\s*\(', original): continue
            new_method_core=re.sub(rf'\b{re.escape(method_name)}\s*\(', f'{new_name}(', method_core, count=1)
            generated_blocks.append(build_attribute_block(attrs, trait)+new_method_core); generated_names.append(new_name)
        if generated_blocks:
            replacements.append((match.start(), close_brace_index+1, '\n\n'.join(generated_blocks), Change(path, method_name, [t.key for t in traits], generated_names)))
    if not replacements: return None
    updated=original
    for start,end,replacement,_ in reversed(replacements): updated=updated[:start]+replacement+updated[end:]
    path.write_text(updated, encoding='utf-8')
    return Change(path, ', '.join(r[3].method_name for r in replacements), [key for r in replacements for key in r[3].trait_keys], [name for r in replacements for name in r[3].generated_methods])
def append_section(path: Path, title: str, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True); existing=path.read_text(encoding='utf-8') if path.exists() else ''
    if title in existing: return
    content=(existing.rstrip()+'\n\n') if existing.strip() else ''
    content += f'{title}\n\n{body.strip()}\n'
    path.write_text(content, encoding='utf-8')
def write_report(changes: list[Change]) -> None:
    report=ROOT/'docs'/'xunit-trait-method-duplication-report.md'; report.parent.mkdir(parents=True, exist_ok=True)
    lines=['# xUnit Trait Method Duplication Report','','Generated by RDEL package 008.','','Purpose: split xUnit `[Fact]` methods with multiple `[Trait]` attributes into separate physical test methods so external test-count tools can count each category.','','## Changed files','']
    if not changes: lines.append('No multi-trait xUnit `[Fact]` methods were found.')
    else:
        for change in changes:
            rel=change.path.relative_to(ROOT); lines += [f'### `{rel}`','',f'- Original method(s): `{change.method_name}`', f"- Trait keys: {', '.join('`'+k+'`' for k in change.trait_keys)}", '- Generated methods:']
            for method in change.generated_methods: lines.append(f'  - `{method}`')
            lines.append('')
    report.write_text('\n'.join(lines).rstrip()+'\n', encoding='utf-8')
def update_docs() -> None:
    append_section(ROOT/'docs'/'DECISIONS.md', '## 2026-07-01 — xUnit Trait Counting Compatibility', 'Decision: xUnit `[Fact]` methods that need to count under more than one trait category must be represented as separate physical test methods, one trait per method.\n\nReason: the external counting tool does not correctly count multiple `[Trait]` attributes on a single xUnit test method.\n\nAvoid relying on one method with multiple traits when the result must be counted by the external tool.')
    append_section(ROOT/'docs'/'AI_INSTRUCTIONS.md', '## xUnit Trait Counting Rule', 'When generating xUnit `[Fact]` tests for this repository, do not put multiple category-counting `[Trait]` attributes on the same method.\n\nIf a test must count for multiple categories, generate one physical method per trait. Each method should have exactly one counting trait and a method name that includes the trait key.')
    append_section(ROOT/'docs'/'memory.md', '## xUnit trait counting compatibility', 'The external counting tool does not correctly count multiple xUnit `[Trait]` attributes on one method. Use duplicated physical test methods with one trait each when a test must count under multiple categories.')
    append_section(ROOT/'docs'/'context.md', '## xUnit trait method duplication', 'For xUnit tests, multiple category traits on one method are not reliable for the external counting tool. The repository uses one physical `[Fact]` method per countable trait when categories must be counted separately.')
def main() -> None:
    changes=[]
    for path in iter_csharp_files():
        change=process_file(path)
        if change is not None: changes.append(change)
    write_report(changes); update_docs()
    print(f'xUnit trait method duplication complete. Changed files: {len(changes)}')
    print('Report: docs/xunit-trait-method-duplication-report.md')
if __name__ == '__main__': main()
