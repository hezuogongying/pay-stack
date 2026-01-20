"""
Pay-Stack Python SDK 安装配置
"""

from setuptools import setup, find_packages
from pathlib import Path

# 读取README文件
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="pay-stack",
    version="1.0.0",
    author="Pay-Stack Team",
    author_email="139563281@qq.com",
    description="Python支付SDK - 支持微信、支付宝、QQ等多种支付方式",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hezuogongying/pay-stack",
    packages=find_packages(exclude=["tests", "tests.*", "examples", "docs"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "cryptography>=41.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.1.0",
            "mypy>=1.5.0",
        ],
    },
    keywords="payment alipay wechat qq pay sdk",
    project_urls={
        "Bug Reports": "https://github.com/hezuogongying/pay-stack/issues",
        "Source": "https://github.com/hezuogongying/pay-stack",
        "Documentation": "https://github.com/hezuogongying/pay-stack/wiki",
    },
)
