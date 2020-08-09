ref: https://segmentfault.com/a/1190000017123921  
https://blog.csdn.net/north1989/article/details/53471439

最基本操作
```
# 1. 先从github创建一个空的仓库

# 2. init repo
git init
git add .
git commit -m "Initial commit"

# 3. add remote repo
git remote add origin + repo address 
git pull origin master --allow-unrelated-histories
git -u push origin master

# 只改一个文件
git add README.md
git commit -m "update readme"
```

换远程仓库
```
# http://yijiebuyi.com/blog/9c00641126e41779ef38cafb9c6aad67.html
# 如何把 clone 后修改的代码提交到 github 
# - u 的作用，第一次的时候用就好了

# 1. 删除远程仓库
git remote remove 远程库名(删除该远程库) 
git remote remove origin(一般都是叫origin)

# 2. 添加新仓库
git remote add 远程库名 远程库地址(添加另外远程库)
git remote add origion https://。。。。。

# 或者一步到位
git remote rename 旧名称 新名称（改变远程库的名字）
git rename origin origin1(把origin改成origin1)
```

branch 的用法
```
# 只切换分支
git checkout [branch name]

# 创建新分支并切换到新分支
git checkout -b [new branch name]

# 显示所有分支（本地）
git branch
# 显示所有分支（本地+远程）
git branch -a 

# 删除分支
git branch -d [branch name]
# 删除远程分支
git push origin --delete [remote branch name]

# push 到分支
# 第一次push，需要在remote仓库建立分支
git push --set-upstream origin [new branch name]
# 第二次push
不知道

# clone指定分支的代码
git clone -b [branch name] [url]

# 本地分支改名
git branch -m [oldName] [newName]

# 远程分支改名
## a. 重命名远程分支对应的本地分支
git branch -m [oldName] [newName]

## b. 删除远程分支
git push --delete origin [oldName]

## c. 上传新命名的本地分支
git push origin [newName]

## d.把修改后的本地分支与远程分支关联
git branch --set-upstream-to origin/[newBranchName]
```

远程仓库的使用
```
# ref: https://git-scm.com/book/zh/v1/Git-%E5%9F%BA%E7%A1%80-%E8%BF%9C%E7%A8%8B%E4%BB%93%E5%BA%93%E7%9A%84%E4%BD%BF%E7%94%A8

# 查看远程仓库
git remote

# 查看完整远程仓库信息
git remote -v 或者 git remote --verbose
```

Fork后同步主仓库最新代码
```
# check remote repos
git remote -v

# set upstream to the main repo
# while the origin is still our own forked repo
# it will now have origin as remote, and upstream as the father of origin
git set upstream http://xxxxxxxxx
```
