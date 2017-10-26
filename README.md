# install pyqt4
## mac os
```
brew install cartr/qt4/pyqt

sudo mkdir -p /Users/username/Library/Python/2.7/lib/python/site-packages

sudo vim /Users/username/Library/Python/2.7/lib/python/site-packages/homebrew.pth
import site; site.addsitedir("/usr/local/lib/python2.7/site-packages")
```

## test
```
vim test_qt4.py

import sys
from PyQt4 import QtGui

def window():
   app = QtGui.QApplication(sys.argv)
   w = QtGui.QWidget()
   b = QtGui.QLabel(w)
   b.setText('Hello World!')
   w.setGeometry(100,100,200,50)
   b.move(50,20)
   w.setWindowTitle('PyQt')
   w.show()
   sys.exit(app.exec_())

if __name__ == '__main__':
   window()
```

```
python test_qt4.py
```

# run yt_ovs
```
git clone https://github.com/cao19881125/YtOvs.git
cd YtOvs
python yt_ovs.py
```
