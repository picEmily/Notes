# Emacs 学习笔记

# 基本快捷键
- C(Ctrl)
- M(Alt/Option)
- S(Win/Command)

**思路**
一般用这些快捷键组合
快捷键组合+命令
函数
命令行



## Document
```
C-h k：查看某个快捷键（组合）的用处或者绑定的函数。
C-h f：查看某个函数的作用，以及它绑定的快捷键。
C-h v：查看某个 Emacs 变量的值。
```

## 打开退出
```
# open
emacas [filename] [filename]  # 打开多个文件
C-X + C-f  # 换文件

# save and quit
C-x + C-s  # 保存
C-x + C-w  # 另存为
C-x + C-c  # 不保存退出

# suspend
C-z
# awake
fg 
```

## Navigating A File
```
Meta-f or Meta-right arrow move to the next word
Meta-b or Meta-back arrow move to the previous word

Ctl-a or Meta-a move to the beginning of the line
Ctl-e or Meta-e move to the end of the line

Meta-g g [NUMBER] jump to a line number. For example, typing Meta-g g 123 would jump to line 123.

Ctl-v page down
Meta-v page up

Meta-< (less-than sign) jump to the start of the file
Meta-> (greater-than sign) jump to the end of the file
```

## Searching
```
Ctl-s searches the file, and prompts you to enter text to search for.

Ctl-s move the cursor to the next search match

Ctl-r move the cursor to the previous search match

Meta-% find and replace text ahead of the current cursor position
```

## Editing Text
```
Click and drag with the mouse to highlight text. (Note: the highlighting text feature will not highlight the text you have chosen until after you have released the mouse).

Ctl-SPACE to put a marker down, and move the cursor to select text

Ctl-w to cut ("kill") the current selection Meta-w to copy the current selection Ctl-y to paste ("yank") whatever is in the copy-paste buffer

Ctl-k cut ("kill") the text on the current line to the right of the cursor

If you hit Ctl-k multiple times in a row (with no other commands between), all the lines will be passed when you hit Ctl-y.

Ctl-d to delete the character under the cursor. Backspace to delete the character before the cursor.

C-k (kill-line)，从光标处起删除该行。
```

## Undo/Redo
```
Ctl-x u undo the last action

Ctl-g cancel (if you're stuck in a command or prompt, pressing this, sometimes several times, should get you out)
```

## copy paste
```
C-w .To cut the text

M-w .To copy the text

C-y .To paste the text
```