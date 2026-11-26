---
phase-id: VS-PH-1
extension-minor: 7
---

# VS-PH-1 — 表达式 `match` 与 `yield`（LANG-29 B5）

> **状态：待开始**。目标扩展版本 `0.7.0`。
> **前置**：无（可在 VS-PH-2/3 之前或之后做，但同一时刻只开一张卡）。
> **上游依据**：`ct-lang` `v1.1.0`（`aa223cf1`），spec §4.73「最小 ADT 与 `match`」，
> 表达式 match 段（行 3290–3297）；样例 `test/ast/302_adt_match_expr/prog.ct`。

## 0 卡片字段（冻结）

| 项 | 值 |
| --- | --- |
| 编号 | `VS-PH-1`（扩展 `MINOR = 7` ↔ `0.7.0`） |
| 目标 | 让 1.1.0 的**表达式 `match`** 在编辑器里可见：值臂箭头 `=>` 有自己的作用域，`yield` 作为臂内关键字着色；语句 `match` 与闭包 `=>` 不回归 |
| 范围 | 语法 2 条新规则 + 1 条顺序约束；新增 fixtures 与断言；README 构造表两行；CHANGELOG `0.7.0` |
| 非目标 | 模式语法扩展（字面量/嵌套/struct/或模式、守卫，属 1.2）；`yield` 唯一出口等语义校验；`indexer.js` 跳转；`box` 与可选链（各自独立卡） |
| 交付物 | `syntaxes/ct.tmLanguage.json` 改动、`test/fixtures/` 三份样例、`test/check-grammar.py` 新断言、README/CHANGELOG、`0.7.0` 打包 |
| 任务清单 | §2（S1 红 / S2 实现 / S3 收口，四列齐全） |
| 退出判据 | `E-VS-1-1 … E-VS-1-8`（§3） |
| version-minor | 7 |
| 已知风险 | `R-VS-1-1 … R-VS-1-4`（§4） |

## 1 入口与闸

| 闸 | 内容 | 现状 |
| --- | --- | --- |
| 上游 | `ct-lang` tag `v1.1.0` = `aa223cf1`；spec §4.73 行 3290–3297 | 已核对 |
| 基线 | 本仓 `main` 上 `npm test` 全绿（`check-index` 26 断言、`check-grammar` 182 检查） | 已核对 |
| 规范歧义 | 行式语法无法判定「`yield` 是否在 match 臂块内」——本卡采用**行首近似**并登记（见 §4 R-1） | 已裁定 |

## 2 任务

| 任务 | 交付 | 验收 | effort |
| --- | --- | --- | --- |
| S1 红 | 从 `ct-lang@v1.1.0` 复制三份样例到 `test/fixtures/test/ast/`：`302_adt_match_expr/prog.ct`、`errors/l29b5_yield_outside.ct`、`errors/l29b5_multi_yield.ct`；在 `check-grammar.py` 的 `CT_CASES` 加入 302，并写下表 6 条新断言 | 新断言**失败**，`python3 test/check-grammar.py` 退出码 1；原始输出贴入提交说明 | S |
| S2 实现 | 新增 `ct-match-arm`（值臂：`_` 或 `Type.Variant(bindings)` 或 `Variant(bindings)` 后的 `=>`）与 `ct-yield`（行首 `yield`）；`ct-match-arm` 排在 `ct-closure-arrow` 之前，`ct-adt-construct` 不受影响 | 新断言由红转绿；既有断言 0 失败 | M |
| S3 收口 | README「What it gives you」加两行（`Pattern => expr`、`yield`）；CHANGELOG `## 0.7.0`；`package.json` 版本 0.7.0；打包 | `npm test` 退出码 0；`npx vsce package` 成功并记录大小 | S |

### S1 断言清单（必须与实现一一对应）

| 断言文本（check 描述） | 条件 |
| --- | --- |
| `` `N.Leaf(v) => v,` -> ct-match-arm `` | 302 中该行命中 `ct-match-arm`，且**不**命中 `ct-closure-arrow` |
| `` `yield prod + 1;` -> ct-yield `` | 302 中该行命中 `ct-yield` |
| `` 表达式位置的 `int t = match (b) {` -> ct-adt-match `` | 该行命中 `ct-adt-match` |
| `字符串/注释里的 yield 与 => 不触发` | 字符串 `"yield x"`、注释 `// ... => ...` 行内无 `ct-yield` / `ct-match-arm` |
| `` `(int x) => x + 1` 仍是闭包 `` | 既有 `NEW088`/`CLOSURE` 合成样例不变 |
| `` `int yield = 1;` 不是 ct-yield `` | 合成样例：声明位置不触发 |

## 3 退出判据（二值）

| ID | 断言 |
| --- | --- |
| E-VS-1-1 | `test/ast/302_adt_match_expr` 的 `Pattern => expr` 行至少一条命中 `ct-match-arm` |
| E-VS-1-2 | 302 的 `yield prod + 1;` 行命中 `ct-yield` |
| E-VS-1-3 | `yield` / `=>` 在字符串、行注释、块注释内均不触发新规则 |
| E-VS-1-4 | 闭包 `(int x) => x + 1` 仍命中 `ct-closure-arrow`，且**不**命中 `ct-match-arm` |
| E-VS-1-5 | `int yield = 1;`、`goto yield;`、`x.yield` 不命中 `ct-yield` |
| E-VS-1-6 | 语句 `match`（302 的 `classic()`）着色与 0.6.1 完全一致（`ct-adt-match` + `ct-adt-construct` 不变） |
| E-VS-1-7 | `npm test` 退出码 0，`check-index` 与 `check-grammar` 均 `0 failed`（原始输出入库） |
| E-VS-1-8 | `npx vsce package` 成功，vsix 大小记录在收口报告；README 构造表与 CHANGELOG 已更新 |

## 4 风险与回滚

| # | 风险 | 处置 |
| --- | --- | --- |
| R-VS-1-1 | **行式近似**：`yield` 在臂外（非法代码）也会被着色为关键字 | 在 README「已知近似」写明：`yield` 以行首判定，臂外写法本就编译报错，不做块作用域推断 |
| R-VS-1-2 | `ct-match-arm` 抢走闭包 `=>` | 规则形状限制为「模式 + 箭头」，并以 E-VS-1-4 锁死；闭包含参数列表，不匹配模式形状 |
| R-VS-1-3 | 规则顺序错误导致 `=>` 仍落 `ct-closure-arrow` | `ct-match-arm` 放在 `ct-closure-arrow` 之前，顺序在 `scan order` 输出里可核对 |
| R-VS-1-4 | 302 引入的新构造（`impl Cell {` 等）干扰既有断言 | 302 只加断言、不改既有样例判定；必要时拆出仅含 match 的最小样例 |

回滚：语法改动、fixtures+断言、文档三笔独立提交；`0.7.0` 版本与 tag 单独回滚。

## 5 关联

- 规范：`ct-lang` `docs/language-spec.md` §4.73（行 3290–3297）、§3（行 231–257）
- 样例：`ct-lang` `test/ast/302_adt_match_expr/prog.ct`、`test/ast/errors/l29b5_yield_outside.ct`、`test/ast/errors/l29b5_multi_yield.ct`
- 上游卡：`ct-lang` `docs/phases/v1-PH-1/card.md`（S2b / E-V2-4）
- 本仓：[roadmap](../../roadmap.md) · [VS-PH-2](../VS-PH-2/card.md) · [VS-PH-4](../VS-PH-4/card.md)
