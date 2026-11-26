---
phase-id: VS-PH-2
extension-minor: 8
---

# VS-PH-2 — 可选链 `?.` / `?[`（Phase 53）

> **状态：待开始**。目标扩展版本 `0.8.0`。
> **前置**：无（与 VS-PH-1 无依赖；同一时刻只开一张卡）。
> **上游依据**：`ct-lang` `v1.1.0`（`aa223cf1`），spec §4.65「可选链 `?.` / `?[`」（行 2961）；
> 样例 `test/ast/p53_{ptr_field,field_ptr,chain,map_ptr_sub,ptr_sub,ternary_dot5}/prog.ct`。

## 0 卡片字段（冻结）

| 项 | 值 |
| --- | --- |
| 编号 | `VS-PH-2`（扩展 `MINOR = 8` ↔ `0.8.0`） |
| 目标 | 让 `p?.f`、`p?[i]`、`m["a"]?.c?.v` 的 `?.` / `?[` 有专属作用域；三目 `?:`、`c?.5`（`.5` 是浮点字面量）、语句尾 `?` 均不回归 |
| 范围 | 语法 1 条新规则 + 与 `ct-try` 的顺序约束；fixtures 与断言；README 构造表一行；CHANGELOG `0.8.0` |
| 非目标 | `T?` / `Maybe<T>`、可选方法调用 `p?.m()`、`p?.b = 1` 等 spec 明列范围外形态；`indexer.js`；`match`/`yield`（VS-PH-1）；`box`（VS-PH-3） |
| 交付物 | `syntaxes/ct.tmLanguage.json` 改动、`test/fixtures/` 五份样例、`check-grammar.py` 新断言、README/CHANGELOG、`0.8.0` 打包 |
| 任务清单 | §2（S1 红 / S2 实现 / S3 收口） |
| 退出判据 | `E-VS-2-1 … E-VS-2-8`（§3） |
| version-minor | 8 |
| 已知风险 | `R-VS-2-1 … R-VS-2-3`（§4） |

## 1 入口与闸

| 闸 | 内容 | 现状 |
| --- | --- | --- |
| 上游 | `ct-lang` tag `v1.1.0`；spec §4.65 行 2961–2976 | 已核对 |
| 切词裁定 | `?.` / `?[` 是解析期组合，不是词法 token；`?` 后接 `.数字` 时仍是三目（spec §4.65「切词」） | 已核对 |
| 基线 | `npm test` 全绿（182 检查），`ct-try` 只匹配语句尾 `?`（`(?=…[;,)\]}])`） | 已核对 |

## 2 任务

| 任务 | 交付 | 验收 | effort |
| --- | --- | --- | --- |
| S1 红 | 复制 `test/ast/p53_ptr_field`、`p53_field_ptr`、`p53_chain`、`p53_map_ptr_sub`、`p53_ternary_dot5` 到 `test/fixtures/test/ast/`；`CT_CASES` 加入这些样例；写下表 5 条新断言 | 新断言失败，`python3 test/check-grammar.py` 退出码 1；原始输出入库 | S |
| S2 实现 | 新增 `ct-optional-chain`：`\?(?=[.\[]…)` 两个分支——`\?\.(?![0-9])` 与 `\?\[`；排在 `ct-try` 之前 | 新断言转绿，既有断言 0 失败 | M |
| S3 收口 | README 构造表加「`p?.f` / `p?[i]` | `keyword.operator`」一行；CHANGELOG `## 0.8.0`；版本 0.8.0；打包 | `npm test` 0 failed；vsix 成功并记录大小 | S |

### S1 断言清单

| 断言文本 | 条件 |
| --- | --- |
| `` `m["a"]?.c?.v` -> 两个 ct-optional-chain `` | `p53_chain` 中该行命中 2 次 |
| `` `m?["k"]` -> ct-optional-chain `` | `p53_map_ptr_sub` 命中 |
| `` `c?.5 : 1.0` 不是可选链 `` | `p53_ternary_dot5` 该行无 `ct-optional-chain` |
| `` `g()?` 仍是 ct-try `` | 既有 `NEW088` 断言不变 |
| `` 字符串/注释里的 `?.` 不触发 `` | 合成样例 `"a?.b"`、`// a?.b` |

## 3 退出判据（二值）

| ID | 断言 |
| --- | --- |
| E-VS-2-1 | `p53_chain` 的 `full = m["a"]?.c?.v;` 行命中 `ct-optional-chain` 恰好 2 次 |
| E-VS-2-2 | `p53_map_ptr_sub` / `p53_ptr_sub` 的 `?[` 形态命中 `ct-optional-chain` |
| E-VS-2-3 | `p53_ternary_dot5` 的 `c?.5 : 1.0` 不打 `ct-optional-chain`，且 `?.5` 不吞掉后续比较/三目 |
| E-VS-2-4 | `a ? b : c`、`return x ? y : z;` 无 `ct-optional-chain` |
| E-VS-2-5 | 语句尾丢错传播 `g()?;` 仍为 `ct-try`，未被新规则改写 |
| E-VS-2-6 | 字符串、行注释、块注释中的 `?.` / `?[` 不触发 |
| E-VS-2-7 | `npm test` 退出码 0，两端 `0 failed`（原始输出入库） |
| E-VS-2-8 | `npx vsce package` 成功，大小记录；README/CHANGELOG 已更新 |

## 4 风险与回滚

| # | 风险 | 处置 |
| --- | --- | --- |
| R-VS-2-1 | 误吃三目：`c?.5` 被当成可选链 | 规则要求 `.` 后非数字，并以 E-VS-2-3 锁死；样例行来自上游 `p53_ternary_dot5` |
| R-VS-2-2 | 与 `ct-try` 顺序冲突，`?` 归属错乱 | `ct-optional-chain` 排在 `ct-try` 之前；E-VS-2-5 锁 `ct-try` 行为 |
| R-VS-2-3 | 与 `ct-adt-construct` / `ct-container-method` 叠加导致同一行多次着色 | 只断言 `?.` 本身的作用域，不断言整行 token 数；必要时把断言收窄到 `?.` 子串 |

回滚：语法、fixtures+断言、文档三笔独立提交；`0.8.0` 版本与 tag 单独回滚。

## 5 关联

- 规范：`ct-lang` `docs/language-spec.md` §4.65（行 2961–2976）、§3 语句层表「可选链」行
- 样例：`ct-lang` `test/ast/p53_chain/prog.ct`、`p53_ternary_dot5/prog.ct`、`p53_map_ptr_sub/prog.ct`、`p53_ptr_sub/prog.ct`、`p53_ptr_field/prog.ct`、`p53_field_ptr/prog.ct`
- 上游卡：`ct-lang` `docs/roadmap.md` Phase 53
- 本仓：[roadmap](../../roadmap.md) · [VS-PH-1](../VS-PH-1/card.md) · [VS-PH-4](../VS-PH-4/card.md)
