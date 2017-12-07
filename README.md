# Install dependencies
## pyqt4
### mac os
```
brew install cartr/qt4/pyqt

sudo mkdir -p /Users/username/Library/Python/2.7/lib/python/site-packages

sudo vim /Users/username/Library/Python/2.7/lib/python/site-packages/homebrew.pth
import site; site.addsitedir("/usr/local/lib/python2.7/site-packages")
```
### ubuntu
```
sudo apt-get install python-qt4
```
### centos
```
sudo yum install PyQt4
```

# install yt_ovs
```
git clone https://github.com/cao19881125/YtOvs.git
cd YtOvs
pip install .
```

# run yt_ovs
```
yt-ovs
```
