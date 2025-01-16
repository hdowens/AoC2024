## Notes from today


A 
B
C

Program 0,3,5,4,3,0

0,3
5,4
3,0

do 
    a = a >> 3
    out(a % 8)
while a >= 0

117440
a = a >> 3
a = 14860
out(14680 % 8)
-> 0
a = a >> 3
1835
-> 3
a = a >> 3
a = 229
-> 5

0, 3, 5 (can see this is the output)

where to go from here
- - -
2,4, # bst with a
1,1, # bxl with 1
7,5, # c divide with b
1,5, # bxl with 5
0,3, # adv left shift a by 3
4,3, # bxc bitwise or b with c
5,5, # out b mod 8
3,0  # jnz back to 0 if a not empty


b = a % 8
b = b ^ 1
c = a >> b
b = b ^ 5
a = a >> 3
b = b ^ c
out(b % 8)
if a != 0: jump to 0

we need to output 0, working backwards. This means a needs to be somewhere between 0 and 7. We can test all values betweenn, in my program it is 4. 

After this, because we are right shifting by 3 after, effectively dividing by 8, when reverse engeineering we need to left shift by 3, effectively multiplying by 8. So we now have our a at 4*8=32. We then can start adding values from 0-7 back into it and we get 5 to produce the sequence 3,0.

Just keep going from there until we get the answer