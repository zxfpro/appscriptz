# 单轮V1.5 回答
import asyncio
from pyppeteer import launch
# TODO 需要优化成无头模式
async def chat_with_kimi(url, user_message,pages=1):
    # 启动浏览器
    browser = await launch(headless=False,
                            userDataDir=f'/Users/zhaoxuefeng/GitHub/test1/userdata{pages}',
                           devtools=False,
                          )  # 设置为 False 可以看到浏览器操作
    page = await browser.newPage()

    # 导航到 Kimi 聊天页面
    await page.goto(url)
    # 等待聊天框加载完成
    await page.waitForSelector('.chat-input')

    await page.type('.chat-input', user_message)
    await page.click('.send-button')
    # 等待提问建议消息框
    xpath_expression2 = '//*[@id="app"]/div/div/div[2]/div/div/div/div[1]/div[2]/div/div[3]/div/div[2]/div[2]'
    await page.waitForXPath(xpath_expression2)
    
    # 这个xpath 获取聊天框汇总的文字 没有思考过程
    xpath_expression = '//*[@id="app"]/div/div/div[2]/div/div/div/div[1]/div[2]/div/div[3]/div/div[2]/div[1]/div[1]/div[2]/div/div'

    elements = await page.xpath(xpath_expression)
    text_contents = []
    for element in elements:
        text_content = await (await element.getProperty('textContent')).jsonValue()
        text_contents.append(text_content)

    response = '\n'.join(text_contents)
    # 关闭浏览器

    await browser.close()
    return response


def kimi_chat(prompt: str, pages:int =1,**kwargs) -> str:
    KIMI_URL = "https://kimi.moonshot.cn/chat"  # 替换为实际的 Kimi 聊天页面 URL
    USER_MESSAGE = prompt

    response = asyncio.get_event_loop().run_until_complete(chat_with_kimi(KIMI_URL, USER_MESSAGE,pages))
    return response
    
if __name__ == "__main__":
    kimi_chat('hello')


