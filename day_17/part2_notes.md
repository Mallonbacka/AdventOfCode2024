# Part B notes

On each iteration, `a` is divided by 8 and truncated to an integer. So if:

- a < 8, the result has one part
- a < 64, the result has two parts
- a < 512, the result has three parts

Our target output has 16 parts, so it happens when a < 8^16, but also when a >= 8^15. This is, however, still 246290604621824 possible values of `a`.

During each loop, the printed value depends on `b` only, but `b` depends on `a` and `c` (which also depends on `a`). `b` is first set to `a mod 8`, so it is only influenced by the smallest three bits of `a`.

