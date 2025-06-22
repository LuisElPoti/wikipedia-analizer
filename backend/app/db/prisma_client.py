from prisma import Prisma

prisma = Prisma()

async def connect_prisma():
    await prisma.connect()

async def disconnect_prisma():
    await prisma.disconnect()
