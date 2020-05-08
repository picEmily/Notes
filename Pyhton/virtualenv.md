# virtualenv
## in Linux
```bash
sudo apt-get install python-pip
pip install virtualenv
virtualenv --version
sudo apt install virtualenv(似乎不需要)
virtualenv -p python3 venv
source venv/bin/activate
(venv)
deactivate

virtualenv -python=python3 venv
```

## in win
```bash
pip install virtualenv
virtualenv venv     \\ in the div I want 
venv\Scripts\activate
(venv) pip3 install -r requirements.txt
deactivate
```

# conda
更强大
https://www.jianshu.com/p/7ebe1df808ba
```
# 创建一个名为test的虚拟环境
conda create -n test

# 创建指定版本的虚拟环境，即便是conda3也可以创建2.x的，反之亦然
conda create -n test python=2.7

# 完整复制某个环境
conda create -n test2 -clone test

# 进入虚拟环境
source activate test

# 退出虚拟环境
source deactivate

# list all venv
conda env list

# list all pkg in a venv 
conda list -n test

# remove
conda env remove --name test
```

```杂七杂八
conda install -c xanderhsia zsh 
conda install -c trent vim
conda install -c r r-base
conda install -c r rstudio
conda install -c anaconda mysql
conda install -c anaconda mongodb
```
cheat sheet 
https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf

conda 换源
临时
```
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -U [pkg name]
```
```
# 换源
conda config --add channels 'https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/'
conda config --set show_channel_urls yes

# 删除添加的源呢？
conda config --remove channels 'https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/' 

# 看看当前的 cofig 是什么样的
conda config --show
```
可用源
```
# 清华
https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/

# 中科大
http://mirrors.ustc.edu.cn/anaconda/pkgs/free/
```

conda install 和 pip install区别
https://blog.csdn.net/persistinlife/article/details/89298094

安装cuda和换源(-c)
https://blog.csdn.net/kaixinjiuxing666/article/details/80321124
https://medium.com/@_willfalcon/how-to-install-pytorch-1-0-with-cuda-10-0-169569c5b82d
```
# 换源(或者用-c)
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/
conda config --set show_channel_urls yes

# 安装
conda install -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/ pytorch
conda install -c fragcolor cuda10.0
```



启动worker的方法:  
    
```python
run_redis_workers_forever(ManagedBertModel, 64, prefix='channel_1')
run_redis_workers_forever(ManagedBertModel, 64, prefix='channel_2')
```

接下来定义在另一个文件中streamer并得到模型结果:  
    
```python
streamer_1 = RedisStreaemr(prefix='channel_1')
streamer_2 = RedisStreaemr(prefix='channel_1')

# predict
output_1 = streamer_1.predict(batch)
output_2 = streamer_1.predict(batch)
```
