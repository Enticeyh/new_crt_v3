import time
import asyncio


class Test:
    a = True

    async def run(self):
        while self.a:
            time.sleep(0.5)
            print("11111111")

    async def stop(self):
        self.a = False
        print('运行停止！')


if __name__ == '__main__':
    test = Test()
    asyncio.run(test.run())
    asyncio.sleep(2)
    asyncio.run(test.stop())

