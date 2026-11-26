# 路线图 — 语法对齐 Ct 1.1.0

> 中文

本文件只做**简要罗列**：对齐基准、差距清单、阶段卡、门禁与收口规则。卡内细节见
`docs/phases/VS-PH-1/card.md`。扩展的功能逻辑（`indexer.js` / `extension.js`）不在本路线内。

## 1 对齐基准

| 项 | 值 |
| --- | --- |
| 目标语言面 | **Ct 1.1.0**（ct-lang 已发布的最新 tag） |
| 上游锚点 | `ct-lang` tag `v1.1.0`，commit `aa223cf18e3ac143d066330569e537b8899ebbea` |
| 规范入口 | `ct-lang` `docs/language-spec.md` 的 §3 / §3.1（顶层与表达式总览）+ §4.60–§4.76 |
| 本仓当前声明 | 扩展 **0.2.0**，对齐 **Ct 1.1.0 语言面**（README「Requirements」一节） |
| 扩展版本线 | 独立于 `CTC_VERSION`：本路线只产生 **0.2.0** 一个版本。Marketplace 已发布 **0.1.0**（不可复用；gallery API 目前仍只列 0.0.1），`0.6.x` 是拆分前的扩展线、从未上架 |

**上游对齐政策**

1. 基准只认 `ct-lang` **已发布 tag**；不追 `main` 上未发布的内容。
2. `ct-lang` 每发一个 tag：在本文件「§6 对齐记录」追加一行，按 spec 新增/变更的 §
   对照本仓语法，登记差距后再决定是否开卡。
3. `v1.0.0` 不含语法变化（seed 冻结与构建切走，见 `ct-lang` `docs/phases/v1-PH-0/card.md`），
   因此不需要单独开卡。

## 2 差距清单（本仓 v0.6.1 vs Ct 1.1.0）

| ID | 构造 | 上游依据 | 本仓现状 | 落点 |
| --- | --- | --- | --- | --- |
| G-1 | 表达式 `match` 的值臂：`Pattern => expr`、`Pattern => { …; yield expr; }` | spec §4.73（行 3290–3297）；`test/ast/302_adt_match_expr/prog.ct` | `match` 关键字有 `ct-adt-match`，但臂箭头落到 `ct-closure-arrow`，没有臂作用域 | VS-PH-1 / S2 |
| G-2 | `yield`（表达式 match 臂的唯一正常出口，**上下文关键字**） | 同上（spec 行 3295–3297） | 语法里完全没有 `yield` 规则 | VS-PH-1 / S2 |
| G-3 | 可选链 `p?.f` / `p?[i]`（Phase 53） | spec §4.65（行 2961）；`test/ast/p53_*/prog.ct` | 完全缺失；`?` 只有语句尾的 `ct-try` | VS-PH-1 / S3 |
| G-4 | `box<T>` 在 1.1 是**硬错**，唯一拼写 `Box<T>` | `v1-PH-1` S4 / `E-V2-7` | `ct-box-type` 仍写 `\b(?:Box\|box)\b`，把已删别名当合法 | VS-PH-1 / S4 |
| G-5 | 固有 `impl N { … }`（ADT 枚举、非泛型 struct） | spec §4.51 / §4.73 B2；`test/ast/301_adt_methods` | 头部被 `ct-impl-open` 兜住（类型名有 scope），但无专属规则、无锁测 | VS-PH-1 / S5（只锁测） |
| G-6 | 语料与版本声明停在 0.88 | — | `test/fixtures/` 只覆盖到 0.88；README 写「ct 0.88.0 或更新」 | VS-PH-1 / S0 + S5 |

结论：**语法缺口集中在 G-1…G-4**；G-5 是「已覆盖但不稳」，G-6 是语料与声明落后。
全部并入同一张卡，卡内按 stage 串行推进，全卡收口后一次提交、打 tag、推送。

## 3 阶段总览

| 卡 | 主题 | 目标扩展版本 | 状态 |
| --- | --- | --- | --- |
| [VS-PH-1](phases/VS-PH-1/card.md) | 语法对齐 Ct 1.1.0（S0 语料 → S1 红 → S2 match/yield → S3 可选链 → S4 `box` → S5 门禁 → S6 收口） | 0.2.0 | ✅ **完成**：tag `v0.2.0` 已推送，Release [45909160446](https://github.com/samxxu/ct-vscode/actions/runs/45909160446) 以 OIDC 发布成功（`Published samxxu.ct-vscode v0.2.0.`） |

**推进规则**

- **一卡一收口**：本路线只开这一张卡，卡内 stage 串行；全部 stage 绿后才做收口动作。
- 决策与口径集中在卡片的 §1「入口与闸」（版本线、发布凭据、行式近似等），本文件只记阶段、差距与门禁。
- 卡内先红后绿：S1 一次性写出全部新断言，先看到**真实失败**（贴原始输出与退出码）；
  随后 S2–S4 分批把它们转绿。无法生成真红时必须登记 `no-test: <理由>`，**禁止假红**。
- 功能逻辑（`indexer.js` / `extension.js`）不动；测试暴露的迁出遗留路径问题单独登记。
- 收口固定动作见卡片 §4：**CI 切 OIDC → 提交 → 打 annotated tag `v0.2.0` → 推送 main 与 tag**；
  剩余工作逐项列在卡片 §6「执笔人交接清单」。

## 4 卡内门禁

| 门禁 | 命令 | 判据 |
| --- | --- | --- |
| 语法与索引测试 | `npm test`（`check-index` + `check-grammar` + `check-surface`） | 退出码 0，全部 `0 failed` |
| 打包 | `npx vsce package` | 成功，记录 vsix 文件大小 |
| 依赖 | `npm ls --omit=dev` | 无运行时依赖 |
| 包内容 | vsce 输出文件清单 | 不含 `test/**`、`docs/**`、`.github/**`、`package-lock.json` |
| 发布闸 | 推送 `v*` tag | 会触发 `Release` 工作流；发布走 **Trusted Publishing（OIDC）**，无需 PAT；publisher 策略已建好（卡片 §4 第 0 步），2026-11-27 Release 成功（run `45909160446`） |
| 文档 | 人工核对 | README 目标版本与构造表、CHANGELOG `0.2.0` 与实现一致 |

## 5 非目标（本路线明确不做）

- ct-lang `main` 上未发布的内容：`test/ast/304…307`（字面量/嵌套/struct/或模式、守卫）、
  spec §4.77 函子签名糖 `(A, B) => R`、v1.2 Typed/Lowered IR。
- 语义级校验（`yield` 唯一出口、`box` 硬错、模式穷尽）：这些是编译器职责，扩展只做着色。
- `indexer.js` 的跳转能力扩展（不因 1.1 语法新增跳转规则）。
- 发布渠道与账号迁移（另议）。

## 6 对齐记录

| 日期 | 上游 | 结论 |
| --- | --- | --- |
| 2026-11-27 | `v1.1.0`（aa223cf1） | 首次对齐评估：G-1…G-4 需实现，G-5 锁测，G-6 语料/声明补齐；合并为单卡 VS-PH-1（0.2.0）；`v1.0.0` 无语法变化 |

## 7 后续（1.2 观察项）

`ct-lang` 发布下一个 tag 时按 §1 政策重评；候选：完整模式匹配语法（304–307）、
函子签名糖、以及 1.1 冻结档位里 `String`/`Str`/切片/`ref-out`/ADT/`Box` 的拼写变化。
