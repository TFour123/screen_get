import os
import re
import time
import random  # 导入 random 用于生成随机数
import concurrent.futures
from tqdm import tqdm  # 导入 tqdm 用于进度条
from queue import PriorityQueue  # 使用优先队列来根据响应时间优先处理
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# 初始化 Chrome 浏览器的设置
chrome_options = Options()
chrome_options.add_argument("--headless")  # 无头模式（不显示浏览器窗口）
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")


# 自动下载 ChromeDriver
def get_driver():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


# 创建一个用于存储截图的文件夹
output_folder = "screenshots"
os.makedirs(output_folder, exist_ok=True)

# 创建 HTML 文件并写入初始内容
html_file = "screenshots_report.html"
with open(html_file, "w", encoding="utf-8") as f:
    f.write("<html><head><title>URL Screenshot Report</title></head><body>\n")
    f.write("<table border='1' cellpadding='10' cellspacing='0' style='border-collapse: collapse;'>\n")
    f.write("<tr><th>URL</th><th>Screenshot</th></tr>\n")  # 添加表格头部


# 使用随机数和时间戳生成唯一文件名
def generate_filename(url):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    random_number = random.randint(1000, 9999)  # 生成 1000 到 9999 的随机数
    file_name = f"screenshot_{random_number}_{timestamp}.png"
    return file_name


# 定义访问和截图的函数，并测量访问时间
def capture_screenshot(url, priority_queue):
    driver = get_driver()  # 每个线程单独初始化一个 driver
    start_time = time.time()
    try:
        driver.get(url)
        print(f"正在访问 {url}...")

        # 生成截图文件的名称
        file_name = generate_filename(url)
        file_path = os.path.join(output_folder, file_name)

        # 截图并保存到指定路径
        driver.save_screenshot(file_path)
        print(f"已保存截图：{file_path}")

        # 截图完成后立即写入 HTML 文件
        with open(html_file, "a", encoding="utf-8") as f:
            f.write(f"<tr><td>{url}</td><td><img src='{file_path}' width='300'></td></tr>\n")

        # 记录完成后的响应时间
        end_time = time.time()
        response_time = end_time - start_time
        priority_queue.put((response_time, url))  # 将 URL 和响应时间放入优先队列

        return (url, file_path)
    finally:
        driver.quit()


# 使用优先队列动态调整优先级
def prioritize_and_process_urls(urls):
    priority_queue = PriorityQueue()

    # 将初始 URL 放入优先队列，初始优先级为 0
    for url in urls:
        priority_queue.put((0, url))

    # 使用多线程加速访问和截图
    max_threads = 10
    with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
        futures = []
        progress = tqdm(total=len(urls), desc="Processing URLs")

        while not priority_queue.empty():
            # 获取优先级最高的 URL（即响应时间最短的）
            priority, url = priority_queue.get()

            # 提交任务并将优先队列传递给 capture_screenshot
            future = executor.submit(capture_screenshot, url, priority_queue)
            futures.append(future)

            # 更新进度条
            progress.update(1)

        # 等待所有任务完成
        concurrent.futures.wait(futures)
        progress.close()


# 从 targets.txt 文件中读取 URL 列表
with open("targets.txt", "r", encoding="utf-8") as f:
    urls = [line.strip() for line in f if line.strip()]  # 去除空行和多余空格

# 优先处理并开始截图
prioritize_and_process_urls(urls)

# 最后关闭 HTML 文件的标签
with open(html_file, "a", encoding="utf-8") as f:
    f.write("</table></body></html>\n")

print(f"报告已生成：{html_file}")
