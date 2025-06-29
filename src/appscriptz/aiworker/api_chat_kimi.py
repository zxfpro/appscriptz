# 多轮对话
import asyncio
from fastapi import FastAPI, HTTPException
from pyppeteer import launch
from pydantic import BaseModel
from contextlib import asynccontextmanager
import os


# 存储浏览器实例和页面对象
browser = None
page = None

userDataDir = '/Users/zhaoxuefeng/GitHub/test1/userdata'
# userDataDir = "~/Library/Application Support/Google/Chrome"
# 启动浏览器并初始化页面
async def init_browser():
    global browser, page, i
    browser = await launch(headless=False,
                        #    args=['--disable-gpu', '--no-sandbox', '--disable-dev-shm-usage'],
                           userDataDir=userDataDir,
                           executable_path='/Applications/Google Chrome',
                           devtools=False,
                          )
    i = 1                     
    page = await browser.newPage()
    await page.goto('https://kimi.moonshot.cn/chat')
    await page.waitForSelector('.chat-input')


# 编写类似with 的功能
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # 启动时执行的逻辑
        await init_browser()
        if not page:
            raise HTTPException(status_code=500, detail="Failed to initialize browser")
        yield

    finally:
        # 确保浏览器关闭
        if browser:
            await browser.close()

app = FastAPI(lifespan=lifespan)


# 定义请求体模型
class ChatRequest(BaseModel):
    message: str

# 多轮对话 API
@app.post("/chat")
async def chat(request: ChatRequest):
    global page,i
    print('start')
    if not page:
        raise HTTPException(status_code=500, detail="Browser not initialized")
    user_input = request.message.strip()
    if not user_input:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    if user_input.lower() == 'exit':
        raise HTTPException(status_code=400, detail="Conversation ended")
    try:
        # 输入用户消息并发送
        await page.type('.chat-input', user_input)
        await page.evaluate('''() => {
        document.querySelector('.send-button').click();
        }''')
        
        # 等待回复
        x = 1 + 2 * i
        print(x)
        xpath_expression2 = f'//*[@id="app"]/div/div/div[2]/div/div/div/div[1]/div[2]/div/div[{x}]/div/div[2]/div[2]'
        await page.waitForXPath(xpath_expression2, timeout=60000)
        
        # 获取回复内容
        xpath_expression = f'//*[@id="app"]/div/div/div[2]/div/div/div/div[1]/div[2]/div/div[{x}]/div/div[2]/div[1]/div[1]/div[2]/div'
        elements = await page.xpath(xpath_expression)
        text_contents = []
        for element in elements:
            text_content = await (await element.getProperty('textContent')).jsonValue()
            text_contents.append(text_content)
        
        response = '\n'.join(text_contents)
        i +=1
        return {"response": response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8093,loop="asyncio") # loop 是有效果的
# loop="asyncio"