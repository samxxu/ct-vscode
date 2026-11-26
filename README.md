# Ct — C with Traits for VS Code

[![CI](https://github.com/samxxu/ct-vscode/actions/workflows/ci.yml/badge.svg)](https://github.com/samxxu/ct-vscode/actions/workflows/ci.yml)

Syntax highlighting, snippets, go-to-definition and language configuration for
**Ct**, the trait-flavoured C compiled by
[`ct`](https://github.com/samxxu/ct-lang) (`ctc` remains a compatibility alias).

This repository is the standalone home of the extension; it was split out of
`ct-lang`'s `editors/vscode` directory and is built, tested and released on its
own.

**Requirements**

- VS Code 1.75 or newer.
- `ct` 1.1.0 or newer to get the whole 1.1 language surface highlighted
  (expression `match` arms `Pattern => expr` and `yield`, optional chain
  `p?.f` / `p?[i]`, `ref` / `out`, `Box<T>` (the lower-case `box<T>` alias is a
  hard error in 1.1), `String` / `Str`, slices, ADT / `match`, `?`, `$name`).
  Older compilers still work — the extension is a syntax superset and simply
  has nothing to highlight for constructs that did not exist yet.
- The extension version line is **independent of `CTC_VERSION`**: 0.2.0 here
  means "0.2.0 of the VS Code extension", not "0.2.0 of the compiler".

```c
trait Greeter {
    void greet();
}

struct Person {
    char *name;
} use Greeter;

impl Greeter for Person {
    void greet() {
        printf("Hello, %s\n", self->name);
    }
}
```

## What it gives you

| Construct | Highlighted as |
| --- | --- |
| `trait Greeter {` | `storage.type` + `entity.name.type` |
| `} use Greeter, Counter;` | `keyword` + one `entity.name.type` per trait |
| `impl Greeter for Person {` | `storage.type`, `keyword`, two `entity.name.type` |
| `self->name` | `variable.language`（`self` 是语言内建接收者） |
| `import a::b as C;` | `keyword` + namespace path + alias |
| `map trait T for instance x {` | `storage.type` + trait/instance names |
| `map trait T for namespace A::B {` | `storage.type` + trait/host names |
| `map trait T for type char * {` | `storage.type` + trait name, host type by the C grammar |
| `trait T { m() { … } }` | `trait`, then the default body as C |
| `own`, `borrow`, `delete`, `pub`, `namespace` | modifiers/keywords at line start |
| `T id<T>(T x)` / `id<int>(…)` | generic declaration / call (type parameter + type argument) |
| `type Name = …;` / `pub type Name = …;` | `storage.type` + alias name |
| `loop(n) {` / `loop(a..b) {` | `keyword.control` for `loop` |
| `0..13($ * 2 + 1)` | `..` range operator + `$` range index |
| `(int x) => expr` | closure arrow |
| `_Static_assert(…)` / `static_assert(…)` | `keyword.control` |
| `_Alignas`, `_Alignof T`, `_Atomic`, `_Generic`, `_Noreturn`, `_Thread_local`, `_Bool` | C11 keywords |
| `__attribute__((…))` | `storage.modifier` |
| `write(buf, len) -> uart_put;` | recipe method + `->` |
| `foreach (xs) { … }` | `keyword.control`, plus `item.key` / `item.value` for a `Map` entry |
| `struct Stack<T> {` / `pub struct Pair<T, U> {` | `storage.type` + struct name + type parameters |
| `impl<T> Stack<T> {` / `impl<T> Stack<T> use Show {` | `storage.type` + type parameters + target + `use` trait |
| `T max2<T: Ord>(T a, T b)` | generic declaration with its trait constraint |
| `Vec<int> nums;` / `Map<char *, int> ages;` | built-in container instantiation (`Box<Box<int>>` nests) |
| `Vec<char *>::from(…)` | static call path: type arguments + `::` + method |
| `.push(…)`, `.get(…)`, `.put(…)`, `.entry(…)`, `.len()`, `.from(…)` | `support.function` for the `Vec` / `Map` protocol (`->` included) |
| `cfg into {` + member lines | `keyword.control` + `variable.other.property` for the leading `.field` / `.method` |
| `cfg into { .backlog = 64; }` | the inline spelling gets the same scopes (`ct-into-inline-field` / `ct-into-inline-method`) |
| `p into { … }.add(2)` / `}->port` / `}[1]` | suffixes stay ordinary C after the block |
| `ref int r` / `out int v` | `storage.modifier` for the call-site sugar |
| `Box<Record> r = new Record { … }` | `Box` type + `new` keyword (`box<T>` was removed in 1.1) |
| `String s = "hi";` / `Str view = s.as_str();` | built-in owning / borrowed string types |
| `int[] nums` | slice type `T[]` |
| `enum Shape { Circle(int r), Empty() }` | payload members make it an ADT |
| `Shape.Circle(2)` / `match (s) { … }` | variant constructor + `match` keyword |
| `Shape.Circle(r) => expr` / `_ => expr` | arm arrow `keyword.operator.match-arm.ct`; the variant keeps the ADT scopes |
| `yield expr;` | `keyword.control.yield.ct` (contextual; only at statement start) |
| `g()?` | postfix `?` error propagation |
| `p?.f` / `p?[i]` | optional chain (`keyword.operator`; `c?.5 : 1.0` stays a conditional) |
| `box<Record> r = …` | `invalid.deprecated` — the 1.1 compiler removed the alias |
| `a.m()$x.n()` | `$x` materialization target |

`.m.ct` mapping units are plain `.ct` files to the editor (the suffix still
ends in `.ct`), so they get the same highlighting; `#include` / `#define`
prologues are handled by the C grammar.

Everything else — strings, comments, preprocessor lines, types, function
bodies — is **VS Code's own C grammar**, pulled in with `include: source.c`.
No duplicated C grammar to maintain and nothing to drift.

### Known line-level approximations

The grammar is line-oriented, so a few constructs are approximated rather than
scoped exactly:

- `yield` is coloured only when it starts a statement (leading whitespace
  allowed). That is the arm exit's normal spelling; a `yield` outside an arm is
  illegal code and is still coloured, and a `yield` that shares its line with
  other code is not coloured.
- A value arm whose block is `Pattern => { … yield … }` looks the same as a
  statement arm on one line, so its arrow keeps `ct-closure-arrow`; only the
  `Pattern => expr` spelling gets `ct-match-arm`.

## Go to definition

`Ctrl+Click` / `F12` works inside `.ct` files without any C/C++ extension:

- `p.greet()` → the matching `impl Greeter for Person` method. The receiver's
  struct is taken from `Person p`, `Person *p`, parameters, or `self` inside
  an `impl` block; if it cannot be inferred, every same-name method is offered
  in the peek list.
- `Controller::send` → the function/type in `namespace Controller` (or the
  namespace that owns the type).
- Plain names → trait/struct declarations, `impl` methods, trait method
  declarations (abstract and default bodies), top-level functions (`pub` and
  Allman-style bodies included).
- Generic declarations (Phase 26): `T id<T>(T x)` is indexed in both K&R and
  Allman bodies, as an `impl` method or a trait default body. The jump target is
  the declaration line only — `id<int>(42)` and `id<char *>(p)` both resolve to
  the `id` declaration, never to an instantiation.
- `c.send()` against a `map`-ed instance → the `map` binding when the receiver
  is the mapped global.
- Trait default methods (batch 36): `c.write_all()` → the impl override when
  one exists, otherwise the default body in the trait; `self->m()` inside a
  default body resolves within that trait; a struct that only wrote
  `} use T;` still resolves.
- Zero-cost static mapping (batch 38): `a.toInt()` on a `char *` receiver
  (arrays decay) → the trait method of the `map trait T for type char *`
  binding, and `libc::Env.get(…)` → the trait method of the
  `map trait T for namespace libc` binding.

The index is built by scanning workspace `.ct` files (`.m.ct` included) on
first use and is invalidated on edits/saves. It is a line-oriented
approximation of the compiler's rules, not a full semantic analyzer: same-name
methods across structs may show multiple candidates, fields are not indexed,
and call sites inside strings/comments still resolve as words.

Strings, chars and comments are tokenised *before* the Ct rules, so the
compiler's core guarantee ("never touch anything inside a string, char or
comment") holds for the highlighter too: `printf("use self here")` stays a
plain string.

Also included: comment and bracket configuration, auto-closing and surrounding
pairs, brace-based indentation, block-comment continuation on Enter, and the
snippets `trait`, `structuse`, `impl`, `method`, `call`, `foreach`,
`foreachmap`, `vec`, `mapvar`, `generic`, `genericbound`, `structg`, `implg`,
`into`, `rangeinit` and `vecrange`.

Two bindings of `$` cannot be told apart by a line-oriented grammar: the range
initializer (`0..n($)`) and the `into` block (`report($)`) share
`variable.language.range-index.ct`. Likewise `item` and `i` are ordinary
identifiers outside the tokens the grammar can prove (`item.key`,
`item.value`); they are never coloured globally, so a user variable named
`item` is not mis-highlighted.

The grammar, snippets and language configuration are **declarative JSON — no
build step**. Navigation is split into `extension.js` (VS Code API only) and
`indexer.js` (the pure line scanner), using only Node's `fs`, so there are still
**no third-party dependencies**. The `.ct` sources are not compiled by this
extension; use `ct` (or the `ctc` alias) for that.

## Install

From the [Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=samxxu.ct-vscode)
(search for “Ct — C with Traits”), or from a local checkout:

```bash
git clone https://github.com/samxxu/ct-vscode.git
cd ct-vscode
npm ci
npx vsce package
code --install-extension ct-vscode-0.2.0.vsix
```

For extension development, open this repository in VS Code and press `F5`
(`.vscode/launch.json` is not committed; the Run Extension configuration uses
`${workspaceFolder}` as `--extensionDevelopmentPath`). Alternatively symlink the
checkout into your extensions folder and reload VS Code:

```bash
ln -s "$PWD" ~/.vscode/extensions/ct-vscode
```

## Checks

```bash
npm test                        # all three gates, in one go
node test/check-index.js        # the indexer's own 26 assertions, runnable without VS Code
python3 test/check-grammar.py   # grammar behaviour (also re-runs the index checks)
python3 test/check-surface.py   # every CT-only construct still has a rule + a fixture hit
```

The script replays the grammar's patterns with Python's `re` over the samples in
`test/fixtures/`, which mirror the paths those files had in `ct-lang`
(`examples/…`, `test/cases/…`, `test/ast/…`, `test/modules/…`). The tests are
self-contained: nothing outside this repository is read.

`test/check-surface.py` is the anti-drift gate: `test/surface.json` maps each
CT-only construct (grouped as top-level / keywords / control / types) to a rule
name, a fixture and a line selector. Renaming or deleting a rule, or dropping a
fixture, fails the gate. `test/fixtures/README.md` records where the corpus came
from (upstream tag, commit, file count) and the gate checks that it still
matches the files on disk.

Assertions run in both directions: the Ct rules fire on `trait` / `use` /
`impl` / `self` / `loop` / `..` / `=>` / generics, and they stay silent inside
comments, strings and look-alike identifiers (`use_it`, `selfish`, `...`,
`int loop = 5`, `p->x`).

It is a smoke test, not a substitute for a human pass: Python's `re` is not
Oniguruma, and the real engine also runs VS Code's built-in `source.c` grammar,
which the script deliberately does not emulate. Open a `.ct` file in VS Code
once before publishing.

## Package and publish

```bash
npm ci
npm test
npm run package                 # -> ct-vscode-0.2.0.vsix
npm run publish                 # local publish needs a Marketplace PAT; CI uses OIDC
```

CI ([ci.yml](.github/workflows/ci.yml)) builds the `.vsix` on every push and
pull request and uploads it as an artifact. [release.yml](.github/workflows/release.yml)
publishes on a `v*` tag with **Trusted Publishing (GitHub OIDC)** — no PAT
secret is involved.

Two things are needed before publishing:

- **`publisher`** in `package.json` must match your
  [Marketplace publisher id](https://marketplace.visualstudio.com/manage)
  (currently set to `samxxu`).
- **`icon.png`** — a 128×128 PNG referenced as `"icon": "icon.png"`.
  It is intentionally absent from the repo; add your own before publishing
  (`vsce` still packages without it, but the listing looks bare).

## License

MIT — see [LICENSE](LICENSE). The compiler itself is GPL-3.0-or-later with an
output exception; see the [ct-lang repository](https://github.com/samxxu/ct-lang)
for details.

---

## 中文说明

给 **Ct（C with Traits）** 用的 VS Code 扩展：语法高亮 + 代码片段 + 跳转定义 + 编辑器配置。

- 本仓是扩展的独立仓库（自 `ct-lang` 的 `editors/vscode` 迁出），可独立测试、构建、发布。
- **要求**：VS Code 1.75+；`ct` 1.1.0 及以上可完整高亮 1.1 语言面（表达式 `match` 值臂与
  `yield`、可选链 `p?.f` / `p?[i]`、`ref` / `out`、`Box<T>`（小写 `box<T>` 在 1.1 是硬错）、
  `String` / `Str`、切片、ADT / `match`、`?`、`$name`），更老的 `ct` 同样可用，只是新构造没有对应规则。
- **版本线独立**：扩展版本与编译器的 `CTC_VERSION` 无关，0.2.0 指的是扩展本身的版本。
- **安装**：Marketplace 搜 “Ct — C with Traits”，或 `npm ci && npx vsce package` 后用
  `code --install-extension ct-vscode-0.2.0.vsix` 本地安装。

- **Ct 独有构造**（`trait` 定义、`use` 子句含逗号列表、`impl … for …`、隐式 `self`）由本扩展高亮；
  **其余全部交给 VS Code 内置的 C 语法**，不需要维护一份 C 语法副本。
- `import a::b as C;`、`map trait T for instance x {`、跨行或被注释分隔的 `trait` / `impl` / `map` 头部均已覆盖。
- **最新特性**：第三十六批的 trait 默认方法（方法体直接写在 trait 里），以及第三十八批的
  `.m.ct` 零成本静态映射（`map trait T for namespace A::B {`、`map trait T for type char * {`，
  `for type` 之后的 C 类型交给 C 语法）。`.m.ct` 映射单元与 `.ct` 用同一套高亮（文件名仍以 `.ct` 结尾）。
- Phase 20–26 的语法同样覆盖：`type` / `pub type` 类型别名、闭包箭头 `=>`、
  `loop(n)` / `loop(a..b)` 与 range 初值 `a..b($)`、泛型声明 `T id<T>(T x)` 与调用 `id<int>(…)`、
  C11 `_Alignas` / `_Alignof` / `_Atomic` / `_Generic` / `_Noreturn` / `_Thread_local` / `_Bool`、
  GNU `__attribute__((…))`，以及 `map` recipe 方法 `write(buf, len) -> uart_put;` 与限定宿主
  `for instance hal::uart1`。这些关键字都是上下文相关的：`int loop = 5;`、`loop:`、`...`、
  `a >= b`、`p->x`、`return id<int>(42);` 均不会被误判。
- 字符串、字符、注释**先于** Ct 规则被整体吃掉，因此编译器"字符串/注释内绝不改写"的保证在高亮层面同样成立。
- **跳转定义**：`Ctrl+Click` / `F12` 可跳到 `impl` 方法、trait/struct 声明、顶层函数与 `map` 绑定；
  `p.greet()` 会按 `p` 的声明类型收窄到对应 `impl`，`self` 取当前 `impl`（默认方法体内则取当前 trait）。
  新特性同样可跳：trait 默认方法（impl 覆盖优先）、静态映射的 `a.toInt()`（按接收者 C 类型 +
  `for type` 宿主匹配）与命名空间调用 `libc::Env.get(…)`；Phase 26 的泛型声明
  `T id<T>(T x)` 也可跳（K&R / Allman / `impl` 方法 / trait 默认体），口径是**只到声明行、
  不区分实例化**。
  它是按行扫描的近似索引，不做完整类型推导：同名方法可能给出多个候选，字段不建索引，字符串/注释里的词也会被当作名字解析。
- 语法与片段仍是纯声明式 JSON，跳转逻辑拆成 `extension.js`（只用 `vscode` API）与
  `indexer.js`（纯行扫描器，可被 Node 直接断言），**无构建、无运行时依赖**，可直接
  `npm run package` 打包；测试用 `npm test`，样例都在 `test/fixtures/`，不依赖其它仓库。
- 发布前需要补两样：`package.json` 里的 `publisher` 改成你真实的 Marketplace 发布者 ID，以及自备一张 128×128 的 `icon.png`；
  GitHub Actions 发布走 **Trusted Publishing（OIDC）**，无需 PAT secret（tag `v*` 触发 [release.yml](.github/workflows/release.yml)）。
