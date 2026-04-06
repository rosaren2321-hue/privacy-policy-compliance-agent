"""
单段 Markdown 上传腾讯云 COS，返回 URL（工作流插件用，不合并多段）。
"""
from __future__ import annotations

import os
import time
from typing import Optional

from qcloud_cos import CosConfig, CosS3Client

REGION = os.environ.get("TENCENT_COS_REGION", "ap-beijing")
BUCKET = os.environ.get("TENCENT_COS_BUCKET", "md-1386995694")

_cos_client: Optional[CosS3Client] = None


def _get_cos_client() -> CosS3Client:
    """
    懒加载 COS 客户端；凭证仅从环境变量读取。

    @returns {CosS3Client} 已配置的客户端
    @throws {ValueError} 未设置必需的环境变量时
    """
    global _cos_client
    if _cos_client is None:
        secret_id = os.environ.get("TENCENT_COS_SECRET_ID")
        secret_key = os.environ.get("TENCENT_COS_SECRET_KEY")
        if not secret_id or not secret_key:
            raise ValueError(
                "请设置环境变量 TENCENT_COS_SECRET_ID 与 TENCENT_COS_SECRET_KEY（可参考 .env.example）"
            )
        config = CosConfig(Region=REGION, SecretId=secret_id, SecretKey=secret_key)
        _cos_client = CosS3Client(config)
    return _cos_client

def upload_markdown_to_cos(md_content: str) -> str:
    """
    上传 Markdown 到 COS，返回可访问 URL。

    @param {str} md_content Markdown 正文
    @returns {str} 对象访问 URL
    """
    client = _get_cos_client()
    filename = f"output_{int(time.time())}.md"

    client.put_object(
        Bucket=BUCKET,
        Body=md_content,
        Key=filename,
        ContentType="text/markdown"
    )

    # 返回 URL 字符串
    md_url = f"https://{BUCKET}.cos.{REGION}.myqcloud.com/{filename}"
    return md_url

def main(params: dict) -> dict:
    """
    工作流入口函数。

    @param {dict} params 含 model_output_md
    @returns {dict} {"md_url": str} 插件固定输出变量名
    """
    model_output_md = params.get("model_output_md", "")
    if not model_output_md:
        return {"md_url": ""}  # 没有 Markdown 输出时返回空字符串

    md_url = upload_markdown_to_cos(model_output_md)
    return {"md_url": md_url}  # 注意这里是字典对象

# --- 使用示例 ---
if __name__ == "__main__":
    example_params = {
        "model_output_md": """
# 我的标题

这是大模型输出的 Markdown 内容。
- 列表1
- 列表2
"""
    }

    result = main(example_params)
    print(result)
    # 输出示例:
    # {"md_url": "https://md-1386995694.cos.ap-beijing.myqcloud.com/output_1763272438.md"}
