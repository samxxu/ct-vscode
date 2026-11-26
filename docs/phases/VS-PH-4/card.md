---
phase-id: VS-PH-4
extension-minor: 10
---

# VS-PH-4 — 1.1.0 语料刷新与语法面清单门禁

> **状态：待开始**。目标扩展版本 `0.10.0`。
> **前置**：`VS-PH-1`、`VS-PH-2`、`VS-PH-3` 全部收口（本卡是路线收口卡）。
> **上游依据**：`ct-lang` `v1.1.0`（`aa223cf1`）；spec §3 / §3.1（构造总览）；
> 样例 `test/ast/300_adt_payload_glue`、`301_adt_methods`、`303_map_binding`。

## 0 卡片字段（冻结）

| 项 | 值 |
| --- | --- |
| 编号 | `VS-PH-4`（扩展 `MINOR = 10` ↔ `0.10.0`） |
| 目标 | 把测试语料锁定到 **Ct 1.1.0**，并加一道「语法面清单」门禁：任何 CT 独有构造缺规则、规则被改名/删除，`npm test` 直接红，防止再次漂移 |
| 范围 | fixtures 按 `v1.1.0` 全量重取 + 来源登记；新增 `test/surface.json` 与 `test/check-surface.py`；`npm test` 串联；README 目标版本与构造表；CHANGELOG `0.10.0` |
| 非目标 | 新增语法（本卡只锁已有面）；`indexer.js` / `extension.js`；发布渠道；1.2 未发布特性（304–307 模式、§4.77 函子糖） |
| 交付物 | `test/fixtures/**` 重取、`test/fixtures/README.md`、`test/surface.json`、`test/check-surface.py`、`package.json` scripts、README/CHANGELOG、`0.10.0` 打包 |
| 任务清单 | §2（S1 红 / S2 实现 / S3 收口） |
| 退出判据 | `E-VS-4-1 … E-VS-4-8`（§3） |
| version-minor | 10 |
| 已知风险 | `R-VS-4-1 … R-VS-4-3`（§4） |

## 1 入口与闸

| 闸 | 内容 | 现状 |
| --- | --- | --- |
| 前置 | VS-PH-1/2/3 收口，`npm test` 全绿 | 待满足 |
| 上游 | `v1.1.0` = `aa223cf1`；`test/ast/300/301/302/303` 在该 tag 存在（302 已在 VS-PH-1 引入） | 已核对 |
| 语料来源 | 现有 fixtures 取自 `ct-lang` 工作区（未登记版本），需按 tag 重取 | 已核对 |
| 门禁基线 | `npm test` = `node test/check-index.js && python3 test/check-grammar.py` | 已核对 |

## 2 任务

| 任务 | 交付 | 验收 | effort |
| --- | --- | --- | --- |
| S1 红 | 新增 `test/surface.json`（构造 → 规则名 → fixture → 行选择器）与 `test/check-surface.py`；把 `npm test` 改成串联三脚本。清单先只覆盖已实现规则，另加 3 条**尚未实现**的条目（若还有缺口）或故意写错的规则名 | `python3 test/check-surface.py` **失败**（缺规则/缺 fixture），退出码 1；原始输出入库 | M |
| S2 实现 | 按 `v1.1.0` 全量重取 fixtures（`rsync --files-from` 同现有清单 + `300_adt_payload_glue`、`301_adt_methods`、`303_map_binding`），写 `test/fixtures/README.md` 登记 tag/commit/文件数；`check-surface.py` 用 `importlib` 复用 `check-grammar.py` 的 `resolve/scan`，逐条断言「规则存在 + fixture 命中」 | 清单全绿；`check-grammar.py` 既有断言 0 失败 | M |
| S3 收口 | README：目标版本改 **1.1.0**、补 1.1 新增构造（表达式 match/yield、可选链、`box` 硬错）、保留独立版本线说明；`.vscodeignore` 增加 `docs/**`；CHANGELOG `## 0.10.0`；版本 0.10.0；打包 | `npm test` 0 failed；vsix 成功、大小记录、包内无 `test/**` 与 `docs/**` | M |

### 清单条目（`test/surface.json` 的最小覆盖）

| 分组 | 必含条目 |
| --- | --- |
| 顶层构造 | `trait` / `use` / `impl … for` / 固有 `impl N` / `import` / `namespace` / `pub` / `type` 别名 / 泛型声明、调用、struct、impl / `map`（instance / type / namespace）/ recipe |
| 关键字与修饰 | `self` / `own` / `borrow` / `delete` / `defer` / `errdefer` / `err:` / `pub` |
| 控制与表达式 | `loop` / `..` range / `foreach` / `into`（块与内联）/ 闭包 `=>` / match 臂 `=>` / `yield` / 可选链 `?.` `?[` / 后缀 `?` / `$` 与 `$name` |
| 类型面 | `Box<T>` / `String` / `Str` / 切片 `T[]` / ADT 构造与 `match` / C11 关键字 / `__attribute__` / `#ct-raw` |

## 3 退出判据（二值）

| ID | 断言 |
| --- | --- |
| E-VS-4-1 | `test/fixtures/README.md` 记录来源 tag `v1.1.0`、commit `aa223cf1`、文件清单与数量；实际文件数与清单一致 |
| E-VS-4-2 | `python3 test/check-surface.py` 退出码 0；清单覆盖 §2 表格的四个分组，且每组至少 5 条，每条都有 fixture 命中 |
| E-VS-4-3 | 演练：临时把清单里任一规则名改错 → `check-surface.py` 退出码非 0；演练后 `git diff` 为空 |
| E-VS-4-4 | `npm test` 串行执行三个脚本且退出码 0，两端 `0 failed`（原始输出入库） |
| E-VS-4-5 | README「最低 ct 版本」= **1.1.0**，构造表含 1.1 新增三行；独立版本线（扩展 ≠ `CTC_VERSION`）表述保留 |
| E-VS-4-6 | `npx vsce package` 成功；vsix 文件清单不含 `test/**`、`docs/**`、`.github/**`、`package-lock.json`；大小记录 |
| E-VS-4-7 | **G-5 锁测**：`impl Cell {` 头部的类型名有 `entity.name.type` scope；`impl Greeter for Person {` 仍命中 `ct-impl` |
| E-VS-4-8 | **多级链不误判**：`doc["user"]["age"]`、`x[k].field` 不命中 `ct-generic-type` / `ct-generic-call` |

## 4 风险与回滚

| # | 风险 | 处置 |
| --- | --- | --- |
| R-VS-4-1 | 清单膨胀成"全量 token 断言"，维护成本过高 | 只覆盖 spec §3/§3.1 的 **CT 独有构造**，C 透传面不列；条目按分组维护 |
| R-VS-4-2 | 按 tag 重取 fixtures 导致既有断言文本/行号变化 | 逐文件 `diff` 记录；断言按内容与子串匹配，不绑行号 |
| R-VS-4-3 | 演练改坏语法后忘记还原 | 演练用 `git stash` 或临时 worktree，收尾以 `git status` + `git diff` 为空为判据 |

回滚：fixtures 重取、门禁脚本、文档三笔独立提交；`0.10.0` 版本与 tag 单独回滚。

## 5 关联

- 规范：`ct-lang` `docs/language-spec.md` §3（行 231–257）、§3.1（行 259–281）
- 样例：`ct-lang` `test/ast/300_adt_payload_glue`、`301_adt_methods`、`303_map_binding`（302 已在 VS-PH-1 引入）
- 上游卡：`ct-lang` `docs/phases/v1-PH-1/card.md`（S2b / LANG-29）
- 本仓：[roadmap](../../roadmap.md) · [VS-PH-1](../VS-PH-1/card.md) · [VS-PH-2](../VS-PH-2/card.md) · [VS-PH-3](../VS-PH-3/card.md)
