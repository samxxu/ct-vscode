# 语法样例（fixtures）

本目录是高亮语料的**唯一来源**：`test/check-grammar.py` 的 `CT_CASES` 与
`test/check-surface.py` 的语法面清单都按这里的相对路径读取，测试不访问本仓之外的任何文件。

| 项 | 值 |
| --- | --- |
| 上游仓库 | `ct-lang`（<https://github.com/samxxu/ct-lang>） |
| 来源 tag | **`v1.1.0`** |
| 来源 commit | `aa223cf18e3ac143d066330569e537b8899ebbea` |
| 取回日期 | 2026-11-27 |
| 文件数 | **54** |

## 取回方式

```bash
# 在 ct-lang 仓里按 tag 取文件，逐份覆盖本目录
git -C ../ct-lang checkout v1.1.0
for f in $(cd test/fixtures && find . -type f | sed 's|^\./||'); do
  mkdir -p "test/fixtures/$(dirname "$f")"
  git -C ../ct-lang show "v1.1.0:$f" > "test/fixtures/$f"
done
```

目录结构沿用上游（`examples/…`、`test/ast/…`、`test/cases/…`、`test/modules/…`），
所以 `check-grammar.py` 里的路径与上游样例一一对应。每次按 tag 重取后，用
`diff <(git -C ../ct-lang show v1.1.0:<相对路径>) <本目录文件>` 逐份核对，
R-VS-1-5 要求把差异记录在对应提交里。

## 文件清单（54 份）

- `examples/01_greeter/greeter.ct`
- `examples/02_market/market.ct`
- `examples/21_generic_bound/generic_bound.ct`
- `examples/22_foreach_map/foreach_map.ct`
- `examples/23_generic_stack/generic_stack.ct`
- `examples/24_vec_ops/vec_ops.ct`
- `examples/26_range_vec/range_vec.ct`
- `examples/29_into_block/into.ct`
- `test/archive/cases/19_namespace.ct`
- `test/archive/cases/22_drop.ct`
- `test/archive/import/app.ct`
- `test/archive/multifile/calc.ct`
- `test/ast/100_loop_contextual_label/prog.ct`
- `test/ast/102_loop_range_basic/prog.ct`
- `test/ast/109_range_init_basic/prog.ct`
- `test/ast/123_generic_identity/prog.ct`
- `test/ast/124_generic_struct/prog.ct`
- `test/ast/125_generic_type_positions/prog.ct`
- `test/ast/128_generic_type_operands/prog.ct`
- `test/ast/138_generic_struct/prog.ct`
- `test/ast/13_map_instance/prog.ct`
- `test/ast/147_generic_impl/prog.ct`
- `test/ast/231_str_ops/prog.ct`
- `test/ast/236_result_try_defer/prog.ct`
- `test/ast/301_adt_methods/prog.ct`
- `test/ast/302_adt_match_expr/prog.ct`
- `test/ast/303_map_binding/prog.ct`
- `test/ast/42_static_assert/prog.ct`
- `test/ast/53_c11_align_generic/prog.ct`
- `test/ast/55_c_compat/prog.ct`
- `test/ast/56_header_compat/prog.ct`
- `test/ast/57_trait_default/prog.ct`
- `test/ast/62_borrow_handback/prog.ct`
- `test/ast/65_raw/prog.ct`
- `test/ast/67_type_alias/lib/lib.m.ct`
- `test/ast/70_closure_basic/prog.ct`
- `test/ast/errors/l29b5_multi_yield.ct`
- `test/ast/errors/l29b5_yield_outside.ct`
- `test/ast/p53_chain/prog.ct`
- `test/ast/p53_field_ptr/prog.ct`
- `test/ast/p53_map_ptr_sub/prog.ct`
- `test/ast/p53_ptr_field/prog.ct`
- `test/ast/p53_ptr_sub/prog.ct`
- `test/ast/p53_ternary_dot5/prog.ct`
- `test/ast/p80_retain/borrow_out_ref.ct`
- `test/ast/p81_box/layout.ct`
- `test/cases/02_multi_trait.ct`
- `test/cases/06_name_collision.ct`
- `test/modules/alias/src/main.ct`
- `test/modules/autodrop/prog.ct`
- `test/modules/map_ns/hal/uart.h.ct`
- `test/modules/map_unit/libc/libc.m.ct`
- `test/modules/map_unit/main.ct`
- `test/modules/map_unit_type/ctypes/ctypes.m.ct`

## 说明

- `test/ast/errors/` 下的两份是上游**负例**（`yield` 在臂外、一个臂两个
  `yield`）。语法高亮不做语义判定，保留它们是为了锁定 R-VS-1-1 的行式近似：
  语句行首的 `yield` 一律着色。
- `236_result_try_defer`、`231_str_ops`、`p80_retain/borrow_out_ref.ct`、
  `p81_box/layout.ct` 是 `check-surface.py`「语法面清单」所需的样例，覆盖
  `defer` / `errdefer` / `err:` / 后缀 `?`、`String` / `Str`、`ref` / `out` / `T[]`、
  `Box<T>` / `new`，与其余文件同取自上表 tag。
- 新增样例只允许来自**已发布 tag**；`ct-lang` `main` 上未发布的内容
  （304–307 模式、§4.77 函子糖）不进语料。
