---
phase-id: VS-PH-1
extension-minor: 2
---

# VS-PH-1 — 语法对齐 Ct 1.1.0（单卡多 stage）

> **状态：进行中**。目标扩展版本 **`0.2.0`**；本卡一次做完，卡内 S0–S6 串行。
> **进度**：S1 红已提交 `f7c91e2`（`== 196 checks, 5 failed`）；S2 实现已提交 `d3a17ad`
> （`== 198 checks, 0 failed`）；S0 的语料重取与 S3–S6 未开始。
> **上游依据**：`ct-lang` tag `v1.1.0`（`aa223cf18e3ac143d066330569e537b8899ebbea`），
> `docs/language-spec.md` §3 / §3.1、§4.65、§4.71、§4.73。
> **覆盖缺口**：G-1 表达式 match 臂、G-2 `yield`、G-3 可选链、G-4 `box` 硬错、G-5 固有 impl 锁测、
> G-6 语料与声明落后（见 [roadmap](../../roadmap.md#2-差距清单本仓-v061-vs-ct-110)）。

## 0 卡片字段（冻结）

| 项 | 值 |
| --- | --- |
| 编号 | `VS-PH-1`（扩展 `MINOR = 2` ↔ `0.2.0`） |
| 目标 | 把扩展语法面从 v0.88 对齐到 **Ct 1.1.0**：表达式 `match` 与 `yield`、可选链 `?.` `?[`、`box<T>` 退场、语料与目标版本声明同步，并加一道语法面清单门禁 |
| 范围 | 语法规则、fixtures、`check-grammar.py` 断言、`test/check-surface.py` 门禁、README / CHANGELOG / `.vscodeignore`、版本与打包、收口提交与 tag |
| 非目标 | 304–307 模式与 §4.77 函子糖（1.2，未发布）；语义校验（`yield` 唯一出口、`box` 硬错判定由编译器负责）；`indexer.js` / `extension.js` 功能；发布渠道与账号迁移 |
| 交付物 | `syntaxes/ct.tmLanguage.json`、`test/fixtures/**`（按 `v1.1.0` 重取 + 新增样例）、`test/surface.json`、`test/check-surface.py`、`check-grammar.py` 断言、README/CHANGELOG、`0.2.0` vsix、`v0.2.0` tag |
| Stage 清单 | S0 语料与基线、S1 红、S2 match/yield、S3 可选链、S4 `box`、S5 语料与门禁、S6 收口（§2） |
| 退出判据 | `E-VS-1-01 … E-VS-1-18`（§3） |
| version-minor | 7 |
| 已知风险 | `R-VS-1-1 … R-VS-1-6`（§5） |

## 1 入口与闸

| 闸 | 内容 | 现状 |
| --- | --- | --- |
| 上游基准 | `ct-lang` tag `v1.1.0` = `aa223cf1`；spec §4.65 / §4.71 / §4.73 已核对 | 已核对 |
| 基线门禁 | 基线 `ede274b` 时 `npm test` 为 182 检查；S1 红提交后为 196 检查（新增 14 条） | 已核对 |
| 规范歧义 | 行式语法无法判定「`yield` 是否在 match 臂块内」，采用**行首近似**并登记（R-VS-1-1） | 已裁定 |
| **版本口径** | Marketplace 已发布 **0.1.0**（用户确认；gallery API 目前仍只列 0.0.1），**0.1.0 不可复用**，本卡目标改为 **0.2.0**；`0.6.x` 是拆分前的扩展线，从未上架。四处置数：`package.json` → `package-lock.json` 根 `version` → README → CHANGELOG | 已裁定（2026-11-27） |
| **发布凭据** | 收口要推 `v*` tag，会触发 `Release` 工作流（`vsce publish`）。**打 tag 前必须确认凭据可用**：`VSCE_PAT` secret 已存在，或工作流已改为 Trusted Publishing（OIDC） | **未完成，收口前必须补齐** |
| 红线 | 已推的 tag 不删、不强推、不改写历史；发布步骤失败只允许修凭据后 `gh run rerun` | 长期有效 |

## 2 Stage

| Stage | 主题 | 交付 | 验收 | effort |
| --- | --- | --- | --- | --- |
| S0 | 语料与基线 | 按 `v1.1.0` 重取 `test/fixtures/**`（现有清单 + `301_adt_methods`、`303_map_binding`、`302_adt_match_expr`、`p53_*`），新增 `test/fixtures/README.md` 登记 tag/commit/文件数 | E-VS-1-16；既有断言 0 失败 | M |
| S1 | 红 | 在 `check-grammar.py` 写出 S2–S4 的全部新断言（表达式 match/yield、可选链、`box`），`CT_CASES` 接入新样例 | 新断言**全部失败**，`python3 test/check-grammar.py` 退出码 1；原始输出入库 | S |
| S2 | 表达式 `match` + `yield` | `ct-match-arm`（值臂箭头）、`ct-yield`（行首），并把它排在 `ct-closure-arrow` 之前 | E-VS-1-01…05 转绿 | M |
| S3 | 可选链 `?.` / `?[` | `ct-optional-chain`（`\?\.(?![0-9])` 与 `\?\[`），排在 `ct-try` 之前 | E-VS-1-06…08 转绿 | M |
| S4 | `box<T>` 退场 | `ct-box-type` 收窄为 `\bBox\b`；新增 `ct-box-alias-removed` → `invalid.deprecated.ct`；snippets 正文核对不含 `box<` | E-VS-1-09…10 转绿 | S |
| S5 | 语料与防漂移门禁 | `test/surface.json`（四组构造清单）+ `test/check-surface.py`（复用 `check-grammar` 的 `resolve/scan`）；`npm test` 串联三脚本；G-5/G-6 锁测 | E-VS-1-11…14、17…18；门禁演练按 E-VS-1-13 | M |
| S6 | 收口 | README（目标 1.1.0、构造表补 1.1 三行）、`.vscodeignore` 加 `docs/**`、CHANGELOG `0.2.0`（顶部加版本线说明：`0.6.x` 为拆分前线，市场线 `0.0.1 → 0.1.0 → 0.2.0`）、`package.json` 版本 `0.2.0` 并 `npm install --package-lock-only` 重生成 lock、打包、**提交 + tag + push** | E-VS-1-15…16；Actions 记录贴入 | M |

**Stage 顺序约束**：S0 → S1（必须真红）→ S2/S3/S4（可自选顺序，各自转绿）→ S5 → S6。
S2–S4 期间不得修改 S1 已提交的断言（断言变更只能回到 S1 重做并重新贴红）。

### 进度台账

| Stage | 状态 | 证据 |
| --- | --- | --- |
| S0 语料与基线 | 部分（302 + 两份 B5 错误样例已入 fixtures；`p53_*`、`301`、`303` 未取） | `f7c91e2` |
| S1 红 | ✅ 已提交 | `f7c91e2`：`== 196 checks, 5 failed`，退出码 1 |
| S2 match/yield | ✅ 已提交 | `d3a17ad`；当前 `npm test` = 198 检查 / 0 失败 |
| S3 可选链 | 未开始 | — |
| S4 `box` 退场 | 未开始 | — |
| S5 语料 + 防漂移门禁 | 未开始 | — |
| S6 收口（提交/tag/push） | **不满足**：工作区已有版本号/README/CHANGELOG 改动，但 S3–S5 未完成，且这些文档仍写着「0.9.0 再对齐 box」的旧分卡口径 | 工作区 |

## 3 退出判据（二值）

| ID | 断言 |
| --- | --- |
| E-VS-1-01 | `test/ast/302_adt_match_expr` 的 `Pattern => expr` 行命中 `ct-match-arm`，且**不**命中 `ct-closure-arrow` |
| E-VS-1-02 | 302 的 `yield prod + 1;` 行命中 `ct-yield` |
| E-VS-1-03 | 闭包 `(int x) => x + 1` 仍命中 `ct-closure-arrow`，且不命中 `ct-match-arm` |
| E-VS-1-04 | `int yield = 1;`、`goto yield;`、`x.yield` 不命中 `ct-yield` |
| E-VS-1-05 | `yield` / `=>` / `?.` 在字符串、行注释、块注释内均不触发新规则 |
| E-VS-1-06 | `full = m["a"]?.c?.v;` 行命中 `ct-optional-chain` 恰好 2 次 |
| E-VS-1-07 | `m?["k"]` 命中 `ct-optional-chain`；`c?.5 : 1.0` **不**命中 |
| E-VS-1-08 | 语句尾 `g()?;` 仍为 `ct-try`，未被可选链改写 |
| E-VS-1-09 | `Box<Record> h = new Record { … };` 仍命中 `ct-box-type`；`box<Record> r = …` 命中 `invalid.deprecated.ct` 且不命中 `ct-box-type` |
| E-VS-1-10 | 裸 `struct Box { int box; }`、`Box box = { 1 };`、`r.box` 不受 `ct-box-type` / `invalid.deprecated.ct` 影响 |
| E-VS-1-11 | `test/fixtures/README.md` 记录来源 tag `v1.1.0`、commit `aa223cf1`、文件清单与数量，实际文件数与清单一致 |
| E-VS-1-12 | `python3 test/check-surface.py` 退出码 0；清单覆盖四组（顶层构造 / 关键字与修饰 / 控制与表达式 / 类型面），每组 ≥ 5 条，每条都有 fixture 命中 |
| E-VS-1-13 | 门禁演练：临时改错清单里任一规则名 → `check-surface.py` 退出码非 0；演练后 `git diff` 为空 |
| E-VS-1-14 | `npm test` 串联 `check-index` + `check-grammar` + `check-surface`，退出码 0，全部 `0 failed`（原始输出入库） |
| E-VS-1-15 | `npx vsce package` 成功；文件清单不含 `test/**`、`docs/**`、`.github/**`、`package-lock.json`；vsix 大小记录 |
| E-VS-1-16 | **收口三连**：提交（含 `VS-PH-1` 标识）→ annotated tag `v0.2.0` → `git push origin main` 与 `git push origin v0.2.0` 均成功；CI 与 Release 的 run 链接与结论入库。**版本一致性**：`package.json`、`package-lock.json` 根 `version`、README、CHANGELOG 四处均为 `0.2.0`，且 `v0.2.0` 不与已发布版本冲突（0.1.0 已占用） |
| E-VS-1-17 | **G-5 锁测**：`impl Cell {` 头部类型名有 `entity.name.type` scope；`impl Greeter for Person {` 仍命中 `ct-impl` |
| E-VS-1-18 | **多级链不误判**：`doc["user"]["age"]`、`x[k].field` 不命中 `ct-generic-type` / `ct-generic-call` |

## 4 收口流程（S6 固定动作，按序执行）

1. `npm test` 全绿 → 贴原始输出（三个脚本的汇总行）。
2. `npx vsce package` → 贴文件清单与大小。
3. `git add -A && git commit -m "feat(grammar): VS-PH-1 语法对齐 Ct 1.1.0（match/yield、可选链、box 退场、语料门禁）"`
4. `git tag -a v0.2.0 -m "ct-vscode 0.2.0 — grammar aligned with Ct 1.1.0"`
5. `git push origin main && git push origin v0.2.0`
6. 贴两条 Actions 结果：`CI`（push）与 `Release`（tag）。
7. 若 `Release` 在 publish 步骤失败：修凭据（`VSCE_PAT` / OIDC 策略）后 `gh run rerun <id>`；
   **不删除 tag、不强推、不改写历史**。

## 5 风险与回滚

| # | 风险 | 处置 |
| --- | --- | --- |
| R-VS-1-1 | **行式近似**：`yield` 在臂外（非法代码）也会被着色 | README「已知近似」写明以行首判定，不做块作用域推断 |
| R-VS-1-2 | `ct-match-arm` 抢走闭包 `=>` | 规则限定「模式 + 箭头」形状；E-VS-1-03 锁死 |
| R-VS-1-3 | 规则顺序错（match-arm / optional-chain 相对 closure-arrow / ct-try） | 顺序写死在 grammar 并在 `scan order` 输出核对；E-VS-1-01、E-VS-1-08 锁 |
| R-VS-1-4 | 可选链误吃三目 `c?.5` | 规则要求 `.` 后非数字；E-VS-1-07 锁 |
| R-VS-1-5 | 按 tag 重取 fixtures 导致既有断言文本/行号变化 | 逐文件 `diff` 记录；断言按内容与子串匹配，不绑行号 |
| R-VS-1-6 | **tag 触发发布但凭据未配** → Release 红 | 打 tag 前过「发布凭据」闸；失败只 rerun，不删 tag |

回滚：语法、测试与门禁、文档三笔独立提交，可分别 revert；`v0.2.0` 版本号与 tag 若已推送则不删，
以新 PATCH（0.7.1）修正。

## 6 关联

- 规范：`ct-lang` `docs/language-spec.md` §3（行 231–257）、§3.1（行 259–281）、§4.65（行 2961）、§4.71（行 3183）、§4.73（行 3249–3460）
- 样例：`ct-lang` `test/ast/302_adt_match_expr`、`errors/l29b5_yield_outside.ct`、`errors/l29b5_multi_yield.ct`、`test/ast/p53_{chain,ptr_field,field_ptr,map_ptr_sub,ptr_sub,ternary_dot5}`、`test/ast/300_adt_payload_glue`、`301_adt_methods`、`303_map_binding`
- 上游卡：`ct-lang` `docs/phases/v1-PH-1/card.md`（S2b / `E-V2-4`、S4 / `E-V2-7`）
- 本仓：[roadmap](../../roadmap.md)
