# Change Log

## 0.2.0

- Grammar aligned with **Ct 1.1.0** (`ct-lang` tag `v1.1.0`, commit
  `aa223cf1`).
  - Expression `match` (LANG-29 B5): `ct-match-arm` gives the `Pattern => expr`
    arm arrow `keyword.operator.match-arm.ct` instead of `ct-closure-arrow`;
    the variant keeps the same `entity.name.type.adt.ct` /
    `entity.name.function.variant.ct` scopes as `ct-adt-construct`, so the
    statement form highlights exactly as before. `ct-yield` colours a
    statement-initial `yield` (`int yield = 1;`, `goto yield;`, `x.yield`,
    strings and comments are unaffected).
  - Optional chain (Phase 53): `ct-optional-chain` colours `?.` / `?[` in
    `p?.f` and `p?[i]`. `c?.5 : 1.0` stays the conditional operator (the `?` is
    followed by a float), and the statement-tail `g()?` stays `ct-try`.
  - `box<T>` removal: `ct-box-type` now matches `Box<T>` only; the lower-case
    alias maps to `ct-box-alias-removed` → `invalid.deprecated.ct`. Snippets
    spell `Box<` only. A bare `Box` / `box` identifier is untouched.
  - Line-level approximations are documented in the README: block-bodied value
    arms keep `ct-closure-arrow`, and `yield` is recognised at statement start
    only.
- VS Code language display name: the first language alias is now `Ct` (it was
  `CT`), so the language selector / status bar reads **Ct — C with Traits**,
  matching the extension name. `CT` and `ct` remain accepted aliases.
- Anti-drift gate: `test/surface.json` + `test/check-surface.py` (51 entries in
  four groups: top-level / keywords / control / types) assert that every
  CT-only construct still has a rule and a fixture hit. `npm test` now runs
  `check-index → check-grammar → check-surface`.
- Fixtures re-taken from `ct-lang` `v1.1.0` (`aa223cf1`): 54 files, including
  `302_adt_match_expr`, `301_adt_methods`, `303_map_binding`, the `p53_*`
  optional-chain samples and the surface-gate samples
  (`236_result_try_defer`, `231_str_ops`, `p80_retain/borrow_out_ref.ct`,
  `p81_box/layout.ct`). `test/fixtures/README.md` records the tag, commit, file
  list and count; the surface gate checks that record against the files on disk.
- `test/check-grammar.py`: 220 checks, up from 182 at 0.6.1.
- Version line: the Marketplace line is **0.0.1 → 0.1.0 → 0.2.0**. The `0.6.x`
  entries below are the pre-split extension line and were never published; as
  before, the extension version is independent of `CTC_VERSION`.

## 0.6.1

- v0.88 language surface: 10 new rules.
  - `ref` / `out` (`ct-ref`, `ct-out`).
  - `box<T>` / `new` (`ct-box-type`, `ct-new`).
  - `String` / `Str` / `U16String` / `U16Str` (`ct-owned-type`).
  - slices `T[]` (`ct-slice-type`).
  - ADT constructors `Shape.Circle(…)` (`ct-adt-construct`) and `match (…)`
    (`ct-adt-match`).
  - postfix `?` (`ct-try`) and `$name` materialization (`ct-materialize`).
- `$` stays `variable.language.range-index.ct` only when it is not followed by
  an identifier, so `$x` and range `$` do not steal each other's scope.
- Snippets: `box`, `String`, `Str`, `slice`, `adt`, `match`, `refout`, `try`.
- `test/check-grammar.py`: 179 assertions, up from 168, with a v0.88 synthetic
  fixture covering all new rules.
- Repository: the extension moved out of `ct-lang`'s `editors/vscode` into the
  standalone [ct-vscode](https://github.com/samxxu/ct-vscode) repository.
  `package.json` metadata points at the new home, the grammar samples are copied
  into `test/fixtures/` so the tests no longer read anything outside this repo,
  and GitHub Actions now builds the `.vsix` on every push and publishes on a
  `v*` tag. The extension version stays **0.6.1**; it is its own line and does
  not track the compiler's `CTC_VERSION`.

## 0.6.0

- Phase 29 syntax, 12 new rules: `foreach (xs)` (`ct-foreach`), the built-in
  container protocol `Vec<T>` / `Map<K,V>` after `.` or `->`
  (`ct-container-method`: `push`, `get`, `set`, `pop`, `clear`, `retain`,
  `release`, `put`, `remove`, `entry`, `len`, `from`), the type-instantiation
  position `Vec<int> nums;` / `Map<char *, int> ages;` / `Box<Box<int>>`
  (`ct-generic-type`), the static path `Vec<char *>::from(…)`
  (`ct-generic-static-call`), `struct Stack<T> {` and `pub struct Pair<T, U> {`
  (`ct-generic-struct`), `impl<T> Stack<T> {` / `impl<T> Stack<T> use Show {`
  (`ct-generic-impl`), and `item.key` / `item.value` as the `Map` entry pair
  (`ct-foreach-entry`). `ct-generic-decl` now accepts a trait constraint
  (`T max2<T: Ord>(T a, T b)`).
- Phase 30 receiver blocks: `into` as a contextual keyword (`ct-into`, only when
  a `{` follows, so `int into = 1;` stays an identifier), the leading-dot body
  members `.field = v;` / `.method(args);` (`ct-into-field`, `ct-into-method`),
  and the inline spelling `into { .field = v; }`
  (`ct-into-inline-field`, `ct-into-inline-method`). Suffix chains
  (`}.add(2)`, `}->field`, `}[1]`) stay outside the block and are left to C.
- A line that starts with `.name` is scoped as a property/method, which is also
  the correct reading of a multi-line designated initializer; the grammar never
  takes a `{` on its own as the start of an `into` block, so
  `Person p = { .name = … }` is not treated as a receiver block.
- `$` keeps one scope, `variable.language.range-index.ct`: the range
  initializer and the `into` receiver are both `$`, and a line-oriented grammar
  cannot tell them apart. `item` / `i` are not coloured globally — only
  `item.key` / `item.value` are provable without block scope — so a user
  variable named `item` is never mis-highlighted.
- Snippets: `foreach`, `foreachmap`, `vec`, `mapvar`, `generic`,
  `genericbound`, `structg`, `implg`, `into`, `rangeinit`, `vecrange`.
- `test/check-grammar.py`: 168 assertions (167 without node), up from 109, with the Phase 29/30
  fixtures (`examples/21`, `22`, `23`, `24`, `26`, `29`, `test/ast/138`,
  `test/ast/147`) scanned by the gate.

This extension has its own version line; 0.6.0 does not affect the compiler's
`CTC_VERSION`.

## 0.5.1

- Go to definition now resolves a generic declaration `T id<T>(T x)` in
  K&R and Allman bodies, as an `impl` method and as a trait default body. The
  jump target is the declaration line only: `id<int>(42)` and `id<char *>(p)`
  both resolve to `id`, never to an instantiation.
- The indexer is now a plain CommonJS module (`indexer.js`) with executable
  assertions (`test/check-index.js`, 26 cases, run by `check-grammar.py` when
  `node` is present).

This extension has its own version line; 0.5.1 does not affect the compiler's
`CTC_VERSION`.

## 0.5.0

- Highlighting for the Phase 20–26 syntax, 17 rules in all: `type` / `pub type`
  aliases (`ct-type-alias`), generic declarations and calls
  (`ct-generic-decl`, `ct-generic-call`), `loop(n)` / `loop(a..b)`
  (`ct-loop`), the `a..b($)` range operator (`ct-range-dots`), the closure
  arrow `=>` (`ct-closure-arrow`), `_Static_assert` / `static_assert`
  (`ct-static-assert`), the C11 surfaces `_Alignas` (`ct-alignas`),
  `_Alignof T` / `_Alignof(T)` (`ct-alignof-type`, `ct-alignof`), `_Atomic`
  (`ct-atomic`), `_Generic` (`ct-generic-select`), `_Noreturn`
  (`ct-noreturn`), `_Thread_local` (`ct-thread-local`), `_Bool` / `_Complex` /
  `_Imaginary` (`ct-c11-builtin-types`), GNU `__attribute__((…))`
  (`ct-attribute`), and `map` recipes `name(args) -> callee(…)`
  (`ct-recipe`).
- `ct-map` accepts a qualified instance host (`for instance hal::uart1`) and
  splits the `::` path from the host name.
- Contextual keywords stay contextual: `int loop = 5;`, `loop:`, `...`,
  `a >= b`, `p->x`, `dog_get()->hi();` and `return id<int>(42);` are all
  pinned by negative assertions.
- `test/check-grammar.py`: 108 assertions (40 before), with the Phase 20–26
  fixtures under `test/ast/` and `test/modules/map_ns/`; every new assertion
  was shown to fail by mutating its rule.
- `extension.js` is unchanged. The go-to-definition index still does not
  register generic function/method templates (`T id<T>(T x)`); the gap and its
  fix criteria are recorded as DOC-68 in `issues/docs/`.

## 0.4.0

- Highlighting for raw pass-through (Phase 17.3): `#ct-raw` / `#ct-endraw`
  form an embedded block (`meta.raw.ct`) whose body is left to the C grammar,
  so a macro or a hand-written function inside it is not read as a Ct construct.
- `test/check-grammar.py`: 36 assertions, adding the raw marker pair and a
  "no Ct keyword inside the block" check.

## 0.3.0

- Highlighting for `borrow` (`storage.modifier.borrow.ct`) in both of its
  contextual-keyword forms: a statement-initial declaration (`borrow struct
  Conn *c = …`) and a parameter annotation (`void render(borrow struct Conn *c)`).
- The built-in traits `Handback` and `Drop` highlight as trait types.
- `test/check-grammar.py`: 33 assertions, covering the two `borrow` forms.

## 0.2.0

- Highlighting for the batch-36 / batch-38 syntax: `map trait T for namespace
  A::B`, `map trait T for type char *` (the host C type is left to the C
  grammar), and trait default method bodies. `.m.ct` mapping units need no
  extra registration — the `.ct` suffix already covers them.
- Go-to-definition for the same features: trait default methods (an `impl`
  override wins, otherwise the body in the trait; `self->m()` inside a default
  body stays in that trait; `} use T;`-only structs resolve), zero-cost static
  mapping calls (`a.toInt()` on a `char *`/array receiver via the
  `for type` host, and `Host::Trait.method(…)` via the `for namespace` host),
  and `map` bindings keyed by the mapped instance.
- `test/check-grammar.py`: 31 assertions, covering the two new `map` hosts and
  the default-method fixtures.

## 0.1.0

- Go-to-definition (`Ctrl+Click` / `F12`) for `.ct` files via a single
  dependency-free `extension.js`: `impl` methods (narrowed by the receiver's
  declared struct), trait/struct declarations, trait method declarations,
  top-level functions, `Qual::name` calls, and `map` bindings.
- Highlighting fixes: `import … as Alias;`, headers whose tokens are split by
  comments or line breaks (`trait` / `impl` / `map`), and `pub` is no longer
  matched mid-line (so `int pub = 1;` stays plain).
- `test/check-grammar.py`: 27 assertions, including the import alias, the
  comment-split headers and the anchored `pub`.

## 0.0.1

Initial release.

- Syntax highlighting for the Ct-specific constructs: `trait` definitions,
  `impl … for …` blocks, `use` clauses (including comma-separated lists) and
  the implicit `self` receiver. Everything else is delegated to VS Code's
  built-in C grammar via `include: source.c`.
- Strings and comments are tokenised before the Ct rules, so the compiler's
  "never touch anything inside a string, char or comment" guarantee holds for
  the highlighter too.
- Language configuration: line/block comments, brackets, auto-closing and
  surrounding pairs, brace indentation, block-comment continuation on Enter.
- Snippets: `trait`, `structuse`, `impl`, `method`, `call`.
- `test/check-grammar.py`: a dependency-free smoke test (13 assertions at
  release) that replays the grammar's patterns over the demos and
  checks both directions — the Ct rules fire on `trait` / `use` / `impl` /
  `self`, and stay silent inside comments, strings and look-alike identifiers
  (`use_it`, `selfish`).
