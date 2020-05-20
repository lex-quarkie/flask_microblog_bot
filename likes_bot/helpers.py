import random
import string
from config import usernames


def generate_username():
    return random.choice(usernames) + str(random.randint(0, 99))


def pw_gen(size=8, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def generate_post_body():
    pangrams = ['The quick brown fox jumps over the lazy dog.',
                'Jackdaws love my big sphinx of quartz.',
                'Τάχιστη αλώπηξ βαφής ψημένη γη, δρασκελίζει υπέρ νωθρού κυνός.',
                'Γαζίες καὶ μυρτιὲς δὲν θὰ βρῶ πιὰ στὸ χρυσαφὶ ξέφωτο.',
                'Ξεσκεπάζω τὴν ψυχοφθόρα βδελυγμία.',
                'Ζαφείρι δέξου πάγκαλο, βαθῶν ψυχῆς τὸ σῆμα.',
                'Chuaigh bé mhórshách le dlúthspád fíorfhinn trí hata mo dhea-phorcáin bhig.',
                'Quiere la boca exhausta vid, kiwi, piña y fugaz jamón.',
                'Fabio me exige, sin tapujos, que añada cerveza al whisky.',
                'Jovencillo emponzoñado de whisky, ¡qué figurota exhibe!',
                'David exige plazo fijo para el embarque de truchas y niños New York.',
                'La cigüeña tocaba cada vez mejor el saxofón y el búho pedía kiwi y queso.',
                'El jefe buscó el éxtasis en un imprevisto baño de whisky y gozó como un duque.',
                'Exhíbanse politiquillos zafios, con orejas kilométricas y uñas de gavilán.',
                'El pingüino Wenceslao hizo kilómetros bajo exhaustiva lluvia y frío, añoraba a su querido cachorro.',
                'El veloz murciélago hindú comía feliz cardillo y kiwi.',
                'La cigüeña tocaba el saxofón detrás del palenque de paja.',
                'Чуєш їх, доцю, га? Кумедна ж ти, прощайся без ґольфів!',
                'Фабрикуймо гідність, лящім їжею, ґав хапаймо, з’єднавці чаш!',
                'Їхав єдиний москаль. Чув, що віз царю жезл, п’ять шуб і гофр.',
                'Юнкерський джинґл, що при безхліб’ї чує фашист, це ловця гімн.',
                'Грішний джиґіт, що хотів у Францію, позбувався цієї думки з’їдаючи трюфель.',
                'Безпігментний шлейф інжектора здається очищався від корозії в Цюриху.',
                'В чащах юга жил бы цитрус? Да, но фальшивый экземпляр!',
                'Друг мой эльф! Яшке б свёз птиц южных чащ!',
                'Любя, съешь щипцы, — вздохнёт мэр, — кайф жгуч.',
                'Шеф взъярён тчк щипцы с эхом гудбай Жюль.',
                'Эй, жлоб! Где туз? Прячь юных съёмщиц в шкаф.',
                'Экс-граф? Плюш изъят. Бьём чуждый цен хвощ!',
                'Эх, чужак! Общий съём цен шляп (юфть) — вдрызг!',
                'Эх, чужд кайф, сплющь объём вши, грызя цент.',
                'Чушь: гид вёз кэб цапф, юный жмот съел хрящ.'
                ]
    return ''.join(random.choices(pangrams, k=random.randint(3, 10)))
