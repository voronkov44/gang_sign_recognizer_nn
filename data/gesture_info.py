import os

# Базовый путь к изображениям жестов
GESTURE_IMAGES_DIR = os.path.join(os.path.dirname(__file__), "gesture_images")

GESTURE_INFO = {
    "Westcoast": {
        "description": "Raspal'tsovka «W» iz pal'tsev.",
        "history": "Etot jest stal simvolom zapadnogo poberezh'ya SShA, osobenno Los-Andzhelesa. Aktivno ispol'zovalsya v rep-kulture 90-h — Tupac, Snoop Dogg, Ice Cube i drugie chasto demonstrirovali ego na fotkah i koncertah. Eto byla ne prosto moda, a marker «my otsyuda», svoya geografiya i ulichnoe bratstvo.",
        "meaning": "Znak prinadlezhnosti k West Coast, zapadnoi rep-stsene.",
        "image": os.path.join(GESTURE_IMAGES_DIR, "westcoast.jpg")
    },
    "Crips": {
        "description": "Variatsiya pal'tsev v forme «S».",
        "history": "Crips — krupneishaya banda gangsterov, osnovannaya eshche v 1969 godu 15-tiletniem shkol'nikom. Kak i u lyuboi drugoi gruppirovki, u nih byl svoi jest, ego ispol'zovali chtoby pokazat' prinadlezhnost' k nei. Naibolee izvestnye predstaviteli etoi bandy — N.W.A., Snoop Dog, Gunna, Schoolboy Q i drugie.",
        "meaning": "Oboznachayet prinadlezhnost' k Crips.",
        "image": os.path.join(GESTURE_IMAGES_DIR, "crips.jpg")
    },
    "MS-13": {
        "description": "Zhest bandy MS-13.",
        "history": "Pomimo afroamerikanskih band v USA bylo neskol'ko opasnyh latinoamerikanskih gruppirovok. Odna iz nih — «Mara Salvatrucha» (ili, kak ih eshche nazyvali, MS-13). Ih jest ochen' pohozh na rokerskuyu «kozu».",
        "meaning": "Oboznachayet prinadlezhnost' k MS-13.",
        "image": os.path.join(GESTURE_IMAGES_DIR, "ms.jpg")
    },
    "Latin kings": {
        "description": "Pohozh na MS-13, no bez sohnutogo bol'shogo pal'tsa.",
        "history": "Latin Kings — odna iz stareishih i vliyatel'nyh latinoamerikanskih band. U Latin Kings sobstvennyi kodeks, tatu, zhesty i odezhda. Ih raspal'tsovku legko sputat' s MS-13, poetomu vnutri subkultury eti nyuansy kriticheski vazhny.",
        "meaning": "Oboznachayet prinadlezhnost' k Latin Kings.",
        "image": os.path.join(GESTURE_IMAGES_DIR, "LatinKing.jpg")
    },
    "Ronaldinho": {
        "description": "Zhest Shaka.",
        "history": "Zhest Shaka imeet gavaiskoe proishozhdenie, i ego ispol'zuyut kak privetstvie i znak odobreniya.",
        "meaning": "Zhest «shaka» (takzhe izvestnyi kak «jambo») predstavlyaet soboi privetstvennyi zhest, pri kotorom bol'shoi palets i mizinets vytianutы naruzhu, a ostal'nye pal'tsy prizhaty k ladoni. On chasto ispol'zuetsya v srede serferov i voennyh, kak simvol druzhelyubiya i vse horosho. Yarkim predstavitelem yavlyaetsya Ronaldinho.",
        "image": os.path.join(GESTURE_IMAGES_DIR, "ron.jpg")
    },
    "Players club": {
        "description": "Variatsiya pal'tsev v forme «P».",
        "history": "Zhest simvoliziruet uvazhenie k Sankt-Peterburgu. Forma pal'tsev napominaet bukvu P, kotoraya assotsiiiruetsya s nazvaniem goroda — Piter. Takzhe zhest izvesten kak Saint-P.",
        "meaning": "Oboznachayet prinadlezhnost' k gorodu Sankt-Peterburg, yarkimi predstavitelyami yavlyayutsya: OBLADAET i ICEGERGERT.",
        "image": os.path.join(GESTURE_IMAGES_DIR, "pc.jpg")
    },
    "Simple": {
        "description": "Pora trenirovatsya.",
        "history": "",
        "meaning": "",
        "image": os.path.join(GESTURE_IMAGES_DIR, "simple.jpg")
    }
}