import os

from django.http import HttpResponse, FileResponse, StreamingHttpResponse
from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request, 'mymain_index.html')


def search(request):
    if request.POST:
        # word_file = request.FILES.get('word_file')
        import os

        wenjian = request.FILES['word_file']  # 读取文件
        baseDir = os.path.dirname(os.path.abspath(__name__))  # 获取运行路径
        jpgdir = os.path.join(baseDir, 'media')  # 加上media路径
        wordcloud_path = jpgdir
        print(wordcloud_path)
        filename = os.path.join(jpgdir, wenjian.name)  # 获取文件路径
        fobj = open(filename, 'wb+')  # 打开上传文件
        for x in wenjian.chunks():
            fobj.write(x)  # request.FILES,文件专用
        fobj.close()
        # print(22222)
        # print(filename)

        f = open(filename, 'r', encoding='utf-8').read()
        counts = {}  # 字典类型
        import jieba



        wordsList = jieba.lcut(f)
        for word in wordsList:
            word = word.replace("，", "").replace("！", "").replace("“", "") \
                .replace("”", "").replace("。", "").replace("？", "").replace("：", "").replace("【", "").replace("】", "") \
                .replace("...", "").replace("、", "").strip(' ').strip('\r\n')
            if len(word) == 1 or word == "":
                continue  # 跳过特殊字符,继续下一个
            else:
                counts[word] = counts.get(word, 0) + 1  # 单词计数

        count_order = sorted(counts.items(), key=lambda x: x[1], reverse=True)  # 降序排列
        # items = list(counts.items())  # 将字典转为list
        # items.sort(key=lambda x: x[1], reverse=True)  # 根据单词出现次数降序排序
        list_words = []
        for a in count_order:
            list_words += [list(a)]

        import xlwt

        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet('词频分析')
        worksheet.write(0, 0, '词语')
        worksheet.write(0, 1, '次数')
        row = 1
        only_word = []
        for i in range(len(list_words)):
            print(list_words[i][0])
            only_word.append(list_words[i][0])
            worksheet.write(row, 0, list_words[i][0])
            worksheet.write(row, 1, list_words[i][1])
            row = row + 1
        workbook.save('WordAnalysis.xls')

        # 绘制词云
        from wordcloud import WordCloud
        import matplotlib.pyplot as plt

        print(only_word)

        # 生成对象
        font_path = "C:\Windows\Fonts\STKAITI.TTF"
        text = " ".join(only_word[0:200])
        wc = WordCloud(font_path=font_path, width=800, height=600, mode='RGBA', background_color=None).generate(
            text)

        # # 显示词云
        # plt.imshow(wc, interpolation='bilinear')
        # plt.axis('off')
        # plt.show()

        # 保存到文件
        wc.to_file('wordcloud.png')  # 生成图像是透明的

        # print(3333)
        # print(list_words)
        # print(count_order)
        # print(counts)

        return render(request, "mymain_index.html", {"data": count_order, "word": list_words})


def download(request):
    str = request.POST.get('result')
    result = str.replace('"', '').split(',')
    while '' in result:
        result.remove('')

    import xlwt

    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('词频分析')
    worksheet.write(0, 0, '词语')
    worksheet.write(0, 1, '次数')
    row = 1
    for i in range(len(result)):
        worksheet.write(row, 0, result[i].split('_')[0])
        worksheet.write(row, 1, result[i].split('_')[1])
        row = row + 1
    workbook.save('WordAnalysis.xls')

    return HttpResponse('文件已经生成')


def download_file(request):
    name = 'WordAnalysis.xls'
    baseDir = os.path.dirname(os.path.abspath(__name__))  # 获取运行路径
    file_name = os.path.join(baseDir, name)  # 获取文件路径
    print(file_name)
    file = open(file_name, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment; filename={0}'.format(name)
    return response


def download_image(request):
    name = 'wordcloud.png'
    baseDir = os.path.dirname(os.path.abspath(__name__))  # 获取运行路径
    file_name = os.path.join(baseDir, name)  # 获取文件路径
    print(file_name)
    file = open(file_name, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment; filename={0}'.format(name)
    return response
