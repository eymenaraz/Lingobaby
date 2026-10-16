import tkinter as tk
from tkinter import ttk, messagebox
import random

# ==========================================
# MEB MÜFREDATINA UYGUN KONU VE KELİME VERİLERİ
# ==========================================
# MEB Okul Öncesi, 1. ve 2. Sınıf İngilizce Müfredatına göre hazırlanmış detaylı içerik.
CURRICULUM_DATA = {
    "kindergarten": {
        "title": "Anaokulu (Preschool)",
        "icon": "🎨",
        "description": "Temel kavramlar, sesler, renkler ve eğlenceli görsel tanıma adımları.",
        "levels": [
            {
                "id": "k_1",
                "title": "1. Level: Colors (Renkler)",
                "topic_desc": "Temel renkleri tanıyalım ve İngilizce isimlerini öğrenelim.",
                "words": [
                    {"en": "Red", "tr": "Kırmızı", "emoji": "🔴", "color": "#FF4D4D"},
                    {"en": "Blue", "tr": "Mavi", "emoji": "🔵", "color": "#4D94FF"},
                    {"en": "Yellow", "tr": "Sarı", "emoji": "🟡", "color": "#FFD700"},
                    {"en": "Green", "tr": "Yeşil", "emoji": "🟢", "color": "#4CAF50"},
                    {"en": "Orange", "tr": "Turuncu", "emoji": "🟠", "color": "#FF9800"},
                    {"en": "Purple", "tr": "Mor", "emoji": "🟣", "color": "#9C27B0"}
                ]
            },
            {
                "id": "k_2",
                "title": "2. Level: Cute Animals (Sevimli Hayvanlar)",
                "topic_desc": "Çevremizdeki tatlı hayvan dostlarımızı keşfedelim.",
                "words": [
                    {"en": "Cat", "tr": "Kedi", "emoji": "🐱", "color": "#FF9800"},
                    {"en": "Dog", "tr": "Köpek", "emoji": "🐶", "color": "#795548"},
                    {"en": "Bird", "tr": "Kuş", "emoji": "🐦", "color": "#2196F3"},
                    {"en": "Fish", "tr": "Balık", "emoji": "🐟", "color": "#00BCD4"},
                    {"en": "Rabbit", "tr": "Tavşan", "emoji": "🐰", "color": "#E91E63"},
                    {"en": "Duck", "tr": "Ördek", "emoji": "🦆", "color": "#8BC34A"}
                ]
            },
            {
                "id": "k_3",
                "title": "3. Level: Numbers 1-5 (Sayılar 1-5)",
                "topic_desc": "İlk 5 sayıyı İngilizce saymayı öğrenelim.",
                "words": [
                    {"en": "One", "tr": "Bir", "emoji": "1️⃣", "color": "#E91E63"},
                    {"en": "Two", "tr": "İki", "emoji": "2️⃣", "color": "#9C27B0"},
                    {"en": "Three", "tr": "Üç", "emoji": "3️⃣", "color": "#3F51B5"},
                    {"en": "Four", "tr": "Dört", "emoji": "4️⃣", "color": "#009688"},
                    {"en": "Five", "tr": "Beş", "emoji": "5️⃣", "color": "#FF5722"}
                ]
            }
        ]
    },
    "grade_1": {
        "title": "1. Sınıf (Primary Grade 1)",
        "icon": "🎒",
        "description": "MEB 1. Sınıf müfredatına uygun selamlaşma, meyveler ve vücudumuz.",
        "levels": [
            {
                "id": "g1_1",
                "title": "1. Level: Greetings (Selamlaşma)",
                "topic_desc": "Günlük yaşamda merhaba ve vedalaşma kelimeleri.",
                "words": [
                    {"en": "Hello", "tr": "Merhaba", "emoji": "👋", "color": "#4CAF50"},
                    {"en": "Goodbye", "tr": "Hoşça Kal", "emoji": "🙋‍♂️", "color": "#F44336"},
                    {"en": "Good Morning", "tr": "Günaydın", "emoji": "🌅", "color": "#FFC107"},
                    {"en": "Good Night", "tr": "İyi Geceler", "emoji": "🌙", "color": "#3F51B5"}
                ]
            },
            {
                "id": "g1_2",
                "title": "2. Level: Yummy Fruits (Lezzetli Meyveler)",
                "topic_desc": "Sevdiğimiz taze meyvelerin İngilizce karşılıkları.",
                "words": [
                    {"en": "Apple", "tr": "Elma", "emoji": "🍎", "color": "#F44336"},
                    {"en": "Banana", "tr": "Muz", "emoji": "🍌", "color": "#FFEB3B"},
                    {"en": "Orange", "tr": "Portakal", "emoji": "🍊", "color": "#FF9800"},
                    {"en": "Strawberry", "tr": "Çilek", "emoji": "🍓", "color": "#E91E63"},
                    {"en": "Grapes", "tr": "Üzüm", "emoji": "🍇", "color": "#9C27B0"}
                ]
            },
            {
                "id": "g1_3",
                "title": "3. Level: Body Parts (Vücudumuz)",
                "topic_desc": "Vücudumuzun bölümlerini öğrenelim.",
                "words": [
                    {"en": "Eye", "tr": "Göz", "emoji": "👁️", "color": "#2196F3"},
                    {"en": "Ear", "tr": "Kulak", "emoji": "👂", "color": "#FF9800"},
                    {"en": "Mouth", "tr": "Ağız", "emoji": "👄", "color": "#E91E63"},
                    {"en": "Nose", "tr": "Burun", "emoji": "👃", "color": "#795548"},
                    {"en": "Hand", "tr": "El", "emoji": "✋", "color": "#4CAF50"}
                ]
            }
        ]
    },
    "grade_2": {
        "title": "2. Sınıf (Primary Grade 2)",
        "icon": "📚",
        "description": "MEB 2. Sınıf ünitelere uygun okul eşyaları, aile ve araçlar.",
        "levels": [
            {
                "id": "g2_1",
                "title": "1. Level: Classroom Objects (Okul Eşyaları)",
                "topic_desc": "Sınıfta ve çantamızda bulunan nesneler.",
                "words": [
                    {"en": "Pencil", "tr": "Kurşun Kalem", "emoji": "✏️", "color": "#FFC107"},
                    {"en": "Book", "tr": "Kitap", "emoji": "📖", "color": "#2196F3"},
                    {"en": "Bag", "tr": "Çanta", "emoji": "🎒", "color": "#E91E63"},
                    {"en": "Ruler", "tr": "Cetvel", "emoji": "📏", "color": "#009688"},
                    {"en": "Eraser", "tr": "Silgi", "emoji": "🧽", "color": "#9C27B0"}
                ]
            },
            {
                "id": "g2_2",
                "title": "2. Level: Family Members (Ailemiz)",
                "topic_desc": "Aile fertlerini İngilizce ifade etme.",
                "words": [
                    {"en": "Mother", "tr": "Anne", "emoji": "👩", "color": "#E91E63"},
                    {"en": "Father", "tr": "Baba", "emoji": "👨", "color": "#1976D2"},
                    {"en": "Brother", "tr": "Erkek Kardeş", "emoji": "👦", "color": "#4CAF50"},
                    {"en": "Sister", "tr": "Kız Kardeş", "emoji": "👧", "color": "#FF9800"},
                    {"en": "Baby", "tr": "Bebek", "emoji": "👶", "color": "#00BCD4"}
                ]
            },
            {
                "id": "g2_3",
                "title": "3. Level: Vehicles (Ulaşım Araçları)",
                "topic_desc": "Çevremizde gördüğümüz taşıtlar.",
                "words": [
                    {"en": "Car", "tr": "Araba", "emoji": "🚗", "color": "#F44336"},
                    {"en": "Bus", "tr": "Otobüs", "emoji": "🚌", "color": "#FFC107"},
                    {"en": "Plane", "tr": "Uçak", "emoji": "✈️", "color": "#0288D1"},
                    {"en": "Bicycle", "tr": "Bisiklet", "emoji": "🚲", "color": "#4CAF50"},
                    {"en": "Train", "tr": "Tren", "emoji": "🚂", "color": "#795548"}
                ]
            }
        ]
    }
}

# ==========================================
# ANA UYGULAMA SINIFI (YATAY EKRAN DÜZENİ)
# ==========================================
class MentalUpEnglishApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Yatay Ekran Modu (MentalUP Tarzı 1280x720 Geniş Arayüz)
        self.title("MentalUP English - Çocuklar İçin İnteraktif İngilizce")
        self.geometry("1280x720")
        self.minsize(1024, 600)
        self.configure(bg="#1E1E2E") # Modern Koyu Arka Plan

        # İlerleme Durumu Ve Yıldızlar (Global Game State)
        self.unlocked_levels = {"k_1": True} # İlk seviye açık
        self.stars_earned = {}               # Seviye bazlı kazanılan yıldızlar
        self.total_stars = 0

        # Mevcut Aktif Seçimler
        self.current_grade_key = "kindergarten"
        self.current_level_data = None

        # Ana Konteyner
        self.container = tk.Frame(self, bg="#1E1E2E")
        self.container.pack(fill="both", expand=True)

        # İlk Açılış Sayfası -> Ana Menü
        self.show_main_menu()

    def clear_container(self):
        """Ekranda bulunan tüm bileşenleri temizler."""
        for widget in self.container.winfo_children():
            widget.destroy()

    # ==========================================
    # 1. ANA MENÜ (ŞIK VE AÇIKLAYICI ARAYÜZ)
    # ==========================================
    def show_main_menu(self):
        self.clear_container()

        # Üst Bilgi Çubuğu (Top Bar)
        top_bar = tk.Frame(self.container, bg="#2A2A40", height=70)
        top_bar.pack(fill="x", side="top")

        title_lbl = tk.Label(top_bar, text="🌟 MentalUP English World", font=("Segoe UI", 22, "bold"), fg="#FFD700", bg="#2A2A40")
        title_lbl.pack(side="left", padx=30, pady=15)

        star_lbl = tk.Label(top_bar, text=f"⭐ Toplam Yıldız: {self.total_stars}", font=("Segoe UI", 16, "bold"), fg="#FFCA28", bg="#2A2A40")
        star_lbl.pack(side="right", padx=30)

        # İçerik Alanı
        content_frame = tk.Frame(self.container, bg="#1E1E2E")
        content_frame.pack(fill="both", expand=True, padx=40, pady=20)

        welcome_lbl = tk.Label(content_frame, text="Hoş Geldin Küçük Öğrenci! Eğitim Düzeyini Seç:", font=("Segoe UI", 18, "bold"), fg="#FFFFFF", bg="#1E1E2E")
        welcome_lbl.pack(pady=10)

        # Düzey Seçim Kartları (Yan Yana Yatay Dizilim)
        cards_frame = tk.Frame(content_frame, bg="#1E1E2E")
        cards_frame.pack(expand=True, fill="both", pady=10)

        for grade_key, grade_info in CURRICULUM_DATA.items():
            card = tk.Frame(cards_frame, bg="#2B2D42", bd=0, relief="flat", highlightthickness=2, highlightbackground="#3D3C5A")
            card.pack(side="left", expand=True, fill="both", padx=15, pady=10)

            # İkon ve Başlık
            icon_lbl = tk.Label(card, text=grade_info["icon"], font=("Segoe UI", 50), bg="#2B2D42")
            icon_lbl.pack(pady=(20, 5))

            t_lbl = tk.Label(card, text=grade_info["title"], font=("Segoe UI", 16, "bold"), fg="#4E9F3D", bg="#2B2D42")
            t_lbl.pack(pady=5)

            desc_lbl = tk.Label(card, text=grade_info["description"], font=("Segoe UI", 11), fg="#A0A0B2", bg="#2B2D42", wraplength=220, justify="center")
            desc_lbl.pack(pady=10, padx=10)

            # Giriş Butonu
            btn = tk.Button(
                card, 
                text="Maceraya Başla 🚀", 
                font=("Segoe UI", 12, "bold"), 
                fg="#FFFFFF", 
                bg="#FF4757", 
                activebackground="#FF6B81",
                bd=0, 
                cursor="hand2",
                command=lambda g=grade_key: self.open_map_screen(g)
            )
            btn.pack(side="bottom", fill="x", padx=20, pady=20)

    # ==========================================
    # 2. SEVİYE VE HARİTA EKRANI (MAP VIEW)
    # ==========================================
    def open_map_screen(self, grade_key):
        self.current_grade_key = grade_key
        self.clear_container()

        grade_data = CURRICULUM_DATA[grade_key]

        # Üst Çubuk
        top_bar = tk.Frame(self.container, bg="#2A2A40", height=60)
        top_bar.pack(fill="x", side="top")

        back_btn = tk.Button(top_bar, text="⬅ Ana Menü", font=("Segoe UI", 11, "bold"), fg="#FFF", bg="#57606F", bd=0, cursor="hand2", command=self.show_main_menu)
        back_btn.pack(side="left", padx=20, pady=10)

        m_title = tk.Label(top_bar, text=f"{grade_data['icon']} {grade_data['title']} - Görev Haritası", font=("Segoe UI", 18, "bold"), fg="#00D2D3", bg="#2A2A40")
        m_title.pack(side="left", padx=20)

        # Harita İç Alanı (MentalUP Tarzı Yol Üzerindeki Level Düğümleri)
        map_canvas = tk.Canvas(self.container, bg="#1E272C", highlightthickness=0)
        map_canvas.pack(fill="both", expand=True)

        # Haritadaki Arka Plan Çizgisi (Path)
        map_canvas.create_line(150, 300, 1100, 300, fill="#546E7A", width=8, dash=(12, 8))

        levels = grade_data["levels"]
        step_x = 900 // (len(levels) if len(levels) > 1 else 1)

        for index, lvl in enumerate(levels):
            x = 200 + index * step_x
            y = 300 + ( -60 if index % 2 == 0 else 60 ) # Zikzak yol görünümü

            lvl_id = lvl["id"]
            is_unlocked = self.unlocked_levels.get(lvl_id, False)
            stars = self.stars_earned.get(lvl_id, 0)

            # Bağlantı Çizgileri
            if index > 0:
                prev_x = 200 + (index - 1) * step_x
                prev_y = 300 + ( -60 if (index - 1) % 2 == 0 else 60 )
                map_canvas.create_line(prev_x, prev_y, x, y, fill="#00E676" if is_unlocked else "#37474F", width=6)

            # Node (Seviye Butonu Alanı)
            node_color = "#FF9F1A" if is_unlocked else "#455A64"
            star_text = "⭐" * stars if stars > 0 else ("AÇIK" if is_unlocked else "KİLİTLİ 🔒")

            # Buton Taşıyıcı Frame
            node_frame = tk.Frame(map_canvas, bg="#1E272C")
            map_canvas.create_window(x, y, window=node_frame)

            btn_state = tk.NORMAL if is_unlocked else tk.DISABLED
            
            btn = tk.Button(
                node_frame, 
                text=f"{index+1}\n{lvl['title'].split(':')[1]}", 
                font=("Segoe UI", 11, "bold"),
                width=16, 
                height=3, 
                bg=node_color, 
                fg="#FFFFFF", 
                state=btn_state,
                cursor="hand2" if is_unlocked else "arrow",
                command=lambda l=lvl: self.start_level(l)
            )
            btn.pack()

            lbl_star = tk.Label(node_frame, text=star_text, font=("Segoe UI", 10, "bold"), fg="#FFD700", bg="#1E272C")
            lbl_star.pack(pady=5)

    # ==========================================
    # 3. İNTERAKTİF DERS VE OYUN MODÜLÜ
    # ==========================================
    def start_level(self, level_data):
        self.current_level_data = level_data
        self.quiz_index = 0
        self.score = 0
        self.words = level_data["words"]

        # Öncelikle Konuyu Anlatan Ders Ekranını Başlat
        self.show_learning_phase()

    def show_learning_phase(self):
        """MentalUP Tarzı Konu Anlatım Ekranı."""
        self.clear_container()

        top_bar = tk.Frame(self.container, bg="#2A2A40", height=50)
        top_bar.pack(fill="x", side="top")

        lbl_top = tk.Label(top_bar, text=f"DERS: {self.current_level_data['title']}", font=("Segoe UI", 14, "bold"), fg="#FFD700", bg="#2A2A40")
        lbl_top.pack(side="left", padx=20, pady=10)

        # Ders Anlatım Alanı
        main_frame = tk.Frame(self.container, bg="#1E1E2E")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)

        info_lbl = tk.Label(main_frame, text=f"💡 {self.current_level_data['topic_desc']}\nKelimeleri incele ve test için hazır ol!", font=("Segoe UI", 14), fg="#FFFFFF", bg="#1E1E2E")
        info_lbl.pack(pady=10)

        # Kelimelerin Kartlar Halinde Gösterimi (Yatay Grid)
        cards_grid = tk.Frame(main_frame, bg="#1E1E2E")
        cards_grid.pack(expand=True, fill="both", pady=10)

        for word_info in self.words:
            card = tk.Frame(cards_grid, bg="#2B2D42", bd=0, relief="flat", highlightthickness=2, highlightbackground=word_info["color"])
            card.pack(side="left", expand=True, fill="both", padx=10, pady=10)

            # Emoji / Görsel Nesne
            e_lbl = tk.Label(card, text=word_info["emoji"], font=("Segoe UI", 48), bg="#2B2D42")
            e_lbl.pack(pady=(15, 0))

            # İngilizce Kelime
            en_lbl = tk.Label(card, text=word_info["en"], font=("Segoe UI", 16, "bold"), fg=word_info["color"], bg="#2B2D42")
            en_lbl.pack(pady=5)

            # Türkçe Anlamı
            tr_lbl = tk.Label(card, text=word_info["tr"], font=("Segoe UI", 12), fg="#A0A0B2", bg="#2B2D42")
            tr_lbl.pack(pady=(0, 15))

        # Teste Başla Butonu
        start_quiz_btn = tk.Button(
            main_frame, 
            text="Öğrendim, Alıştırmalara Başla! 🎮", 
            font=("Segoe UI", 14, "bold"), 
            fg="#FFFFFF", 
            bg="#2ED573", 
            activebackground="#26AF5F",
            bd=0, 
            cursor="hand2",
            padx=20,
            pady=10,
            command=self.show_quiz_phase
        )
        start_quiz_btn.pack(side="bottom", pady=15)

    def show_quiz_phase(self):
        """Oyunlaştırılmış Test Ekranı."""
        self.clear_container()

        if self.quiz_index >= len(self.words):
            self.finish_level()
            return

        current_word = self.words[self.quiz_index]

        # Üst Çubuk / İlerleme
        top_bar = tk.Frame(self.container, bg="#2A2A40", height=50)
        top_bar.pack(fill="x", side="top")

        lbl_progress = tk.Label(top_bar, text=f"Soru {self.quiz_index + 1} / {len(self.words)}", font=("Segoe UI", 14, "bold"), fg="#00D2D3", bg="#2A2A40")
        lbl_progress.pack(side="left", padx=20, pady=10)

        # Soru Alanı
        quiz_frame = tk.Frame(self.container, bg="#1E1E2E")
        quiz_frame.pack(fill="both", expand=True, padx=40, pady=20)

        question_lbl = tk.Label(quiz_frame, text="Aşağıdaki görselin İngilizce karşılığı hangisidir?", font=("Segoe UI", 16, "bold"), fg="#FFFFFF", bg="#1E1E2E")
        question_lbl.pack(pady=10)

        # Soru Görseli (Big Emoji)
        img_lbl = tk.Label(quiz_frame, text=current_word["emoji"], font=("Segoe UI", 90), bg="#1E1E2E")
        img_lbl.pack(pady=10)

        # Seçenekleri Hazırlama (Şıklar)
        options = [current_word["en"]]
        all_other_words = [w["en"] for w in self.words if w["en"] != current_word["en"]]
        
        # Seçenek yetersizse tüm müfredattan yanlış şık çek
        if len(all_other_words) < 3:
            all_other_words = ["Cat", "Dog", "Red", "Blue", "Apple", "Book", "Car", "One"]
            all_other_words = [w for w in all_other_words if w != current_word["en"]]

        random_wrong = random.sample(all_other_words, min(3, len(all_other_words)))
        options.extend(random_wrong)
        random.shuffle(options)

        # Şıkları Buton Olarak Dizme (2x2 Grid Düzeni)
        opts_frame = tk.Frame(quiz_frame, bg="#1E1E2E")
        opts_frame.pack(pady=20)

        for i, opt in enumerate(options):
            r = i // 2
            c = i % 2

            btn = tk.Button(
                opts_frame,
                text=opt,
                font=("Segoe UI", 14, "bold"),
                width=18,
                height=2,
                bg="#2B2D42",
                fg="#FFFFFF",
                activebackground="#3F4156",
                bd=0,
                cursor="hand2",
                command=lambda chosen=opt: self.check_answer(chosen, current_word["en"])
            )
            btn.grid(row=r, column=c, padx=15, pady=15)

    def check_answer(self, chosen_option, correct_option):
        """Cevap Kontrolü."""
        if chosen_option == correct_option:
            self.score += 1
            messagebox.showinfo("Tebrikler! 🎉", "Doğru Cevap! Harikasın! 🌟")
        else:
            messagebox.showerror("Üzgünüm 😅", f"Yanlış Cevap!\nDoğrusu: {correct_option}")

        self.quiz_index += 1
        self.show_quiz_phase()

    # ==========================================
    # 4. SEVİYE TAMAMLAMA VE ÖDÜL EKRANI
    # ==========================================
    def finish_level(self):
        self.clear_container()

        total_q = len(self.words)
        ratio = self.score / total_q

        # Yıldız Hesaplama
        if ratio == 1.0:
            stars = 3
        elif ratio >= 0.5:
            stars = 2
        else:
            stars = 1

        lvl_id = self.current_level_data["id"]
        self.stars_earned[lvl_id] = max(self.stars_earned.get(lvl_id, 0), stars)
        self.total_stars = sum(self.stars_earned.values())

        # Sonraki Seviyenin Kilidini Açma
        levels = CURRICULUM_DATA[self.current_grade_key]["levels"]
        curr_idx = next(i for i, l in enumerate(levels) if l["id"] == lvl_id)
        if curr_idx + 1 < len(levels):
            next_lvl_id = levels[curr_idx + 1]["id"]
            self.unlocked_levels[next_lvl_id] = True

        # Tebrik Ekranı UI
        res_frame = tk.Frame(self.container, bg="#1E1E2E")
        res_frame.pack(fill="both", expand=True, padx=40, pady=40)

        congrats_lbl = tk.Label(res_frame, text="LEVEL TAMAMLANDI! 🏆", font=("Segoe UI", 26, "bold"), fg="#FFD700", bg="#1E1E2E")
        congrats_lbl.pack(pady=10)

        stars_lbl = tk.Label(res_frame, text="⭐ " * stars, font=("Segoe UI", 48), bg="#1E1E2E")
        stars_lbl.pack(pady=10)

        score_lbl = tk.Label(res_frame, text=f"Toplam Skor: {self.score} / {total_q}", font=("Segoe UI", 16), fg="#FFFFFF", bg="#1E1E2E")
        score_lbl.pack(pady=5)

        map_btn = tk.Button(
            res_frame,
            text="Haritaya Dön 🗺️",
            font=("Segoe UI", 14, "bold"),
            fg="#FFFFFF",
            bg="#2ED573",
            bd=0,
            cursor="hand2",
            padx=20,
            pady=10,
            command=lambda: self.open_map_screen(self.current_grade_key)
        )
        map_btn.pack(pady=30)


# ==========================================
# UYGULAMANIN BAŞLATILMASI
# ==========================================
if __name__ == "__main__":
    app = MentalUpEnglishApp()
    app.mainloop()
