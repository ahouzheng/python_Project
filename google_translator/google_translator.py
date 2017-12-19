import requests
import execjs

url_Src = 'https://translate.google.cn/translate_a/single'

get_tk = execjs.compile('''function TL(a) {
    var k = "";
    var b = 406644;
    var b1 = 3293161072;
    
    var jd = ".";
    var $b = "+-a^+6";
    var Zb = "+-3^+b+-f";

    for (var e = [], f = 0, g = 0; g < a.length; g++) {
        var m = a.charCodeAt(g);
        128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023),
        e[f++] = m >> 18 | 240,
        e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224,
        e[f++] = m >> 6 & 63 | 128),
        e[f++] = m & 63 | 128)
    }
    a = b;
    for (f = 0; f < e.length; f++) a += e[f],
    a = RL(a, $b);
    a = RL(a, Zb);
    a ^= b1 || 0;
    0 > a && (a = (a & 2147483647) + 2147483648);
    a %= 1E6;
    return a.toString() + jd + (a ^ b)
};

function RL(a, b) {
    var t = "a";
    var Yb = "+";
    for (var c = 0; c < b.length - 2; c += 3) {
        var d = b.charAt(c + 2),
        d = d >= t ? d.charCodeAt(0) - 87 : Number(d),
        d = b.charAt(c + 1) == Yb ? a >>> d: a << d;
        a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d
    }
    return a
}
''')


def trans(text):
    if len(text.encode('utf-8')) > len(text) * 2:
        # 汉译英
        sl = 'zh-CN'
        tl = 'en'
    else:
        # 英译汉
        sl = "en"
        tl = 'zh-CN'

    tk = get_tk.call("TL", text)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
     Chrome/62.0.3202.75 Safari/537.36'
    }   

    data = {
        'client': 't',
        'sl': sl,
        'tl': tl,
        'hl': 'zh-CN',
        # 'dt': 'at',
        # 'dt': 'bd',
        # 'dt': 'ex',
        # 'dt': 'ld',
        # 'dt': 'md',
        # 'dt': 'qca',
        # 'dt': 'rw',
        # 'dt': 'rm',
        # 'dt': 'ss',
        'dt': 't',
        'ie': 'UTF-8',
        'oe': 'UTF-8',
        'source': 'btn',
        'ssel': '6',
        'tsel': '3',
        'kc': '0',
        'tk': tk,
        'q': text
    }
    res1 = requests.get(url_Src, headers=headers, params=data).json()
    to_text = ''
    for item in res1[0]:
        to_text += item[0]
    return to_text

while True:
    para = input("input:")
    print(trans(para))




