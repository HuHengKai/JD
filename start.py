from  scrapy import cmdline
#cmdline.execute("scrapy crawl baidu".split())
cmdline.execute("scrapy crawl baidu -o a.csv".split())
