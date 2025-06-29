import random
import time

class StorageSystem:
    def __init__(self, cache_size=4, memory_size=16, disk_size=100):
        """初始化存储系统"""
        self.cache_size = cache_size  # 缓存大小（块数）
        self.memory_size = memory_size  # 内存大小（块数）
        self.disk_size = disk_size  # 硬盘大小（块数）
        
        # 初始化存储内容
        self.cache = {}  # 缓存：存储数据和访问时间
        self.memory = {}  # 内存：存储数据和访问时间
        self.disk = {i: f"Data_{i}" for i in range(disk_size)}  # 硬盘：存储所有数据
        
        # 统计命中率
        self.cache_hits = 0
        self.memory_hits = 0
        self.disk_accesses = 0
        self.total_accesses = 0

    def access_data(self, address):
        """访问指定地址的数据"""
        self.total_accesses += 1
        
        # 检查缓存
        if address in self.cache:
            self.cache_hits += 1
            self.cache[address]['time'] = time.time()  # 更新访问时间
            print(f"缓存命中: 地址 {address} 数据 {self.cache[address]['data']}")
            return self.cache[address]['data']
        
        # 检查内存
        if address in self.memory:
            self.memory_hits += 1
            print(f"内存命中: 地址 {address} 数据 {self.memory[address]['data']}")
            
            # 将数据加载到缓存（可能需要替换）
            self._load_to_cache(address)
            return self.memory[address]['data']
        
        # 从硬盘加载
        self.disk_accesses += 1
        print(f"硬盘访问: 地址 {address} 数据 {self.disk[address]}")
        
        # 将数据加载到内存（可能需要替换）
        self._load_to_memory(address)
        
        # 将数据加载到缓存（可能需要替换）
        self._load_to_cache(address)
        
        return self.disk[address]

    def _load_to_cache(self, address):
        """将数据从内存加载到缓存（使用 LRU 替换策略）"""
        if address not in self.cache:
            if len(self.cache) >= self.cache_size:
                # 找到最近最少使用的数据（LRU）
                lru_address = min(self.cache, key=lambda k: self.cache[k]['time'])
                del self.cache[lru_address]
                print(f"缓存替换: 移除地址 {lru_address}")
            
            # 加载数据到缓存
            self.cache[address] = {
                'data': self.memory[address]['data'] if address in self.memory else self.disk[address],
                'time': time.time()
            }
            print(f"缓存加载: 地址 {address} 数据 {self.cache[address]['data']}")

    def _load_to_memory(self, address):
        """将数据从硬盘加载到内存（使用 LRU 替换策略）"""
        if address not in self.memory:
            if len(self.memory) >= self.memory_size:
                # 找到最近最少使用的数据（LRU）
                lru_address = min(self.memory, key=lambda k: self.memory[k]['time'])
                del self.memory[lru_address]
                print(f"内存替换: 移除地址 {lru_address}")

            # 加载数据到内存
            self.memory[address] = {
                'data': self.disk[address],
                'time': time.time()
            }
            print(f"内存加载: 地址 {address} 数据 {self.memory[address]['data']}")

    def get_statistics(self):
        """获取命中率统计"""
        cache_hit_rate = (self.cache_hits / self.total_accesses) * 100 if self.total_accesses > 0 else 0
        memory_hit_rate = ((self.cache_hits + self.memory_hits) / self.total_accesses) * 100 if self.total_accesses > 0 else 0
        return {
            "缓存命中率": f"{cache_hit_rate:.2f}%",
            "内存命中率": f"{memory_hit_rate:.2f}%",
            "硬盘访问次数": self.disk_accesses,
            "总访问次数": self.total_accesses
        }

# 模拟程序
if __name__ == "__main__":
    # 初始化存储系统
    storage = StorageSystem(cache_size=4, memory_size=16, disk_size=100)

    # 模拟访问随机地址
    print("开始模拟访问...")
    for _ in range(20):
        address = random.randint(0, 99)
        data = storage.access_data(address)
        time.sleep(0.1)  # 模拟时间流逝

    # 输出统计结果
    stats = storage.get_statistics()
    print("\n模拟结束，统计结果：")
    for key, value in stats.items():
        print(f"{key}: {value}")