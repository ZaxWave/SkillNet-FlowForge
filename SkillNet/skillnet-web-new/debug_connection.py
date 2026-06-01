import os
import toml
import time
from supabase import create_client

def test_connection():
    print("1. 读取配置文件...")
    try:
        secrets = toml.load(".streamlit/secrets.toml")
        url = secrets["supabase"]["SUPABASE_URL"]
        key = secrets["supabase"]["SUPABASE_KEY"]
        print(f"   URL: {url}")
        print("2. 初始化 Supabase 客户端...")
        supabase = create_client(url, key)
        print("   客户端对象创建成功")
        
        print("3. 尝试连接数据库 (发送 HEAD 请求)...")
        start_time = time.time()
        
        # 尝试简单的请求 (改为普通 GET 请求以获取详细错误信息，避免 HEAD 请求无 Body 导致的解析报错)
        print("   正在发送 GET 请求测试表是否存在...")
        try:
            response = supabase.table("skills").select("*").limit(1).execute()
            print(f"4. 连接成功!")
            print(f"   返回数据示例: {response.data}")
        except Exception as query_err:
             print(f"   查询请求失败. 尝试获取底层响应信息...")
             # 尝试从异常中提取更多信息
             if hasattr(query_err, 'code'):
                 print(f"   Error Code: {query_err.code}")
             if hasattr(query_err, 'details'):
                 print(f"   Error Details: {query_err.details}")
             if hasattr(query_err, 'message'):
                 print(f"   Error Message: {query_err.message}")
             raise query_err
        
        end_time = time.time()
        
    except Exception as e:
        print("\n[错误] 连接失败!")
        print(f"错误信息: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_connection()
