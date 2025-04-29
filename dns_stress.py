import asyncio
import random
import aiodns

resolver = aiodns.DNSResolver()

# Load a list of real domains
with open('domains.txt', 'r') as f:
    domain_list = [line.strip() for line in f if line.strip()]

async def query_dns(domain):
    try:
        await resolver.query(domain, 'A')
    except Exception as e:
        print(f"A lookup failed for {domain}: {e}")

    try:
        await resolver.query(domain, 'AAAA')
    except Exception as e:
        print(f"AAAA lookup failed for {domain}: {e}")

async def worker(queue):
    while True:
        domain = await queue.get()
        await query_dns(domain)
        queue.task_done()

async def main():
    queue = asyncio.Queue()

    # Launch workers
    num_workers = 500  # You can tune this if needed
    for _ in range(num_workers):
        asyncio.create_task(worker(queue))

    while True:
        start = asyncio.get_event_loop().time()

        # Pick 2500 random domains each second
        domains = random.sample(domain_list, 2500)

        for domain in domains:
            await queue.put(domain)

        elapsed = asyncio.get_event_loop().time() - start
        sleep_time = max(0, 1 - elapsed)
        await asyncio.sleep(sleep_time)

if __name__ == "__main__":
    asyncio.run(main())
