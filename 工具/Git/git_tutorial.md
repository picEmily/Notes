# branch 

创建新分支：

- ``git branch <branch name>; git checkout <branch name>;`` 等价于 ``git checkout -b <branch name>``

- ``git checkout -b <branch name>  <from_branch_name>`` 不写最后一个参数则默认当前提交

``git checkout`` 只是把 HEAD 引用切过去了，而不是 master 引用 

强制修改分支位置

``git branch -f <from_addr> <tp_addr>``

# merge

- 我现在在master，我想把bugFix分支合并进来

``git merge bugFix``

- 现在master会有一个新的提交记录，这个记录的父提交有两个，bugFix和之前的master

``git checkout bugFix``; `` git merge master``

- 同理，现在 bugFix 会有一个新的提交记录，这个记录的父提交有两个，bugFix和之前的master。这个提交正好就是master指向的哪一个。

。所以现在bugFix和master指向同一个提交。

# rebase

- 我现在在bugFix分支上，我想把我的记录嫁接到master上

``git rebase master``

- 这个时候 master 落后一次提交    C0 -> C1 -> ... -> master -> bugFix

``git checkout master``; ``git rebase bugFix``; (如何让提交移到下一个提交)

- 现在 bugFix 和 master 指向同一个提交

# 相对引用

- HEAD 是个引用，指向某条提交。

  ``git log`` 查看的话可以看到很多 SHA 过的号码，这个号是绝对的。但是太难记了，用相对引用即可以用相对关系来定位提交。

- ``HEAD^`` 等价于 ``HEAD~1``

  如果现在我在master，那么 ``master^`` 也等价

# 撤销变更

- ``git reset <commit id / commit reference>`` 回退提交记录

- ``git revert <commit id / commit reference>`` 会记录下来这次回退操作，用于远程



# 整理提交记录

git cherry-pick



合并之前的提交

- 我不想要上次提交了。说简单点就是合并两次提交。

  假设我现在在C4，我觉得C3提交很蠢，想隐藏掉C3，只能看到C4提交

  ``git rebase -i HEAD^^``

- 假设我有20个垃圾提交我都不想要了，指向看到C20提交，C1~C19都不要了

  ``git rebase -i HEAD~10``

- 如果我现在在C3，我又改了代码，还没提交，我不想要C3了

  ``git commit --amend``

> git rebase: **Reapply commits on top of another base tip**  
>
> ``-i`` 是 ``--interactive`` 的简写
>
> 实际上 ``git rebase -i`` 会将之前的提交合并，创建一个新分支实际上 ``git rebase -i`` 会将之前的提交合并，创建一个新分支

# 远程

- **远程分支在本地的时候 origin/master 反映了远程仓库(在你上次和它通信时)的状态**

- 远程分支有一个特别的属性，在你检出时自动进入分离 HEAD 状态。Git 这么做是出于不能直接在这些分支上进行操作的原因, 你必须在别的地方完成你的工作, （更新了远程分支之后）再用远程分享你的工作成果。  所以在本地对origin/master操作没什么意义。

# 从远程仓库获取数据

``git fetch`` 下载master的提交

``git pull`` 相当于 ``git fetch`` + ``fit merge origin/master``



遇到多人合作:

- 先merge 远程代码，才能push

  我从C1拉了代码，然后提交了一次，同时remote也有一次提交

  本地历史 C0 -> C1 -> C3

  远程历史 C0 -> C1 -> C2

  现在无法直接push

- 方法一: git fetch origin master; git rebase origin/master; git push

  方法二: git fetch origin master; git merge origin/master; git push

  方法三: git pull; git push 等价方法二

  方法四: git pull --rebase 等价 方法一

# git log

查看提交历史

https://git-scm.com/book/zh/v1/Git-%E5%9F%BA%E7%A1%80-%E6%9F%A5%E7%9C%8B%E6%8F%90%E4%BA%A4%E5%8E%86%E5%8F%B2

```bash
git log # 基础款
git log -p 或者 git log --patch # 它会显示每次提交所引入的差异
git log --stat # 每次提交的简略信息

# 更好看
git log --pretty=oneline/short/full/fuller
git log --pretty=format:"%h %s" --graph # 常用，有多个人的时候

# 限制输出长度
git log -2　# 只输出2条
git log --since=2.weeks # 输出近两周
git log -S <some text> # 只输出包含此字符串的提交，例如可以写一个函数名
# 例子
git log --pretty="%h - %s" --author='Junio C Hamano' --since="2008-10-01" \
   --before="2008-11-01" --no-merges -- t/
```