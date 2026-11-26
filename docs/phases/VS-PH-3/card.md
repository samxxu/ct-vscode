---
phase-id: VS-PH-3
extension-minor: 9
---

# VS-PH-3 — `box<T>` 退场（1.1 硬错）

> **状态：待开始**。目标扩展版本 `0.9.0`。
> **前置**：无（与 VS-PH-1/2 独立；同一时刻只开一张卡）。
> **上游依据**：`ct-lang` `v1.1.0`（`aa223cf1`），`docs/phases/v1-PH-1/card.md` S4 与 `E-V2-7`：
> `box<T>` 改为硬错并提示 `Box<T>`；spec §4.71「`Box<T>` / `new`」。

## 0 卡片字段（冻结）

| 项 | 值 |
| --- | --- |
| 编号 | `VS-PH-3`（扩展 `MINOR = 9` ↔ `0.9.0`） |
| 目标 | 语法与 1.1 口径一致：`Box<T>` 是唯一拼写；`box<T>` 不再按合法类型着色，改为 `invalid.deprecated.ct` 提示已删别名 |
| 范围 | `ct-box-type` 拆分两条规则；断言反转（既有 `box` 断言先红后绿）；snippets 核对；README/CHANGELOG |
| 非目标 | `Box` 的语义（布局/retain/release）；`new T { … }` 的着色（已由 `ct-new` 覆盖，不改）；其他已冻结拼写（`String`/`Str`/切片/ADT） |
| 交付物 | 语法改动、`test/check-grammar.py` 断言更新、README 与 CHANGELOG、`0.9.0` 打包 |
| 任务清单 | §2（S1 红 / S2 实现 / S3 收口） |
| 退出判据 | `E-VS-3-1 … E-VS-3-6`（§3） |
| version-minor | 9 |
| 已知风险 | `R-VS-3-1 … R-VS-3-2`（§4） |

## 1 入口与闸

| 闸 | 内容 | 现状 |
| --- | --- | --- |
| 上游 | `v1.1.0` S4：删 `box` 别名，硬错提示 `Box<T>` | 已核对 |
| 本仓现状 | `ct-box-type` = `\b(?:Box\|box)\b(?=[ \t]*<)`，`box` 仍按合法类型着色 | 已核对 |
| snippets | 只有 `Box` 前缀（无 `box` 前缀），需逐条核对片段正文不含 `box<` | 已核对前缀，正文待 S3 核对 |
| 使用面 | 0.88–1.0 的旧代码允许 `box<T>`；本卡之后这类代码会被标红，属预期的 1.1 口径变化 | 已裁定 |

## 2 任务

| 任务 | 交付 | 验收 | effort |
| --- | --- | --- | --- |
| S1 红 | 把 `check-grammar.py` 既有 `box<T>` 断言从「仍 -> ct-box-type」改为「-> invalid.deprecated.ct 且不是 ct-box-type」；新增 `Box<…>` 不变断言 | 改后的断言**失败**（当前仍报 ct-box-type），退出码 1；原始输出入库 | S |
| S2 实现 | `ct-box-type` 收窄为 `\bBox\b(?=[ \t]*<)`；新增 `ct-box-alias-removed`：`\bbox\b(?=[ \t]*<)` → `invalid.deprecated.ct`；顺序：新规则在 `ct-box-type` 之前（避免 `Box` 分支干扰） | 断言转绿；`Box<Record>`、`struct Box { int box; }`、`Box box;` 行为不变 | S |
| S3 收口 | snippets 正文核对（无 `box<`）；README 把「`box` 是弃用别名」改成「1.1 起硬错」；CHANGELOG `## 0.9.0`；版本 0.9.0；打包 | `npm test` 0 failed；vsix 成功并记录大小 | S |

## 3 退出判据（二值）

| ID | 断言 |
| --- | --- |
| E-VS-3-1 | `Box<Record> h = new Record { 7, "x" };` 仍命中 `ct-box-type`（不回归） |
| E-VS-3-2 | `box<Record> r = new Record { 7, "x" };` 命中 `invalid.deprecated.ct`，且**不**命中 `ct-box-type` |
| E-VS-3-3 | 裸标识符 `struct Box { int box; }`、`Box box = { 1 };`、`r.box` 不命中 `ct-box-type` / `invalid.deprecated.ct` |
| E-VS-3-4 | `snippets/ct.json` 全文无 `box<`（仅 `Box<`） |
| E-VS-3-5 | README 构造表与「最低 ct 版本」段落的 `box` 措辞已改为「1.1 起硬错」；CHANGELOG 有 `0.9.0` 条目 |
| E-VS-3-6 | `npm test` 退出码 0，两端 `0 failed`；`npx vsce package` 成功并记录大小（原始输出入库） |

## 4 风险与回滚

| # | 风险 | 处置 |
| --- | --- | --- |
| R-VS-3-1 | 旧用户（ct ≤ 1.0）的 `box<T>` 被标红，视觉上是"变差" | 属 1.1 硬错的正确反映；README 注明适用版本，必要时后续提供设置项（不在本卡） |
| R-VS-3-2 | `invalid.deprecated.*` 与某些主题的 `invalid` 叠色不一致 | 只要求 scope 名与断言；若主题表现差，退化为不着色（plain C），在卡内记录一次裁定 |

回滚：语法、断言、文档三笔独立提交；`0.9.0` 版本与 tag 单独回滚。

## 5 关联

- 规范：`ct-lang` `docs/language-spec.md` §4.71（行 3183）
- 上游卡：`ct-lang` `docs/phases/v1-PH-1/card.md`（S4、`E-V2-7`）
- 本仓样例：`test/check-grammar.py` 的 `BOX_ALIAS` / `BOX_BARE` 合成用例
- 本仓：[roadmap](../../roadmap.md) · [VS-PH-1](../VS-PH-1/card.md) · [VS-PH-4](../VS-PH-4/card.md)
