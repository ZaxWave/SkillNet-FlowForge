#!/usr/bin/env python3
"""
SkillNet 站点统计双向同步脚本

将国内和海外两个 Supabase 实例的 site_stats 表进行交叉同步：
  - 读取国内的 local 行 → 写入海外的 remote 行
  - 读取海外的 local 行 → 写入国内的 remote 行

这样两边的 get_total_stats() 都能返回全局合计值。

用法:
    python sync_stats.py              # 执行同步
    python sync_stats.py --dry-run    # 仅预览，不写入

部署建议（crontab，每小时执行一次）:
    0 * * * * /usr/bin/python3 /path/to/sync_stats.py >> /var/log/sync_stats.log 2>&1

依赖:
    pip install supabase
"""

import argparse
import os
import sys
from datetime import datetime

try:
    from supabase import create_client, Client
except ImportError:
    print("ERROR: supabase-py not installed. Run: pip install supabase")
    sys.exit(1)

# ============================================================
# 配置：可通过环境变量覆盖，也可直接修改默认值
# ============================================================

DOMESTIC_URL = os.environ.get(
    "DOMESTIC_SUPABASE_URL",
    "http://121.41.117.246:8001"
)
DOMESTIC_KEY = os.environ.get(
    "DOMESTIC_SUPABASE_KEY",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoic2VydmljZV9yb2xlIiwiaXNzIjoic3VwYWJhc2UiLCJpYXQiOjE3Njk0MTM5MDUsImV4cCI6MTkyNzA5MzkwNX0.8UJdJ0LqhQw-BVKohL1qzXisFPsb45mIJjOSmqN2K4Q"
)

OVERSEAS_URL = os.environ.get(
    "OVERSEAS_SUPABASE_URL",
    "http://94.72.120.33:8000"
)
OVERSEAS_KEY = os.environ.get(
    "OVERSEAS_SUPABASE_KEY",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoic2VydmljZV9yb2xlIiwiaXNzIjoic3VwYWJhc2UiLCJpYXQiOjE3MDAwMDAwMDAsImV4cCI6MjAwMDAwMDAwMH0.Eq-N-l9VcV_gM2H-eBgKLCkScFqzGeB4qiTmCyW0WU8"
)


def log(msg: str):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")


def read_local_stats(client: Client, label: str) -> dict | None:
    """读取某个实例的 source='local' 行"""
    try:
        result = (
            client.table("site_stats")
            .select("visits, downloads")
            .eq("source", "local")
            .single()
            .execute()
        )
        data = result.data
        log(f"  {label} local: visits={data['visits']}, downloads={data['downloads']}")
        return data
    except Exception as e:
        log(f"  ERROR reading {label} local: {e}")
        return None


def write_remote_stats(client: Client, label: str, visits: int, downloads: int) -> bool:
    """将对端数据写入某个实例的 source='remote' 行"""
    try:
        client.table("site_stats").upsert({
            "source": "remote",
            "visits": visits,
            "downloads": downloads,
            "updated_at": datetime.utcnow().isoformat()
        }).execute()
        log(f"  {label} remote updated: visits={visits}, downloads={downloads}")
        return True
    except Exception as e:
        log(f"  ERROR writing {label} remote: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="SkillNet 站点统计双向同步")
    parser.add_argument("--dry-run", action="store_true", help="仅预览数据，不执行写入")
    args = parser.parse_args()

    log("=" * 50)
    log("SkillNet stats sync started" + (" (DRY RUN)" if args.dry_run else ""))

    # 初始化客户端
    try:
        domestic = create_client(DOMESTIC_URL, DOMESTIC_KEY)
        log(f"Connected to domestic: {DOMESTIC_URL}")
    except Exception as e:
        log(f"FATAL: Cannot connect to domestic Supabase: {e}")
        domestic = None

    try:
        overseas = create_client(OVERSEAS_URL, OVERSEAS_KEY)
        log(f"Connected to overseas: {OVERSEAS_URL}")
    except Exception as e:
        log(f"FATAL: Cannot connect to overseas Supabase: {e}")
        overseas = None

    if not domestic and not overseas:
        log("Both connections failed. Exiting.")
        sys.exit(1)

    # 读取两端 local 数据
    domestic_stats = read_local_stats(domestic, "domestic") if domestic else None
    overseas_stats = read_local_stats(overseas, "overseas") if overseas else None

    if args.dry_run:
        log("DRY RUN - no writes performed")
        if domestic_stats and overseas_stats:
            total_visits = domestic_stats["visits"] + overseas_stats["visits"]
            total_downloads = domestic_stats["downloads"] + overseas_stats["downloads"]
            log(f"  Projected totals: visits={total_visits}, downloads={total_downloads}")
        log("Done.")
        return

    # 交叉写入
    success = True

    # 国内 local → 海外 remote
    if domestic_stats and overseas:
        ok = write_remote_stats(overseas, "overseas", domestic_stats["visits"], domestic_stats["downloads"])
        success = success and ok
    elif not domestic_stats:
        log("  SKIP: domestic local data unavailable, cannot update overseas remote")

    # 海外 local → 国内 remote
    if overseas_stats and domestic:
        ok = write_remote_stats(domestic, "domestic", overseas_stats["visits"], overseas_stats["downloads"])
        success = success and ok
    elif not overseas_stats:
        log("  SKIP: overseas local data unavailable, cannot update domestic remote")

    # 输出同步后的合计
    if domestic_stats and overseas_stats:
        total_visits = domestic_stats["visits"] + overseas_stats["visits"]
        total_downloads = domestic_stats["downloads"] + overseas_stats["downloads"]
        log(f"  Synced totals: visits={total_visits}, downloads={total_downloads}")

    log("Sync " + ("completed successfully" if success else "completed with errors"))
    log("=" * 50)

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
