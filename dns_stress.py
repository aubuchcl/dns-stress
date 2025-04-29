import os
import asyncio
import random
import aiodns

# Read environment variables with defaults
NUM_WORKERS = int(os.getenv("NUM_WORKERS", 5))
DOMAINS_PER_SECOND = int(os.getenv("DOMAINS_PER_SECOND", 25))

# Load domains
with open("domains.txt", "r") as f:
    domain_list = [line.strip() for line in f if line.strip()]

async def query_dns(domain, resolver):
    try:
        result = await resolver.query(domain, 'A')
        if isinstance(result, list):
            for r in result:
                print(f"A record for {domain}: {r.host}")
        else:
            print(f"A record for {domain}: {result.host}")
    except Exception as e:
        print(f"A lookup failed for {domain}: {e}")

    try:
        result = await resolver.query(domain, 'AAAA')
        if isinstance(result, list):
            for r in result:
                print(f"AAAA record for {domain}: {r.host}")
        else:
            print(f"AAAA record for {domain}: {result.host}")
    except Exception as e:
        print(f"AAAA lookup failed for {domain}: {e}")


async def worker(queue, resolver):
    while True:
        domain = await queue.get()
        try:
            await query_dns(domain, resolver)
        finally:
            queue.task_done()

async def main():
    resolver = aiodns.DNSResolver()
    queue = asyncio.Queue()

    # Launch workers
    for _ in range(NUM_WORKERS):
        asyncio.create_task(worker(queue, resolver))

    while True:
        domains = random.sample(domain_list, min(DOMAINS_PER_SECOND, len(domain_list)))
        for domain in domains:
            await queue.put(domain)
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
