(module
    (func $collatz (param $n i64) (result i64)
       (local i64)
       i64.const 0
       local.set 1                    ;; j = 0   (result)
       (block
           (loop                      ;; label B
               local.get $n           ;; n
               i64.const 1
               i64.eq
               br_if 1                ;; if n == 1: goto A

               local.get $n
               i64.const 2
               i64.rem_u              ;; n % 2
               i32.wrap_i64
               (if                    ;; if n % 2: goto D
                   (then
                       i64.const 3
                       local.get $n
                       i64.mul
                       i64.const 1
                       i64.add
                       local.set $n   ;; n = 3 * n + 1
                  )
                  (else
                       local.get $n
                       i64.const 2
                       i64.div_u
                       local.set $n   ;; n = n / 2
                   )
               )
               local.get 1
               i64.const 1
               i64.add
               local.set 1            ;; j = j + 1
               br 0                   ;; goto B     (continue)
           )
       )                              ;; label A
       local.get 1
    )
    (export "collatz" (func $collatz))
)
