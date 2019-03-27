# coding: utf-8
import os

# botアカウントのトークンを指定
API_TOKEN = os.environ["SAMPLE_API_TOKEN"]

# このbot宛のメッセージで、どの応答にも当てはまらない場合の応答文字列
DEFAULT_REPLY = "こんにちは"

# 使用するPORT
PORT = os.environ['PORT'] or 8080

# プラグインスクリプトを置いてあるサブディレクトリ名のリスト
PLUGINS = ['plugins']
