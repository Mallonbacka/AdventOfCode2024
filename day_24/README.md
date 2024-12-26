# Day 24

In part 2 I wrote no new code. I recognized the "full adder" logic, and was able to find the "broken" parts with carefully crafted searches in my text editor. For example, if a gate writes to an output bit (except the last), it must be an `XOR` gate, so I could write a regular expression for lines which contain something other than `XOR` and `-> z` to quickly spot the incorrect gates. Then, I could trace the inputs from the corresponding input bits to find the gate that needs swapping with the incorrect gate.

I wrote code to test adding two numbers, then kept tweaking the `input.txt` file until it worked reliably, while keeping the list is swapped gates on scratch paper. I didn't think too much about how I might have approached this if I were only allowed to write code.
