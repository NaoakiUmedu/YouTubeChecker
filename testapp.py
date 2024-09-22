from ast import keyword
from apiclient.discovery import build
import os


class video_info:
    """動画の検索結果を保持するクラス"""
    kugiri = '####################'
    kaigyo = '\n'
    separator = '\t'

    def __init__(self, title, publishDate, channeltitle):
        self.title = title
        self.publishDate = publishDate
        self.channeltitle = channeltitle

    def printInfo(self):
        print(self.getInfoGui())

    def getInfoGui(self) -> str:
        return self.kugiri + self.kaigyo + self.title + self.kaigyo + self.channeltitle + self.kaigyo + self.publishDate + self.kaigyo

    def getInfoForFile(self) -> str:
        return (self.publishDate + self.separator + self.title + self.channeltitle + self.separator + self.kaigyo)


class filehandler:
    """ファイルを操作する"""
    filedir = "./data/"
    filenameOshiri = "_vinfofile.txt"

    def getFileName(self, keyword) -> str:
        """ファイル名を取得する"""
        return keyword + self.filenameOshiri

    def getOldFileName(self, keyword) -> str:
        """ファイル名を取得する"""
        return "old_" + self.getFileName(keyword)

    def moveOldFile(self, keyword):
        """前回の結果をリネームする"""
        filepath = self.filedir + self.getFileName(keyword)
        oldfilepath = self.filedir + self.getOldFileName(keyword)
        try:
            os.remove(oldfilepath)
        except (FileNotFoundError):
            pass
        try:
            os.rename(filepath, oldfilepath)
        except (FileNotFoundError):
            pass

    def writeVideoInfoFile(self, keyword, vinfos):
        """ファイルに結果を記録する"""
        filepath = self.filedir + self.getFileName(keyword)
        vinfofile = open(filepath, "w", encoding='utf-8')
        for vinfo in vinfos:
            content: str = vinfo.getInfoForFile()
            vinfofile.write(content)
        vinfofile.close

    def checkDiff(self, keyword) -> bool:
        """oldと違いがあるか見る"""
        filepath = self.filedir + self.getFileName(keyword)
        contents: list
        oldfilepath = self.filedir + self.getOldFileName(keyword)
        oldcontents: list

        try:
            now = open(filepath, "r", encoding='utf-8')
            contents = now.readlines()
            now.close
        except (FileNotFoundError):
            print("比較結果：nowファイルなし")
            return False

        try:
            old = open(oldfilepath, "r", encoding='utf-8')
            oldcontents = old.readlines()
            old.close
        except (FileNotFoundError):
            print("比較結果：oldファイルなし")
            return False

        if contents != oldcontents:
            diff = list(filter(lambda x: x not in contents, oldcontents))
            return diff
        return False


class youtube_discoverer:
    """YouTubeの検索をするクラス"""

    def discoverKeyword(self, keyword):
        """keywordをYouTubeで検索する"""
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        # part 検索方法
        # q query
        search_responses = youtube.search().list(
            part='snippet',
            q=keyword,
            type='video',
            maxResults=10,
            order='date'
        ).execute()
        return search_responses

    def getVideoInfos(self, search_responses) -> list:
        """動画の検索結果のクラスを作る"""
        vinfos: list = list()
        for search_response in search_responses['items']:
            snipet_info = search_response['snippet']
            vinfo = video_info(
                snipet_info['title'], snipet_info['publishedAt'], snipet_info['channelTitle'])
            vinfos.append(vinfo)
        return vinfos


# メインプログラム
if __name__ == '__main__':
    # 検索したいキーワード
    keywords = [
        'Kenneth Hesketh',
        'Patrick Hiketick'
    ]

    # 認証情報の設定
    keyfile = open("./Key.txt", "r")
    YOUTUBE_API_KEY = keyfile.readline()
    keyfile.close()

    # キーワードごとに検索していく
    discoverer = youtube_discoverer()
    file_io = filehandler()
    for keyword in keywords:
        # 前回の検索結果を退避
        file_io.moveOldFile(keyword)
        # 検索を実行する
        videos = discoverer.getVideoInfos(discoverer.discoverKeyword(keyword))
        # 今回の検索結果を保存
        file_io.writeVideoInfoFile(keyword, videos)

        # 前回と今回の検索結果と比較
        diffs = file_io.checkDiff(keyword)
        if diffs:
            print("★★★ 検索キーワード[" + keyword + "] 更新あり! ★★★")
            for diff in diffs:
                print('■'+diff)
        else:
            print("☆☆ 検索キーワード[" + keyword + "] 更新なし ☆")
        print()
