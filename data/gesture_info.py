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
    "Eastcoast": {
        "description": "Variatsiya pal'tsev v forme «E».",
        "history": "Otvet zapadnomu poberezh'yu. Repery N'yu-Iorka i drugih vostochnyh gorodov pokazyvali etot znak, podcherkivaya prinadlezhnost' k svoei tusovke. On olichitvorial ne tol'ko lokatsiyu, no i stil' muzyki — bolee agressivnyi, surovy, ulichnyi.",
        "meaning": "East Coast, vostochnoye poberezh'ye.",
        "image": os.path.join(GESTURE_IMAGES_DIR, "eastcoast.jpg")
    },
    "Crips": {
        "description": "Variatsiya pal'tsev v forme «S».",
        "history": "Crips — krupneishaya banda gangsterov, osnovannaya eshche v 1969 godu 15-tiletniem shkol'nikom. Kak i u lyuboi drugoi gruppirovki, u nih byl svoi jest, ego ispol'zovali chtoby pokazat' prinadlezhnost' k nei. Naibolee izvestnye predstaviteli etoi bandy — N.W.A., Snoop Dog, Gunna, Schoolboy Q i drugie.",
        "meaning": "Oboznachayet prinadlezhnost' k Crips.",
        "image": os.path.join(GESTURE_IMAGES_DIR, "crips.jpg")
    },
    "Bloods": {
        "description": "Kombinatsiya pal'tsev, formiruyushchaya slovo «Blood».",
        "history": "Bloods — eshche odna afroamerikanskaya banda, sozdannaya v 1972 godu, chtoby protivostoyat' Crips. Ee predstaviteli nosili iskluchitel'no krasnyi tsvet. Ih jest neskol'ko slozhnee, chem u Crips. Kstati, v etoi bande sostoit mnogo predstavitelei novoi shkoly. Naprimer: Offset, 21 Savage, The Game, Trippie Red, Lil Wayne i drugie.",
        "meaning": "Oboznachayet prinadlezhnost' k Bloods.",
        "image": os.path.join(GESTURE_IMAGES_DIR, "bloods.jpg")
    },
    "Crip Killa": {
        "description": "Provokatsionnyi jest bandy Bloods.",
        "history": "Etot znak ispol'zovalsya uchastnikami Bloods, chtoby zayavit' o svoem neprimirimom otnoshenii k Crips. Bukval'no — «ubiytsa Crips». V ulichnoi kulture takie veshchi krajne opasny dlya demonstratsii, osobenno bez sootvetstvuyushchego prikrytiya.",
        "meaning": "Vrazhdebnyi znak protiv Crips.",
        "image": os.path.join(GESTURE_IMAGES_DIR, "ck.jpg")
    },
    "b.k": {
        "description": "Zhest ot Crips v adres Bloods.",
        "history": "Etot jest — otvetochnyi ot bandy Crips. Oznachaet on blood killa, to est' ubiytsa Bloods. Eti veshchi neredko provotsirovali real'nye konflikty i nasilie na ulitsah.",
        "meaning": "Vrazhdebnyi znak protiv Bloods.",
        "image": os.path.join(GESTURE_IMAGES_DIR, "bk.jpg")
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
    "Piru": {
        "description": "Zhest bandy Piru.",
        "history": "Eto zhest bandy pod nazvaniem Piru Street Boys, kotoraya tozhe byla sozdana v 1969 godu. Iznachal'no eta gruppirovka byla vmeste s Crips, no spustya nekotoroe vremya otdelilas'.",
        "meaning": "Oboznachayet prinadlezhnost' k Piru.",
        "image": os.path.join(GESTURE_IMAGES_DIR, "piru.jpg")
    },
    "Ronaldinho": {
        "description": "Zhest Shaka.",
        "history": "Zhest Shaka imeet gavaiskoe proishozhdenie, i ego ispol'zuyut kak privetstvie i znak odobreniya.",
        "meaning": "Zhest «shaka» (takzhe izvestnyi kak «jambo») predstavlyaet soboi privetstvennyi zhest, pri kotorom bol'shoi palets i mizinets vytianutы naruzhu, a ostal'nye pal'tsy prizhaty k ladoni. On chasto ispol'zuetsya v srede serferov i voennyh, kak simvol druzhelyubiya i vse horosho. Yarkim predstavitelem yavlyaetsya Ronaldinho.",
        "image": os.path.join(GESTURE_IMAGES_DIR, "ron.jpg")
    },
    "Kiz": {
        "description": "HAUNTED FAMILY.",
        "history": "U etogo zhesta dvoinoi smysl. V vizual'nom plane iz tryoh ostavshihsya pal'tsev (ukazatel'nogo, srednego i mizinza) mozhno sobrat' zaglavnye bukvy H i F — abbreviatura ego obedinenie Haunted Family.",
        "meaning": "V SNG etot zhest zakreplilsya za Kizaru i fanatami Haunted Family.",
        "image": os.path.join(GESTURE_IMAGES_DIR, "kiz.jpg")
    },
    "Players club": {
        "description": "Variatsiya pal'tsev v forme «P».",
        "history": "Zhest simvoliziruet uvazhenie k Sankt-Peterburgu. Forma pal'tsev napominaet bukvu P, kotoraya assotsiiiruetsya s nazvaniem goroda — Piter. Takzhe zhest izvesten kak Saint-P.",
        "meaning": "Oboznachayet prinadlezhnost' k gorodu Sankt-Peterburg, yarkimi predstavitelyami yavlyayutsya: OBLADAET i ICEGERGERT.",
        "image": os.path.join(GESTURE_IMAGES_DIR, "pc.jpg")
    },
    "Cigarettes": {
        "description": "Kurenie ubivaet.",
        "history": "",
        "meaning": "",
        "image": os.path.join(GESTURE_IMAGES_DIR, "c.jpg")
    },
    "52": {
        "description": "Variatsiya pal'tsev v forme «5» i «2».",
        "history": "52 ngg — molodoe obedinenie v rossiiskoi hip-hop stsene, sostoyashchee iz pyati uchastnikov: FRIENDLY THUG 52 NGG, ALBLAK 52, Glocki52, SaintPrince 52 i MyDee 52.",
        "meaning": "Vse oni rodom iz Sankt-Peterburga i predstavlyayut soboi odnu iz samyh interesnyh komand na segodnyashnii den'.",
        "image": os.path.join(GESTURE_IMAGES_DIR, "52.jpg")
    },
    "Simple": {
        "description": "Pora trenirovatsya.",
        "history": "",
        "meaning": "",
        "image": os.path.join(GESTURE_IMAGES_DIR, "simple.jpg")
    },
    "Other": {
        "description": "Neizvestnyi zhest.",
        "history": "",
        "meaning": "",
        "image": None
    }
}