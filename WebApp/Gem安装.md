# 安装Gem
```
wget https://rubygems.org/rubygems/rubygems-2.6.12.zip

unzip rubygems-2.6.12.zip

cd rubygems-2.6.12/

sudo apt-get install ruby-full

sudo ruby setup.rb

# gem -v 查看版本
```

# 安装bundle
```
sudo gem install bundler
```

修改./Gemfile
```
source 'https://gems.ruby-china.com/'
```
```
bundle install
```

bundle config build.nokogiri -v '1.6.2.1' \
--with-iconv-lib=/usr/local/lib \
--with-iconv-include=/usr/local/include