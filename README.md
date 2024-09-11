<img width="1488" alt="图片" src="https://github.com/user-attachments/assets/979c6f10-e52c-4354-9264-f5d4857a23a1">
1.安装依赖  pip install selenium webdriver-manager tqdm

2.在py脚本所在文件夹下，创建targets.txt文件，运行脚本即可。

说明：

感谢夜组安全公众号的转发，因为第一版的效果不是很好。目前正在重构相关的截图逻辑，加入进度条显示。优化截图速度特别是面对资产多的情况。
新版本已上线！！！！，放在Releases，有相关问题提issue

(1)该脚本旨在攻防中，批量的请求url，获取页面截图，以便初步判断脆弱资产。

(2)脚本运行后，会在py文件所在的文件夹下创建screenshots文件夹，并把截图保存到该文件夹下，最后会生成html文档，以便快速筛选可能脆弱的资产

运行截图：

<img width="1488" alt="图片" src="https://github.com/user-attachments/assets/979c6f10-e52c-4354-9264-f5d4857a23a1">

