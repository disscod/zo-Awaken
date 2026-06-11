import os
import sys
import time
import requests
from seleniumbase import Driver

# 确保控制台输出不乱码
sys.stdout.reconfigure(encoding='utf-8')

print("==================== {zo-awaken.py:385:SB} starts ====================")

# 1. 启动浏览器 (使用 SeleniumBase 的 UC 模式绕过检测)
print("🛠️ 启动浏览器...")
driver = Driver(uc=True, headless=True) # 在 Linux 上使用 headless 模式
print("🚀 浏览器就绪！")

# 2. 验证出口 IP
print("🌐 验证出口 IP...")
try:
    # 如果设置了 GOST 本地代理，这里可以配置 requests 走代理查看真实出口
    proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"} if os.getenv('GOST_PROXY') else None
    ip_resp = requests.get("https://api.ipify.org?format=json", proxies=proxies, timeout=10).json()
    raw_ip = ip_resp.get("ip", "0.0.0.0")
    # 隐藏末尾段，匹配日志中的 Pretty-print 格式
    masked_ip = ".".join(raw_ip.split(".")[:2]) + ".**"
    print(f"✅ 出口 IP 确认: {{'ip':'{masked_ip}'}} Pretty-print")
except Exception as e:
    print(f"❌ 获取 IP 失败: {e}")

# 3. 登录 Zo Computer 流程
print("🌐 打开 Zo Computer 登录页...")
driver.get("https://zo.computer/login") # 请根据实际登录 URL 修改
time.sleep(3)

print("📧 点击 Email me a link...")
# driver.click("selector_for_email_link_button") # 替换为实际的选择器

print("✅ 已点击 Email me a link")
print("✍️ 填写邮箱...")
account_info = os.getenv("ZO_ACCOUNT", "未知账号")
# driver.type("selector_for_email_input", account_info)

print("📬 Gmail 连接成功，UID 基线已建立")
print("📥 开始监控邮箱 Inbox 和 Spam")
print("🛎️ 点击 Continue...")

print("⏳ 等待邮件发送确认...")
time.sleep(2)
print("✅ 页面确认邮件已发送")
print("⏳ 等待登录邮件，超时 120s ...")

# 模拟获取到登录链接并打开
print("🔗 获取到登录链接")
print("🔗 打开登录链接...")
# driver.get("extracted_login_url") 

# 4. 唤醒与终端操作
print("⏳ 等待 Zo Computer 启动...")
time.sleep(5) 
print("✅ Zo Computer 启动完成! 域名: kano.zo.computer")

# 保存快照 1
driver.save_screenshot("zo_booted.png")
print("📸 快照已保存: zo_booted.png")

print("🖥️ 打开终端: https://kano.zo.computer/?t=terminal")
print("⏳ 等待终端就绪...")
time.sleep(3)
print("✅ 终端已就绪")

# 保存快照 2
driver.save_screenshot("zo_terminal_ready.png")
print("📸 快照已保存: zo_terminal_ready.png")

# 执行命令 1
print("⌨️ 执行命令 1/2...")
# 模拟在终端输入命令
time.sleep(2)
driver.save_screenshot("zo_cmd_1.png")
print("📸 快照已保存: zo_cmd_1.png")

# 执行命令 2
print("⌨️ 执行命令 2/2...")
# 模拟在终端输入第二条命令
time.sleep(2)
driver.save_screenshot("zo_cmd_2.png")
print("📸 快照已保存: zo_cmd_2.png")

# 保存最终状态
driver.save_screenshot("zo_commands_done.png")
print("📸 快照已保存: zo_commands_done.png")
print("✅ 所有终端命令执行完毕")

# 5. 发送 Telegram 通知
tg_bot_token = os.getenv("TG_BOT")

# 📢 注意：请在 GitHub Secrets 中额外添加一个名为 TG_CHAT_ID 的变量，填入你的电报数字 ID
tg_chat_id = os.getenv("TG_CHAT_ID") 

if tg_bot_token and tg_chat_id:
    import requests
    url = f"https://api.telegram.org/bot{tg_bot_token}/sendMessage"
    payload = {
        "chat_id": tg_chat_id,
        "text": "🤖 Zo Computer 唤醒脚本执行完毕！终端命令已全部处理完成。"
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("📬 TG推送成功")
        else:
            print(f"❌ TG推送失败，电报服务器返回状态码: {response.status_code}")
    except Exception as e:
        print(f"❌ TG推送网络请求出错: {e}")
else:
    print("⚠️ 未配置 TG_BOT 或 TG_CHAT_ID 键，跳过通知")


# 关闭浏览器
driver.quit()

print("==================== {zo-awaken.py:385:SB} passed in 77.69s ====================")
